#!/usr/bin/env python3
"""
kads — Kozbeyli Konağı Reklam Operasyonları CLI.

Tek yuzey, deterministik cikti, sysexits cikis kodlari. OpenCLI + Agent-Reach
desenleri: doctor (kendi kendini teshis), --format table|json|yaml|md|csv,
pluggable platformlar (google/meta), safe/dry-run varsayilan (yazma guardrail'li).

Komutlar:
  doctor          Ortam + config + kanal teshisi (kendi kendini kontrol)
  config          Cozulmus ayarlar (secret'lar maskeli)
  plan            30.000 TL capraz kanal plani
  budget          Butce dagilimi + gunluk/aylik tavanlar
  kpi             Blended ROAS/CPA + rezervasyon kirilim matematigi
  keywords        Google anahtar kelime + negatif setleri
  creative <p>    RSA (google) veya Meta reklam metinleri
  build <hedef>   google | meta | all  -> import-hazir dosyalar (out/)
  validate        RSA uzunluk + butce + CSV butunluk dogrulamasi
  guard           Degisiklik guardrail kontrolu (scripts/guardrails.py sarmalar)
  monitor         Salt-okunur izleme yolu (MCP baglandiginda)
  brief           Haftalik brief sablonu uret
  version | help

Her komut: --format (varsayilan table). Cikis kodlari: 0 ok, 2 kullanim, 66 bos,
69 servis yok, 77 onay gerekli, 78 config hatasi.
"""
from __future__ import annotations

import json
import socket
import subprocess
import sys
from pathlib import Path

from kads import core, data
from kads.platforms import google as gx
from kads.platforms import meta as mx
from kads import seo as sx
from kads import presence as px
from kads import rules as rx
from kads import report as rp
from kads import data_ext as dx
from kads import data_growth as dg
from kads import calendar as calx
from kads import publish as pubx
import shutil

ROOT = core.ROOT
OUT = ROOT / "out"
VERSION = "1.15.1"


# ---- arg ayiklama ----------------------------------------------------------
def _opt(args: list[str], name: str, default=None):
    if name in args:
        i = args.index(name)
        if i + 1 < len(args):
            return args[i + 1]
    return default


def _fmt(args: list[str]) -> str:
    return _opt(args, "--format", _opt(args, "-f", "table"))


# ---- doctor ----------------------------------------------------------------
def _net(host: str, port: int = 443, timeout: float = 4.0) -> bool:
    try:
        socket.create_connection((host, port), timeout=timeout).close()
        return True
    except OSError:
        return False


def cmd_doctor(args: list[str]) -> int:
    fmt = _fmt(args)
    env = core.load_env()
    rows: list[dict] = []

    def add(name, ok, detail):
        rows.append({"kontrol": name, "durum": ("OK" if ok else "UYARI"), "detay": detail})

    # 1) Python + dosyalar
    add("python3", sys.version_info >= (3, 8), f"{sys.version.split()[0]}")
    add(".mcp.json", (ROOT / ".mcp.json").exists(),
        "var" if (ROOT / ".mcp.json").exists() else "yok — cp .mcp.json.example .mcp.json")
    add(".env", (ROOT / ".env").exists(),
        "var" if (ROOT / ".env").exists() else "yok — cp .env.example .env")
    add("config/ads-assets.yaml", core.CONFIG_FILE.exists(), "var" if core.CONFIG_FILE.exists() else "yok")

    # 2) Olcum kimlikleri
    for key in ("GA4_MEASUREMENT_ID", "GOOGLE_ADS_TAG_ID", "META_PIXEL_ID"):
        v = env.get(key, "")
        add(key, bool(v) and not core.is_placeholder(v), v or "eksik")
    gtm = env.get("GTM_CONTAINER_ID", "")
    add("GTM_CONTAINER_ID", bool(gtm), gtm or "çöz: docs/02 (iki aday)")

    # 3) Reklam hesabi kimlikleri (yazma icin gerekli)
    meta_acc = env.get("META_AD_ACCOUNT_ID", "")
    add("META_AD_ACCOUNT_ID", meta_acc.startswith("act_") and not core.is_placeholder(meta_acc),
        meta_acc if not core.is_placeholder(meta_acc) else "eksik — act_...")
    g_id = "".join(ch for ch in env.get("GOOGLE_ADS_CUSTOMER_ID", "") if ch.isdigit())
    add("GOOGLE_ADS_CUSTOMER_ID", len(g_id) == 10, g_id or "eksik — 10 hane")
    dev = env.get("GOOGLE_ADS_DEVELOPER_TOKEN", "")
    add("GOOGLE_ADS_DEVELOPER_TOKEN", bool(dev) and not core.is_placeholder(dev),
        "tanımlı (gizli)" if dev and not core.is_placeholder(dev) else "eksik (Explorer+)")

    # 4) Yazma kapisi
    writes = env.get("ADS_WRITES_ENABLED", "false").lower() == "true"
    add("ADS_WRITES_ENABLED", not writes, "kapalı (güvenli)" if not writes else "AÇIK — guardrail şart")

    # 5) Guardrail import
    gp = ROOT / "scripts" / "guardrails.py"
    add("guardrails.py", gp.exists(), "var" if gp.exists() else "yok")

    # 6) Veri butunlugu (RSA uzunluk)
    bad = _length_problems()
    add("RSA uzunlukları", not bad, "tümü ≤30/≤90" if not bad else f"{len(bad)} sorun (kads validate)")

    # 7) Ag (best-effort, fail-soft)
    add("ag: mcp.facebook.com", _net("mcp.facebook.com"), "erişilebilir / connector OAuth")
    add("ag: github.com", _net("github.com"), "erişilebilir")

    warns = [r for r in rows if r["durum"] != "OK"]
    if fmt == "table":
        core.banner(f"kads doctor — {data.HOTEL['name']}")
    core.emit(rows, fmt=fmt, title=None, columns=["kontrol", "durum", "detay"])
    if fmt == "table":
        crit = [r for r in warns if r["kontrol"] in
                ("config/ads-assets.yaml", "guardrails.py")]
        print()
        if crit:
            print(core.red(f"  {len(crit)} kritik eksik — kurulumu tamamla (README)."))
        elif warns:
            print(core.yellow(f"  {len(warns)} uyarı — çoğu 'sen doldur' (kimlik/GTM). Yazma için gerekli."))
        else:
            print(core.green("  Her şey hazır."))
    # Kritik dosyalar yoksa config hatasi dondur; aksi halde ok (uyarilar fail degil).
    crit_missing = not (ROOT / "scripts" / "guardrails.py").exists() or not core.CONFIG_FILE.exists()
    return core.EX_CONFIG if crit_missing else core.EX_OK


# ---- config ----------------------------------------------------------------
def cmd_config(args: list[str]) -> int:
    env = core.load_env()
    keys = ["GA4_MEASUREMENT_ID", "GOOGLE_ADS_TAG_ID", "META_PIXEL_ID", "META_BUSINESS_ID",
            "GTM_CONTAINER_ID", "META_AD_ACCOUNT_ID", "GOOGLE_ADS_CUSTOMER_ID",
            "GOOGLE_ADS_DEVELOPER_TOKEN", "GOOGLE_MONTHLY_BUDGET_TRY", "META_MONTHLY_BUDGET_TRY",
            "ADS_WRITES_ENABLED"]
    rows = [{"anahtar": k, "deger": core.mask(k, env.get(k, "")) or core.dim("(boş)")} for k in keys]
    core.emit(rows, fmt=_fmt(args), title=f"Cozulmus ayarlar — {data.HOTEL['name']}",
              columns=["anahtar", "deger"])
    return core.EX_OK


# ---- plan ------------------------------------------------------------------
def cmd_plan(args: list[str]) -> int:
    core.emit(data.PLAN["channels"], fmt=_fmt(args), title="30.000 TL/ay capraz kanal plani",
              columns=["kanal", "aylik_try", "gunluk_try", "islev", "faz"])
    return core.EX_OK


# ---- budget ----------------------------------------------------------------
def cmd_budget(args: list[str]) -> int:
    p, caps = data.PLAN, data.BUDGET_CAPS
    rows = [
        {"kalem": "Toplam aylık", "TRY": p["total_monthly_try"]},
        {"kalem": "Google aylık", "TRY": p["google_monthly_try"]},
        {"kalem": "Meta aylık", "TRY": p["meta_monthly_try"]},
        {"kalem": "Google günlük tavan", "TRY": caps["google_daily_try"]},
        {"kalem": "Meta günlük tavan", "TRY": caps["meta_daily_try"]},
    ]
    core.emit(rows, fmt=_fmt(args), title="Butce dagilimi ve tavanlar", columns=["kalem", "TRY"])
    return core.EX_OK


# ---- kpi -------------------------------------------------------------------
def cmd_kpi(args: list[str]) -> int:
    rev = _opt(args, "--revenue")
    spend = _opt(args, "--spend")
    if rev and spend:
        try:
            rev_f, sp_f = float(rev), float(spend)
        except ValueError:
            print(core.red("--revenue ve --spend sayısal olmalı")); return core.EX_USAGE
        roas = rev_f / sp_f if sp_f else 0
        rows = [{"metrik": "Harcama", "deger": f"{sp_f:,.0f} TL"},
                {"metrik": "İzlenen gelir", "deger": f"{rev_f:,.0f} TL"},
                {"metrik": "Blended ROAS", "deger": f"{roas:.2f}x"},
                {"metrik": "Yorum", "deger": "≥3x hedef; <2x ise optimize et"}]
        core.emit(rows, fmt=_fmt(args), title="Blended ROAS", columns=["metrik", "deger"])
        return core.EX_OK
    # Varsayilan: rezervasyon kirilim matematigi
    rows = []
    for t in data.PLAN["commercial_targets"]:
        for avg in (7500, 10000):
            rows.append({"hedef": t["hedef"],
                         "ort_rezervasyon_TL": avg,
                         "gereken_gelir_TL": t["izlenen_rezervasyon_geliri_try"],
                         "gereken_rezervasyon": -(-t["izlenen_rezervasyon_geliri_try"] // avg)})
    core.emit(rows, fmt=_fmt(args), title="Rezervasyon kirilim (30.000 TL medya)",
              columns=["hedef", "ort_rezervasyon_TL", "gereken_gelir_TL", "gereken_rezervasyon"])
    if _fmt(args) == "table":
        print("\n  " + core.dim(data.KPI["whatsapp_formula"]))
        print("  " + core.dim(data.KPI["ornek"]))
    return core.EX_OK


# ---- keywords --------------------------------------------------------------
def cmd_keywords(args: list[str]) -> int:
    rows = []
    for grp, spec in data.KEYWORDS.items():
        for term in spec["terms"]:
            rows.append({"reklam_grubu": grp, "anahtar_kelime": term,
                         "eslesme": spec["match"]})
    core.emit(rows, fmt=_fmt(args), title=f"Anahtar kelimeler ({len(rows)})",
              columns=["reklam_grubu", "anahtar_kelime", "eslesme"])
    if _fmt(args) == "table":
        print(core.dim(f"\n  + {len(data.NEGATIVES)} negatif anahtar kelime (kads creative ile/CSV)"))
    return core.EX_OK


# ---- creative --------------------------------------------------------------
def cmd_creative(args: list[str]) -> int:
    platform = args[0] if args and not args[0].startswith("-") else "google"
    fmt = _fmt(args)
    if platform == "meta":
        core.emit(mx.copy_rows(), fmt=fmt, title="Meta reklam metinleri",
                  columns=["Konsept", "Tema", "Varyant", "Primary Text", "Headline", "CTA"])
        return core.EX_OK
    # google RSA
    rows = []
    for grp, a in data.RSA.items():
        for h in a["headlines"]:
            rows.append({"grup": grp, "tip": "headline", "metin": h, "uzunluk": len(h)})
        for d in a["descriptions"]:
            rows.append({"grup": grp, "tip": "description", "metin": d, "uzunluk": len(d)})
    core.emit(rows, fmt=fmt, title="Google RSA varlıkları", columns=["grup", "tip", "metin", "uzunluk"])
    return core.EX_OK


# ---- build -----------------------------------------------------------------
def cmd_build(args: list[str]) -> int:
    target = args[0] if args and not args[0].startswith("-") else "all"
    out = Path(_opt(args, "--out", str(OUT)))
    results: list[dict] = []
    if target in ("google", "all"):
        for fn, n in gx.build(out / "google-editor"):
            results.append({"platform": "google", "dosya": fn, "satır/öğe": n})
    if target in ("meta", "all"):
        for fn, n in mx.build(out / "meta"):
            results.append({"platform": "meta", "dosya": fn, "satır/öğe": n})
    if target in ("seo", "all"):
        for fn, n in sx.build(out / "seo"):
            results.append({"platform": "seo", "dosya": fn, "satır/öğe": n})
    if not results:
        print(core.red(f"Bilinmeyen hedef: {target} (google|meta|seo|all)")); return core.EX_USAGE
    core.emit(results, fmt=_fmt(args), title=f"Üretildi → {out}",
              columns=["platform", "dosya", "satır/öğe"])
    if _fmt(args) == "table":
        print(core.green(f"\n  ✓ {len(results)} dosya. Google: Editor import; Meta: kurulum rehberi."))
    return core.EX_OK



# ---- seo (yerel SEO + Google Isletme Profili) ------------------------------
def cmd_seo(args: list[str]) -> int:
    sub = args[0] if args and not args[0].startswith("-") else "all"
    fmt = _fmt(args)
    if sub in ("schema", "jsonld"):
        print(json.dumps(sx.schema_jsonld(), ensure_ascii=False, indent=2))
        return core.EX_OK
    if sub == "gbp":
        core.emit(sx.gbp_rows(), fmt=fmt, title="Google Isletme Profili kontrol listesi",
                  columns=["alan", "yapılacak", "öncelik"])
        return core.EX_OK
    if sub in ("local", "citations", "nap"):
        core.emit(sx.citation_rows(), fmt=fmt, title="NAP / atif listesi",
                  columns=["platform", "öncelik", "not"])
        return core.EX_OK
    if sub == "brand":
        core.emit(sx.brand_rows(), fmt=fmt, title="Markali arama hakimiyeti",
                  columns=["yüzey", "taktik", "beklenti"])
        return core.EX_OK
    # all: ozet
    if fmt != "table":
        core.emit(sx.brand_rows(), fmt=fmt, columns=["yüzey", "taktik", "beklenti"])
        return core.EX_OK
    core.banner("kads seo — yerel SEO + Google Isletme")
    print(core.dim("  Markali 'Kozbeyli Konağı' #1 ulaşılabilir; jenerik organik #1 GARANTI degil.\n"))
    core.emit(sx.brand_rows(), fmt="table", title="Markali hakimiyet",
              columns=["yüzey", "taktik", "beklenti"])
    print()
    core.emit(sx.gbp_rows()[:6], fmt="table", title="GBP (ilk 6 — tamami: kads seo gbp)",
              columns=["alan", "yapılacak", "öncelik"])
    print(core.dim("\n  Sema/JSON-LD: kads seo schema   •   Uret: kads build seo"))
    return core.EX_OK


# ---- validate --------------------------------------------------------------
def _length_problems() -> list[dict]:
    bad = []
    for grp, a in data.RSA.items():
        for h in a["headlines"]:
            if len(h) > 30:
                bad.append({"grup": grp, "tip": "headline", "metin": h, "uzunluk": len(h)})
        for d in a["descriptions"]:
            if len(d) > 90:
                bad.append({"grup": grp, "tip": "description", "metin": d, "uzunluk": len(d)})
    return bad


def cmd_validate(args: list[str]) -> int:
    fmt = _fmt(args)
    checks: list[dict] = []
    bad = _length_problems()
    checks.append({"kontrol": "RSA uzunlukları (≤30/≤90)", "sonuç": "GEÇTİ" if not bad else f"{len(bad)} SORUN"})
    # her grupta 15 headline / 4 description (öneri)
    for grp, a in data.RSA.items():
        checks.append({"kontrol": f"RSA {grp} başlık adedi", "sonuç": f"{len(a['headlines'])} (öneri 15)"})
        checks.append({"kontrol": f"RSA {grp} açıklama adedi", "sonuç": f"{len(a['descriptions'])} (öneri 4)"})
    # butce tavanlari plan ile uyumlu mu
    caps_ok = (data.BUDGET_CAPS["google_monthly_try"] == data.PLAN["google_monthly_try"]
               and data.BUDGET_CAPS["meta_monthly_try"] == data.PLAN["meta_monthly_try"])
    checks.append({"kontrol": "Bütçe tavanı = plan", "sonuç": "GEÇTİ" if caps_ok else "UYUMSUZ"})
    # CSV uretimi calisiyor mu (gecici dizine)
    import tempfile
    try:
        tmp = Path(tempfile.mkdtemp())
        gn = sum(n for _, n in gx.build(tmp / "g"))
        mn = sum(n for _, n in mx.build(tmp / "m"))
        checks.append({"kontrol": "CSV üretimi (google+meta)", "sonuç": f"GEÇTİ ({gn}+{mn} satır)"})
    except Exception as exc:  # noqa: BLE001
        checks.append({"kontrol": "CSV üretimi", "sonuç": f"HATA: {exc}"})
    core.emit(checks, fmt=fmt, title="Doğrulama", columns=["kontrol", "sonuç"])
    ok = not bad and caps_ok and not any("HATA" in c["sonuç"] for c in checks)
    if fmt == "table":
        print((core.green("\n  ✓ Tüm doğrulamalar geçti.") if ok else core.red("\n  ✗ Sorun var.")))
    return core.EX_OK if ok else core.EX_GENERIC


# ---- guard (guardrails.py sarmalayici) -------------------------------------
def cmd_guard(args: list[str]) -> int:
    gp = ROOT / "scripts" / "guardrails.py"
    if not gp.exists():
        print(core.red("scripts/guardrails.py yok")); return core.EX_CONFIG
    check = _opt(args, "--check")
    if not check:
        print(core.yellow("Kullanım: kads guard --check change.json [--approval \"ONAYLA | ...\"]"))
        print(core.dim("Çıkış: 0 ALLOW, 1 DENY, 2 NEEDS_APPROVAL (sysexits 77 onay)."))
        return core.EX_USAGE
    cmd = [sys.executable, str(gp), "--check", check]
    appr = _opt(args, "--approval")
    if appr:
        cmd += ["--approval", appr]
    proc = subprocess.run(cmd)
    # guardrails: 0 ALLOW, 1 DENY, 2 NEEDS_APPROVAL -> sysexits'e esle
    return {0: core.EX_OK, 1: core.EX_GENERIC, 2: core.EX_NOPERM}.get(proc.returncode, proc.returncode)


# ---- monitor ---------------------------------------------------------------
def cmd_monitor(args: list[str]) -> int:
    env = core.load_env()
    meta_ok = env.get("META_AD_ACCOUNT_ID", "").startswith("act_") and not core.is_placeholder(env.get("META_AD_ACCOUNT_ID", ""))
    g_ok = len("".join(c for c in env.get("GOOGLE_ADS_CUSTOMER_ID", "") if c.isdigit())) == 10
    rows = [
        {"kanal": "Meta hesabı", "durum": "bağlanmaya hazır" if meta_ok else "act_ ID eksik"},
        {"kanal": "Google hesabı", "durum": "bağlanmaya hazır" if g_ok else "10 hane ID eksik"},
    ]
    fmt = _fmt(args)
    if fmt == "table":
        core.banner("kads monitor — salt okunur izleme")
        print("Canlı veri için MCP bağlantısı gerekir (henüz bu oturumda yok).")
        print("Yollar:")
        print("  • Meta resmî connector: https://mcp.facebook.com/ads  (OAuth, 29 araç, okuma+yazma)")
        print("  • Google okuma MCP: googleads/google-ads-mcp  (GAQL search, salt okuma)")
        print("  • Claude skill: /kozbeyli-ads-monitor son 7 günü önceki 7 günle karşılaştır")
    core.emit(rows, fmt=fmt, columns=["kanal", "durum"])
    return core.EX_OK if (meta_ok or g_ok) else core.EX_UNAVAILABLE


# ---- brief -----------------------------------------------------------------
def cmd_brief(args: list[str]) -> int:
    out = Path(_opt(args, "--out", str(OUT)))
    out.mkdir(parents=True, exist_ok=True)
    p = out / "haftalik-brief-sablonu.md"
    p.write_text(_BRIEF_TEMPLATE, encoding="utf-8")
    if _fmt(args) == "json":
        print(json.dumps({"out": str(p)}, ensure_ascii=False))
    else:
        print(core.green(f"✓ {p}"))
    return core.EX_OK


_BRIEF_TEMPLATE = """# Kozbeyli Konağı — Haftalık Reklam Brief'i

Dönem: ____ – ____   (önceki hafta ile karşılaştır)

## Blended (Google + Meta)
- Toplam harcama: ____ TL  |  İzlenen rezervasyon geliri: ____ TL
- Blended ROAS: ____x  |  Blended CPA: ____ TL

## Google
- Marka: spend ____ / clicks ____ / CTR ____ / dönüşüm ____
- Non-brand: spend ____ / arama terimi notları ____ / yeni negatifler ____

## Meta
- Prospecting: spend ____ / CPM ____ / CTR ____ / Purchase ____
- WhatsApp: spend ____ / mesaj ____ / nitelikli lead ____
- Retargeting (ay 2+): spend ____ / dönüşüm ____

## Aksiyonlar (bu hafta)
- [ ] Negatif ekle: ____
- [ ] Düşük performans kreatif/keyword duraklat: ____
- [ ] Doluluk: dolu tarihlerde harcamayı kıs, boş döneme yönlendir
- [ ] Teklif stratejisi gözden geçir (yeterli dönüşüm birikti mi?)

## Riskler / notlar
- Meta connector token süresi (~60 gün) — yenileme hatırlatması
- Ölçüm doğrulaması (purchase) hâlâ sağlam mı?
"""



# ---- presence (dijital varlik denetimi) ------------------------------------
def cmd_presence(args: list[str]) -> int:
    sub = args[0] if args and not args[0].startswith("-") else "all"
    fmt = _fmt(args)
    if sub in ("fix", "fixes", "todo"):
        core.emit(px.fix_rows(), fmt=fmt, title="Onceliklendirilmis duzeltme listesi",
                  columns=["#", "bulgu", "mülk", "öncelik", "aksiyon"])
        return core.EX_OK
    if sub in ("props", "properties", "list"):
        core.emit(px.property_rows(), fmt=fmt, title="Dijital mulk envanteri",
                  columns=["mülk", "tür", "durum", "bulgu", "öncelik"])
        return core.EX_OK
    # all: ozet
    c = px.counts()
    if fmt != "table":
        core.emit(px.property_rows(), fmt=fmt, columns=["mülk", "tür", "durum", "bulgu", "öncelik"])
        return core.EX_OK
    core.banner("kads presence — dijital varlik denetimi (docs/09)")
    print(f"  Düzeltme: {core.red(str(c['Kritik'])+' Kritik')}  "
          f"{core.yellow(str(c['Yüksek'])+' Yüksek')}  {c['Orta']} Orta  {c['Düşük']} Düşük\n")
    core.emit(px.property_rows(), fmt="table", title="Mülk envanteri",
              columns=["mülk", "durum", "öncelik"])
    print()
    core.emit([r for r in px.fix_rows() if r["öncelik"] == "Kritik"], fmt="table",
              title="KRİTİK düzeltmeler", columns=["#", "bulgu", "aksiyon"])
    print(core.dim("\n  Tümü: kads presence fixes  •  Envanter: kads presence props  •  docs/09"))
    return core.EX_OK



# ---- mcp ---------------------------------------------------------------------
def cmd_mcp(args):
    env = core.load_env(); have = (ROOT / ".mcp.json").exists()
    rows = [
        {"connector": "meta-ads", "tip": "http (Claude.ai web)", "yol": "mcp.facebook.com/ads",
         "durum": "yapilandirildi" if have else ".mcp.json yok"},
        {"connector": "google-ads-readonly", "tip": "stdio (pipx)", "yol": "googleads/google-ads-mcp",
         "durum": "yapilandirildi" if have else ".mcp.json yok"},
    ]
    if _fmt(args) == "table":
        core.banner("kads mcp — baglanti durumu")
    core.emit(rows, fmt=_fmt(args), columns=["connector", "tip", "yol", "durum"])
    if _fmt(args) == "table":
        print(core.dim("\n  Meta: Claude.ai web connector ekle (OAuth bug -> Claude Code degil)."))
        print(core.dim("  Google: .env doldur (PROJECT_ID, DEVELOPER_TOKEN, OAUTH). Kurulum: docs/13"))
        ok = all(not core.is_placeholder(env.get(k, "")) for k in ("GOOGLE_PROJECT_ID", "GOOGLE_ADS_DEVELOPER_TOKEN"))
        print((core.green("  Google env hazir.") if ok else core.yellow("  Google env eksik (docs/13).")))
    return core.EX_OK


# ---- skills ------------------------------------------------------------------
def cmd_skills(args):
    rows = [
        {"skill": "/spy", "is": "Rakip aktif reklamlar + haftalik fark", "paket": "AgriciDaniel/claude-ads"},
        {"skill": "/competitive-ads-extractor", "is": "Hook siralama + gap analizi", "paket": "ComposioHQ/awesome-claude-skills"},
        {"skill": "/bulk-creative", "is": "20 reklam metni varyanti", "paket": "AgriciDaniel/claude-ads"},
        {"skill": "/ads meta", "is": "186 kontrol hesap sagligi", "paket": "AgriciDaniel/claude-ads"},
        {"skill": "/ads-score", "is": "Reklami 6 boyutta puanla", "paket": "AgriciDaniel/claude-ads"},
    ]
    core.emit(rows, fmt=_fmt(args), title="Meta reklam Claude skilleri (docs/11)", columns=["skill", "is", "paket"])
    if _fmt(args) == "table":
        print(core.dim("\n  Kur: scripts/install-skills.sh (mac/linux) - scripts/install-skills.bat (win)"))
        print(core.dim("  On kosul: export META_ACCESS_TOKEN=...  (sohbete/URLye YAZMA)"))
    return core.EX_OK


# ---- rules -------------------------------------------------------------------
def cmd_rules(args):
    fmt = _fmt(args); mfile = _opt(args, "--metrics")
    if mfile:
        mp = Path(mfile)
        if not mp.exists():
            print(core.red(f"Metrik dosyasi bulunamadi: {mfile}")); return core.EX_NOINPUT
        trig = rx.evaluate(rx.load_metrics_csv(mp))
        if not trig:
            print(core.green("Tetiklenen kural yok (metrikler esik icinde).")); return core.EX_OK
        core.emit(trig, fmt=fmt, title="Tetiklenen optimizasyon onerileri",
                  columns=["oncelik", "id", "metrik", "deger", "kosul", "aksiyon"])
        print(core.dim("\n  Oneri: degisiklik kads guard + acik onaydan gecer (otomatik uygulanmaz)."))
        return core.EX_OK
    core.emit(rx.rule_rows(), fmt=fmt, title="Butce/teklif optimizasyon kurallari",
              columns=["oncelik", "id", "metrik", "kosul", "aksiyon"])
    if fmt == "table":
        print(core.dim("\n  Metrige uygula: kads rules --metrics metrics.csv  (sablon: kads report --template)"))
    return core.EX_OK


# ---- audiences ---------------------------------------------------------------
def cmd_audiences(args):
    core.emit(mx.audiences_rows(), fmt=_fmt(args), title="Retargeting / Lookalike kitleleri",
              columns=["Kitle", "Tip", "Kaynak", "Pencere", "Kullanim"])
    if _fmt(args) == "table":
        print(core.dim("\n  " + dx.RETARGETING_NOTE))
    return core.EX_OK


# ---- report ------------------------------------------------------------------
def cmd_report(args):
    fmt = _fmt(args); mfile = _opt(args, "--metrics")
    if mfile:
        mp = Path(mfile)
        if not mp.exists():
            print(core.red(f"Metrik dosyasi bulunamadi: {mfile}")); return core.EX_NOINPUT
        m = rx.load_metrics_csv(mp); k = rp.compute(m)
        core.emit([{"metrik": kk, "deger": vv} for kk, vv in k.items()], fmt=fmt,
                  title="Rapor — blended KPI", columns=["metrik", "deger"])
        trig = rx.evaluate({**m, **k})
        if trig and fmt == "table":
            print(); core.emit(trig, fmt="table", title="Otomatik oneriler", columns=["oncelik", "id", "aksiyon"])
        return core.EX_OK
    out = Path(_opt(args, "--out", str(OUT))); n = rp.write_template(out / "metrics.csv")
    if fmt == "json":
        print(json.dumps({"out": str(out / "metrics.csv"), "fields": n}, ensure_ascii=False)); return core.EX_OK
    print(core.green(f"OK Metrik sablonu: {out / 'metrics.csv'} ({n} alan)"))
    print(core.dim("  Doldur -> kads report --metrics metrics.csv  -  Pano: dashboard/rapor.html"))
    return core.EX_OK



# ---- golive (fazli yayina alma kapisi) --------------------------------------
def cmd_golive(args):
    env = core.load_env(); fmt = _fmt(args)
    def ok(b): return "OK" if b else "EKSIK"
    g_id = "".join(c for c in env.get("GOOGLE_ADS_CUSTOMER_ID", "") if c.isdigit())
    meta_acc = env.get("META_AD_ACCOUNT_ID", "")
    dev = env.get("GOOGLE_ADS_DEVELOPER_TOKEN", "")
    gtm = env.get("GTM_CONTAINER_ID", "")
    writes = env.get("ADS_WRITES_ENABLED", "false").lower() == "true"
    rows = [
        {"faz": "1 Okuma", "kapi": "Google read MCP env (token/project/oauth)",
         "durum": ok(dev and not core.is_placeholder(dev)), "tip": "otomatik"},
        {"faz": "1 Okuma", "kapi": "Meta connector (Claude.ai web) eklendi", "durum": "MANUEL", "tip": "manuel"},
        {"faz": "1 Okuma", "kapi": "Hesap ID: Meta act_ + Google 10 hane",
         "durum": ok(meta_acc.startswith("act_") and not core.is_placeholder(meta_acc) and len(g_id) == 10), "tip": "otomatik"},
        {"faz": "2 Olcum", "kapi": "GTM container secildi (docs/02)",
         "durum": ok(bool(gtm) and not core.is_placeholder(gtm)), "tip": "otomatik"},
        {"faz": "2 Olcum", "kapi": "GA4 cross-domain + Consent v2 + Pixel/CAPI", "durum": "MANUEL", "tip": "manuel"},
        {"faz": "2 Olcum", "kapi": "HMS onay sayfasi dogrulandi (fixes/05)", "durum": "MANUEL", "tip": "manuel"},
        {"faz": "2 Olcum", "kapi": "TEST REZERVASYONU dedup purchase (GA4+Meta)", "durum": "MANUEL", "tip": "manuel"},
        {"faz": "3 Yazma", "kapi": "Allowlist dolu (act_ + 10 hane)",
         "durum": ok(meta_acc.startswith("act_") and len(g_id) == 10), "tip": "otomatik"},
        {"faz": "3 Yazma", "kapi": "ADS_WRITES_ENABLED + write_guardrails (olcum SONRASI)",
         "durum": ("ACIK" if writes else "kapali (guvenli)"), "tip": "otomatik"},
        {"faz": "3 Yazma", "kapi": "Kampanyalar PAUSED import + guard ile ENABLE", "durum": "MANUEL", "tip": "manuel"},
    ]
    if fmt == "table":
        core.banner("kads golive — fazli yayina alma kapisi")
    core.emit(rows, fmt=fmt, columns=["faz", "kapi", "durum", "tip"])
    if fmt == "table":
        auto_missing = [r for r in rows if r["tip"] == "otomatik" and r["durum"] == "EKSIK"]
        print()
        print(core.yellow(f"  {len(auto_missing)} otomatik kapi eksik (kads doctor + .env).") if auto_missing
              else core.green("  Otomatik kapilar tamam; manuel kapilari (olcum) bitir."))
        print(core.dim("  Kural: olcum test rezervasyonuyla dogrulanmadan ENABLE yok (docs/03)."))
    return core.EX_OK



# ---- competitors -------------------------------------------------------------
def cmd_competitors(args):
    core.emit(dx.COMPETITORS, fmt=_fmt(args), title="Rakip izleme (Foca/Eski Foca)",
              columns=["rakip", "konum", "vurgu", "karsi_mesaj", "izle"])
    if _fmt(args) == "table":
        print(core.dim("\n  Sablon: competitors/izleme-sablonu.csv  -  Arac: /spy (docs/11) - kads ile haftalik."))
    return core.EX_OK


# ---- calendar ----------------------------------------------------------------
def cmd_calendar(args):
    fmt = _fmt(args)
    try: days = int(_opt(args, "--days", "30"))
    except ValueError: days = 30
    rows = calx.generate(days=days)
    outopt = _opt(args, "--out")
    if outopt:
        n = calx.write_csv(Path(outopt) / "icerik-takvimi.csv", rows)
        print(core.green(f"OK Takvim: {Path(outopt) / 'icerik-takvimi.csv'} ({n} post / {days} gun)"))
        return core.EX_OK
    core.emit(rows[:20], fmt=fmt, title=f"Icerik takvimi ({len(rows)} post / {days} gun) - ilk 20",
              columns=["tarih", "gün", "saat", "kanal", "konsept", "format"])
    if fmt == "table":
        print(core.dim("\n  Tamami CSV: kads calendar --out content/takvim  -  Yayinla: kads publish"))
    return core.EX_OK


# ---- publish (Postiz-hazir) --------------------------------------------------
def cmd_publish(args):
    try: days = int(_opt(args, "--days", "30"))
    except ValueError: days = 30
    out = Path(_opt(args, "--out", str(OUT)))
    n = pubx.write_csv(out / "postiz-takvim.csv", days=days)
    csv_path = str(out / "postiz-takvim.csv")
    if _fmt(args) == "json":
        print(json.dumps({"out": csv_path, "posts": n}, ensure_ascii=False)); return core.EX_OK
    core.banner("kads publish - otomatik publisher (Postiz)")
    print(core.green(f"OK Postiz-hazir CSV: {csv_path} ({n} post)"))
    print(core.dim("  Postiz (gitroomhq/postiz-app, self-host UCRETSIZ): IG/FB/TikTok/LinkedIn/X + 20 kanal."))
    print(core.dim("  Bagla: Cowork Postiz eklentisi veya self-host -> kanallari ekle -> CSV/n8n ile zamanla (publishing/)."))
    return core.EX_OK


# ---- setup -------------------------------------------------------------------
def cmd_setup(args):
    fmt = _fmt(args)
    if fmt == "table":
        core.banner("kads setup - kurulum asistani")
    made = []
    if not (ROOT / ".env").exists() and (ROOT / ".env.example").exists():
        shutil.copy(ROOT / ".env.example", ROOT / ".env"); made.append(".env (ornekten)")
    if not (ROOT / ".mcp.json").exists() and (ROOT / ".mcp.json.example").exists():
        shutil.copy(ROOT / ".mcp.json.example", ROOT / ".mcp.json"); made.append(".mcp.json (ornekten)")
    env = core.load_env()
    todo = []
    for k in ("GTM_CONTAINER_ID", "META_AD_ACCOUNT_ID", "GOOGLE_ADS_CUSTOMER_ID",
              "GOOGLE_PROJECT_ID", "GOOGLE_ADS_DEVELOPER_TOKEN"):
        if core.is_placeholder(env.get(k, "")):
            todo.append(k)
    if fmt != "table":
        core.emit([{"doldurulacak": k} for k in todo], fmt=fmt, columns=["doldurulacak"])
        return core.EX_OK
    for m in made:
        print(core.green(f"  + olusturuldu: {m}"))
    if not made:
        print(core.dim("  .env ve .mcp.json zaten var (uzerine yazilmadi)."))
    print()
    core.emit([{"doldurulacak": k} for k in todo] or [{"doldurulacak": "(hepsi dolu)"}],
              fmt="table", title=".env doldurulacaklar", columns=["doldurulacak"])
    print(core.dim("\n  Sonra: kads doctor (denetim) - kads golive (yayina alma kapisi) - docs/13"))
    return core.EX_OK



# ---- status (sistem ozeti capstone) -----------------------------------------
def cmd_status(args):
    fmt = _fmt(args)
    packs = [
        ("Reklam kampanyalari", "campaigns"), ("Denetim duzeltmeleri", "fixes"),
        ("Profil kiti (GBP/OTA/sosyal)", "profiles"), ("Rakip izleme", "competitors"),
        ("Otomatik yayin (Postiz)", "publishing"), ("Kreatif + storyboard", "creatives"),
        ("Olcum implementasyonu", "tracking/implementation"), ("Icerik + takvim", "content"),
        ("WhatsApp sablonlari", "whatsapp"), ("Yayina alma runbook", "golive"),
        ("Web veri (Apify)", "apify"), ("AEO/GEO sema", "aeo"),
        ("E-posta", "email"), ("Landing A/B", "landing"),
        ("Influencer/PR", "outreach"), ("İtibar/kriz", "reputation"), ("Finans modeli", "finance"), ("Frontend (web)", "web"), ("B2B kurumsal", "b2b"),
        ("Attribution modeli", "attribution"), ("Donusum olcum", "conversions"), ("Dokumanlar", "docs"), ("Panolar", "dashboard"),
    ]
    rows = []
    for name, rel in packs:
        d = ROOT / rel
        n = sum(1 for _ in d.rglob("*") if _.is_file()) if d.exists() else 0
        rows.append({"paket": name, "yol": rel, "dosya": n, "durum": "OK" if n else "yok"})
    env = core.load_env()
    missing = [k for k in ("GTM_CONTAINER_ID", "META_AD_ACCOUNT_ID", "GOOGLE_ADS_CUSTOMER_ID",
               "GOOGLE_PROJECT_ID", "GOOGLE_ADS_DEVELOPER_TOKEN") if core.is_placeholder(env.get(k, ""))]
    if fmt == "table":
        core.banner(f"kads status v{VERSION} - {data.HOTEL['name']}")
        print(core.dim(f"  Komut: 40 - Test: pytest - Repo: github.com/No3214/ADS\n"))
    core.emit(rows, fmt=fmt, columns=["paket", "yol", "dosya", "durum"])
    if fmt == "table":
        print()
        if missing:
            print(core.yellow(f"  Kimlik eksik ({len(missing)}): {', '.join(missing)}"))
            print(core.dim("  Sonraki: kads setup -> .env doldur -> kads golive -> olcum -> kads build all"))
        else:
            print(core.green("  Kimlikler dolu. Sonraki: olcum dogrula (golive Faz 2) -> kads build all."))
    return core.EX_OK



# ---- apify (web veri actor receteleri) --------------------------------------
def cmd_apify(args):
    core.emit(dx.APIFY_ACTORS, fmt=_fmt(args), title="Apify actor receteleri (free-tier)",
              columns=["gorev", "actor", "girdi", "maliyet"])
    if _fmt(args) == "table":
        print(core.dim("\n  MCP akisi: search-actors -> fetch-actor-details -> call-actor -> get-dataset-items."))
        print(core.dim("  Receteler + canli URL listesi: apify/actor-recipes.md  -  Plan: apify/monitoring-plan.md"))
    return core.EX_OK



# ---- aeo (AI motoru gorunurlugu) --------------------------------------------
def cmd_aeo(args):
    sub = args[0] if args and not args[0].startswith("-") else "all"
    fmt = _fmt(args)
    if sub in ("schema", "sema"):
        core.emit(dx.AEO_SCHEMA_CHECKLIST, fmt=fmt, title="JSON-LD sema kontrol listesi (aeo/schema)",
                  columns=["sema", "sayfa", "dosya"])
        if fmt == "table":
            print(core.dim("\n  Dogrula: Google Rich Results Test + Schema Markup Validator. SAHTE puan/fiyat YOK."))
        return core.EX_OK
    if fmt == "table":
        core.banner("kads aeo - AI motoru gorunurlugu (AEO/GEO)")
        print(core.dim("  En kritik is: JSON-LD sema katmani (aeo/schema). Garanti yok; olasilik artar.\n"))
    core.emit(dx.AEO_CLUSTERS, fmt=fmt, title="Soru kumeleri (niyet -> sayfa)",
              columns=["kume", "ornek", "hedef"])
    if fmt == "table":
        print(core.dim("\n  Sema listesi: kads aeo schema  -  Paket: aeo/ (robots/llms/hreflang/olcum/plan)"))
    return core.EX_OK



# ---- season / funnel / offers -----------------------------------------------
def cmd_season(args):
    fmt = _fmt(args)
    sub = args[0] if args and not args[0].startswith("-") else ""
    if sub in ("detail", "detay"):
        core.emit(dg.SEASON_DETAIL, fmt=fmt, title="Sezon strateji detayi",
                  columns=["sezon", "aylar", "butce_vurgu", "kanal_mix", "kreatif_aci", "kelime_vurgu", "teklif", "kpi", "b2b"])
        if fmt == "table":
            print(core.dim("\n  Ozet: kads season  -  Butce: kads allocate  -  Detay: docs/19"))
        return core.EX_OK
    core.emit(dx.SEASONS, fmt=fmt, title="Sezon kampanya planlari",
              columns=["sezon", "tema", "kanal", "butce", "teklif", "kpi"])
    if fmt == "table":
        print(core.dim("\n  Detay: kads season detail / docs/19  -  Teklifler: kads offers  -  Takvim: kads calendar"))
    return core.EX_OK


def cmd_funnel(args):
    core.emit(dx.FUNNEL_STAGES, fmt=_fmt(args), title="Donusum hunisi (funnel)",
              columns=["asama", "kanal", "kpi", "kayip", "fix"])
    if _fmt(args) == "table":
        print(core.dim("\n  Tikanma teshisi + tablo: docs/16  -  Olc: kads report / rules"))
    return core.EX_OK


def cmd_offers(args):
    core.emit(dx.OFFERS, fmt=_fmt(args), title="Teklif / paket sablonlari",
              columns=["teklif", "kosul", "mesaj", "kanal"])
    return core.EX_OK



# ---- web (frontend kontrol listesi) -----------------------------------------
def cmd_web(args):
    core.emit(dx.WEB_CHECKLIST, fmt=_fmt(args), title="Frontend (web/) kontrol listesi",
              columns=["alan", "hedef", "kaynak"])
    if _fmt(args) == "table":
        print(core.dim("\n  Drop-in kod: web/  -  Dogrula: Lighthouse (mobil) + axe + gercek cihaz."))
    return core.EX_OK



# ---- b2b (kurumsal Aliağa) ---------------------------------------------------
def cmd_b2b(args):
    sub = args[0] if args and not args[0].startswith("-") else "targets"
    fmt = _fmt(args)
    if sub in ("packages", "paket", "mice"):
        core.emit(dx.B2B_PACKAGES, fmt=fmt, title="B2B / MICE paketleri", columns=["paket", "icerik", "hedef"])
        return core.EX_OK
    if fmt == "table":
        core.banner("kads b2b - kurumsal motor (Aliağa sanayi)")
        print(core.dim(f"  {dx.B2B_LOCATION}\n"))
    core.emit(dx.B2B_TARGETS, fmt=fmt, title="Hedef sektör / çapa firmalar",
              columns=["sektor", "cap_firma", "kullanim", "oncelik"])
    if fmt == "table":
        print(core.dim("\n  Paketler: kads b2b packages  -  Detay: b2b/ (rate card, outreach, hesap CSV, prospecting)"))
    return core.EX_OK


# ---- buyume: PMax / Demand Gen / Google remarketing -------------------------
def cmd_pmax(args):
    fmt = _fmt(args)
    sub = args[0] if args and not args[0].startswith("-") else "groups"
    if sub in ("specs", "spec", "varlik"):
        core.emit(dg.PMAX_ASSET_SPECS, fmt=fmt, title="PMax varlik (asset) limitleri",
                  columns=["varlik", "adet", "limit", "not"])
        return core.EX_OK
    if sub in ("setup", "kurulum"):
        core.emit(dg.PMAX_SETUP, fmt=fmt, title="PMax kurulum adimlari",
                  columns=["adim", "is", "detay"])
        return core.EX_OK
    if fmt == "table":
        core.banner("kads pmax - Performance Max (tum Google envanteri)")
    core.emit(dg.PMAX_ASSET_GROUPS, fmt=fmt, title="PMax asset group'lari",
              columns=["grup", "tema", "final_url", "tema_kitle_sinyali", "oncelik"])
    if fmt == "table":
        print(core.dim("\n  " + dg.PMAX_NOTE))
        print(core.dim("  Varliklar: kads pmax specs  -  Kurulum: kads pmax setup  -  Asset: campaigns/google-pmax/"))
    return core.EX_OK


def cmd_demandgen(args):
    fmt = _fmt(args)
    sub = args[0] if args and not args[0].startswith("-") else "formats"
    if sub in ("audiences", "kitle"):
        core.emit(dg.DEMAND_GEN_AUDIENCES, fmt=fmt, title="Demand Gen kitleleri",
                  columns=["kitle", "kaynak", "huni", "not"])
        return core.EX_OK
    if sub in ("specs", "spec", "varlik"):
        core.emit(dg.DEMAND_GEN_SPECS, fmt=fmt, title="Demand Gen varlik specs",
                  columns=["varlik", "limit", "adet", "not"])
        return core.EX_OK
    if fmt == "table":
        core.banner("kads demandgen - Demand Gen (YouTube + Discover + Gmail)")
    core.emit(dg.DEMAND_GEN_FORMATS, fmt=fmt, title="Demand Gen formatlari",
              columns=["format", "oran", "yerlesim", "kullanim"])
    if fmt == "table":
        print(core.dim("\n  " + dg.DEMAND_GEN_NOTE))
        print(core.dim("  Kitleler: kads demandgen audiences  -  Varlik: kads demandgen specs  -  campaigns/google-demandgen/"))
    return core.EX_OK


def cmd_remarketing(args):
    fmt = _fmt(args)
    sub = args[0] if args and not args[0].startswith("-") else "lists"
    if sub in ("rlsa",):
        core.emit(dg.RLSA_RULES, fmt=fmt, title="RLSA kurallari (Search + liste)",
                  columns=["senaryo", "aksiyon", "neden"])
        return core.EX_OK
    if sub in ("flow", "akis"):
        core.emit(dg.REMARKETING_FLOW, fmt=fmt, title="Kanal arasi remarketing akisi",
                  columns=["tetik", "1_kanal", "2_kanal", "mesaj"])
        return core.EX_OK
    if fmt == "table":
        core.banner("kads remarketing - Google geri kazanim (Meta'yi tamamlar)")
    core.emit(dg.GOOGLE_REMARKETING, fmt=fmt, title="Google remarketing listeleri",
              columns=["liste", "uyelik_gun", "min_boyut", "kullanim", "oncelik"])
    if fmt == "table":
        print(core.dim("\n  " + dg.GOOGLE_REMARKETING_NOTE))
        print(core.dim("  RLSA: kads remarketing rlsa  -  Akis: kads remarketing flow  -  campaigns/remarketing/"))
    return core.EX_OK


# ---- buyume: UTM standardi/builder + attribution ----------------------------
def cmd_utm(args):
    fmt = _fmt(args)
    sub = args[0] if args and not args[0].startswith("-") else "matrix"
    if sub == "build":
        from urllib.parse import urlencode, urlparse
        url = _opt(args, "--url", "")
        ch = _opt(args, "--channel", "")
        if ch:
            preset = next((r for r in dg.UTM_MATRIX if r["anahtar"] == ch), None)
            if not preset:
                print(core.red("Bilinmeyen kanal: " + ch + "  (liste: kads utm)"))
                return core.EX_USAGE
            src, med, camp = preset["utm_source"], preset["utm_medium"], preset["utm_campaign"]
        else:
            src, med, camp = _opt(args, "--source", ""), _opt(args, "--medium", ""), _opt(args, "--campaign", "")
        term, content = _opt(args, "--term", ""), _opt(args, "--content", "")
        if not url or not (src and med and camp):
            print(core.red("Kullanim: kads utm build --url URL (--channel ANAHTAR | --source S --medium M --campaign C) [--term T --content C]"))
            return core.EX_USAGE
        params = [("utm_source", src), ("utm_medium", med), ("utm_campaign", camp)]
        if term:
            params.append(("utm_term", term))
        if content:
            params.append(("utm_content", content))
        sep = "&" if urlparse(url).query else "?"
        built = url + sep + urlencode(params)
        if fmt == "json":
            print(json.dumps({"url": built, **dict(params)}, ensure_ascii=False, indent=2))
        else:
            print(built)
        return core.EX_OK
    if sub in ("rules", "kural"):
        core.emit(dg.UTM_RULES, fmt=fmt, title="UTM kurallari", columns=["kural", "ornek", "neden"])
        return core.EX_OK
    core.emit(dg.UTM_MATRIX, fmt=fmt, title="UTM standardi (kanal -> source/medium/campaign)",
              columns=["anahtar", "kanal", "utm_source", "utm_medium", "utm_campaign", "not"])
    if fmt == "table":
        print(core.dim("\n  Uret: kads utm build --url https://www.kozbeylikonagi.com/odalar --channel google-pmax"))
        print(core.dim("  Kurallar: kads utm rules  -  Detay: tracking/utm-standard.md"))
    return core.EX_OK


def cmd_attribution(args):
    fmt = _fmt(args)
    core.emit(dg.ATTRIBUTION, fmt=fmt, title="Attribution modeli (katman -> model)",
              columns=["katman", "model", "pencere", "not"])
    if fmt == "table":
        print("")
        for n in dg.ATTRIBUTION_NOTES:
            print(core.dim("  - " + n))
        print(core.dim("\n  Olcum kurulumu: tracking/  -  Cross-domain: tracking/implementation/03-ga4-cross-domain.md"))
    return core.EX_OK


# ---- buyume: butce dagitim matrisi ------------------------------------------
def cmd_allocate(args):
    fmt = _fmt(args)
    sub = args[0] if args and not args[0].startswith("-") else "channels"
    if sub in ("funnel", "huni"):
        core.emit(dg.BUDGET_BY_FUNNEL, fmt=fmt, title="Butce — huni asamasina gore (ay2+, 30.000 TL)",
                  columns=["asama", "kanallar", "ay2_try", "pct", "amac"])
        return core.EX_OK
    if sub in ("rules", "kural"):
        core.emit(dg.BUDGET_REALLOCATION_RULES, fmt=fmt, title="Butce yeniden dagitim kurallari",
                  columns=["tetik", "esik", "aksiyon", "kaynak"])
        return core.EX_OK
    if fmt == "table":
        core.banner("kads allocate - butce dagitim matrisi (30.000 TL/ay)")
    core.emit(dg.BUDGET_MATRIX, fmt=fmt, title="Kanal x huni x ay (TRY)",
              columns=["kanal", "huni", "ay1_try", "ay1_pct", "ay2_try", "ay2_pct", "gerekce"])
    if fmt == "table":
        a1 = sum(r["ay1_try"] for r in dg.BUDGET_MATRIX)
        a2 = sum(r["ay2_try"] for r in dg.BUDGET_MATRIX)
        print(core.dim("\n  Ay1 toplam: %s TL  -  Ay2+ toplam: %s TL  (hedef %s TL)" % (a1, a2, dg.BUDGET_TOTAL_TRY)))
        print(core.dim("  Huni: kads allocate funnel  -  Kurallar: kads allocate rules  -  Detay: docs/18"))
    return core.EX_OK


# ---- buyume: donusum olcum dongusu (online + offline/call) -------------------
def cmd_conversions(args):
    fmt = _fmt(args)
    sub = args[0] if args and not args[0].startswith("-") else "actions"
    if sub in ("offline", "oci"):
        combined = ([{"platform": "Google OCI", **r} for r in dg.OFFLINE_IMPORT_GOOGLE] +
                    [{"platform": "Meta CAPI", **r} for r in dg.OFFLINE_IMPORT_META])
        if fmt == "table":
            core.banner("kads conversions offline - telefon/WhatsApp rezervasyonu geri yukle")
        core.emit(combined, fmt=fmt, title="Offline import (Google OCI + Meta CAPI)",
                  columns=["platform", "adim", "is", "detay"])
        return core.EX_OK
    if sub in ("enhanced", "match"):
        core.emit(dg.ENHANCED_MATCHING, fmt=fmt, title="Enhanced Conversions / Advanced Matching",
                  columns=["platform", "ozellik", "veri", "not"])
        return core.EX_OK
    if sub in ("calls", "call"):
        core.emit(dg.CALL_TRACKING, fmt=fmt, title="Arama (call) takibi",
                  columns=["kaynak", "olcum", "esik", "not"])
        return core.EX_OK
    if fmt == "table":
        core.banner("kads conversions - donusum olcum dongusu")
    core.emit(dg.CONVERSION_ACTIONS, fmt=fmt, title="Donusum aksiyonlari (online + offline)",
              columns=["olay", "kaynak", "tip", "deger", "not"])
    if fmt == "table":
        print(core.dim("\n  " + dg.CONVERSION_NOTE))
        print(core.dim("  Offline: kads conversions offline  -  Enhanced: kads conversions enhanced  -  Aramalar: kads conversions calls"))
        print(core.dim("  Kurulum: conversions/  -  Altyapi: tracking/"))
    return core.EX_OK


# ---- selfcheck (kirilmaz / butunluk denetimi) -------------------------------
def cmd_selfcheck(args):
    import json as _json, glob as _glob, tempfile as _tmp
    fmt = _fmt(args); checks = []
    def add(name, ok, detail=""):
        checks.append({"kontrol": name, "sonuç": "GEÇTİ" if ok else "HATA", "detay": detail})
    # 1) RSA uzunluk + bütçe (validate ile aynı çekirdek)
    bad = _length_problems(); add("RSA uzunlukları (≤30/≤90)", not bad, f"{len(bad)} sorun")
    add("Bütçe tavanı = plan", data.BUDGET_CAPS["google_monthly_try"] == data.PLAN["google_monthly_try"])
    # 2) AEO JSON-LD + PWA manifest geçerli JSON
    jbad = 0
    for f in _glob.glob(str(ROOT / "aeo" / "schema" / "*.jsonld")) + [str(ROOT / "web" / "pwa" / "manifest.webmanifest")]:
        try: _json.load(open(f, encoding="utf-8"))
        except Exception: jbad += 1
    add("JSON-LD + manifest geçerli", jbad == 0, f"{jbad} bozuk")
    # 3) CSV üretimi (google+meta+seo)
    try:
        t = Path(_tmp.mkdtemp())
        n = sum(x for _, x in gx.build(t/"g")) + sum(x for _, x in mx.build(t/"m")) + sum(x for _, x in sx.build(t/"s"))
        add("Üretim (CSV/şema)", n > 100, f"{n} satır/öğe")
    except Exception as exc:  # noqa: BLE001
        add("Üretim", False, str(exc)[:40])
    # 4) Beklenen paketler mevcut
    packs = ["campaigns","fixes","profiles","competitors","publishing","creatives","tracking/implementation",
             "content","whatsapp","golive","aeo","email","landing","outreach","reputation","finance","web","b2b","apify","docs","attribution","conversions"]
    miss = [p for p in packs if not (ROOT / p).exists()]
    add("Paket bütünlüğü", not miss, f"eksik: {miss}" if miss else f"{len(packs)} paket")
    # 5) guardrails + bundle yedek
    add("guardrails.py", (ROOT/"scripts"/"guardrails.py").exists())
    add("Yedek (ADS.bundle)", (ROOT/"ADS.bundle").exists(), "git push.bat ile GitHub")
    ok = all(c["sonuç"] == "GEÇTİ" for c in checks)
    if fmt == "table":
        core.banner("kads selfcheck - sistem bütünlük denetimi")
    core.emit(checks, fmt=fmt, columns=["kontrol", "sonuç", "detay"])
    if fmt == "table":
        print((core.green("\n  ✓ Sistem sağlam.") if ok else core.red("\n  ✗ Sorun var — düzelt.")))
    return core.EX_OK if ok else core.EX_GENERIC


# ---- help / version --------------------------------------------------------
def cmd_help(args: list[str]) -> int:
    core.banner(f"kads {VERSION} — {data.HOTEL['name']} Reklam Operasyonları")
    cmds = [
        ("doctor", "Ortam + config + kanal teşhisi"),
        ("config", "Çözülmüş ayarlar (secret maskeli)"),
        ("plan", "30.000 TL çapraz kanal planı"),
        ("budget", "Bütçe dağılımı + tavanlar"),
        ("kpi [--revenue X --spend Y]", "Blended ROAS / rezervasyon matematiği"),
        ("keywords", "Google anahtar kelime setleri"),
        ("creative google|meta", "RSA / Meta reklam metinleri"),
        ("seo schema|gbp|local|brand", "Yerel SEO + Google İşletme Profili"),
        ("presence [fixes|props]", "Dijital varlık denetimi + düzeltmeler"),
        ("mcp", "Baglanti durumu (Google read / Meta connector)"),
        ("skills", "Meta reklam Claude skill paketi + kurulum"),
        ("audiences", "Retargeting / Lookalike kitleleri"),
        ("rules [--metrics f.csv]", "Butce/teklif optimizasyon kurallari"),
        ("report [--metrics f.csv]", "Blended KPI raporu / metrik sablonu"),
        ("golive", "Fazli yayina alma kapisi (hazirlik denetimi)"),
        ("competitors", "Rakip izleme listesi"),
        ("calendar [--days N --out DIR]", "Cok kanalli icerik takvimi"),
        ("publish [--days N --out DIR]", "Postiz-hazir yayin takvimi (oto publisher)"),
        ("setup", "Kurulum asistani (.env/.mcp.json)"),
        ("status", "Sistem ozeti (paketler + hazirlik)"),
        ("apify", "Web veri actor receteleri (yorum/fiyat/SERP)"),
        ("aeo [schema]", "AI motoru gorunurlugu: soru kumeleri + JSON-LD"),
        ("season / funnel / offers", "Sezon plani / donusum hunisi / teklifler"),
        ("web", "Frontend kontrol listesi (perf/a11y/PWA/meta)"),
        ("b2b [packages]", "Kurumsal motor (Aliağa sanayi) hedef + paket"),
        ("pmax [specs|setup]", "Performance Max asset group + varlik + kurulum"),
        ("demandgen [audiences|specs]", "Demand Gen format + kitle + varlik"),
        ("remarketing [rlsa|flow]", "Google remarketing liste + RLSA + kanal akisi"),
        ("utm [build|rules]", "UTM standardi + tutarli link uretici"),
        ("attribution", "Attribution modeli + cift sayim dedup"),
        ("allocate [funnel|rules]", "Butce dagitim matrisi (kanal x huni x ay)"),
        ("conversions [offline|enhanced|calls]", "Donusum olcum dongusu (online + offline/call import)"),
        ("selfcheck", "Sistem bütünlük denetimi (kırılmaz)"),
        ("build google|meta|seo|all [--out DIR]", "Import-hazır dosyalar üret"),
        ("validate", "RSA uzunluk + bütçe + CSV doğrulama"),
        ("guard --check change.json [--approval ...]", "Değişiklik guardrail kontrolü"),
        ("monitor", "Salt-okunur izleme yolu"),
        ("brief", "Haftalık brief şablonu"),
        ("version | help", ""),
    ]
    core.emit([{"komut": c, "açıklama": d} for c, d in cmds], fmt="table",
              columns=["komut", "açıklama"])
    print(core.dim("\n  Her komut: --format table|json|yaml|md|csv  •  Çıkış kodları: sysexits"))
    return core.EX_OK


def main(argv: list[str] | None = None) -> int:
    # Windows konsolu cp1254 (Turkce) olabilir; UTF-8'e zorla ki kutu-cizim ve
    # Turkce karakterler UnicodeEncodeError ile cokmesin (Linux/UTF-8'de no-op).
    for _s in (sys.stdout, sys.stderr):
        _enc = (getattr(_s, "encoding", "") or "").lower().replace("-", "")
        if _enc not in ("utf8", "utf8mb4", "cp65001"):
            try:
                _s.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("help", "-h", "--help"):
        return cmd_help(argv[1:] if argv else [])
    cmd, rest = argv[0], argv[1:]
    if cmd in ("version", "-v", "--version"):
        print(f"kads {VERSION}"); return core.EX_OK
    table = {
        "doctor": cmd_doctor, "config": cmd_config, "plan": cmd_plan, "budget": cmd_budget,
        "kpi": cmd_kpi, "keywords": cmd_keywords, "creative": cmd_creative, "build": cmd_build,
        "seo": cmd_seo, "presence": cmd_presence, "mcp": cmd_mcp, "skills": cmd_skills,
        "rules": cmd_rules, "audiences": cmd_audiences, "report": cmd_report, "golive": cmd_golive,
        "competitors": cmd_competitors, "calendar": cmd_calendar, "publish": cmd_publish, "setup": cmd_setup,
        "status": cmd_status, "apify": cmd_apify, "aeo": cmd_aeo,
        "season": cmd_season, "funnel": cmd_funnel, "offers": cmd_offers, "web": cmd_web,
        "b2b": cmd_b2b, "selfcheck": cmd_selfcheck,
        "pmax": cmd_pmax, "demandgen": cmd_demandgen, "remarketing": cmd_remarketing,
        "utm": cmd_utm, "attribution": cmd_attribution,
        "allocate": cmd_allocate,
        "conversions": cmd_conversions,
        "validate": cmd_validate, "guard": cmd_guard, "monitor": cmd_monitor, "brief": cmd_brief,
    }
    fn = table.get(cmd)
    if not fn:
        print(core.red(f"Bilinmeyen komut: {cmd}")); cmd_help([]); return core.EX_USAGE
    try:
        return fn(rest)
    except KeyboardInterrupt:
        return 130
    except BrokenPipeError:
        return core.EX_OK


if __name__ == "__main__":
    raise SystemExit(main())
