#!/usr/bin/env python3
"""
kads.platforms.meta — Meta (Instagram/Facebook) Ads Manager kurulum paketi.

Meta'da Google Ads Editor benzeri guvenilir bir CSV import yoktur; bu yuzden
modul, Ads Manager'da elle (veya resmi Meta connector ile) kurulum icin TAM
doldurulmus bir kurulum sayfasi (build sheet) + paste-hazir reklam metni CSV'si
uretir. Resmi connector: https://mcp.facebook.com/ads (29 arac, OAuth, acik beta).

Ciktilar (out/meta/):
  meta-kurulum-rehberi.md     Kampanya > ad set > reklam, her alan dolu
  meta-kampanyalar.csv        Kampanya/ad set ozet tablosu
  meta-reklam-metinleri.csv   Konsept bazinda primary text / headline / cta
"""
from __future__ import annotations

import csv
from pathlib import Path

from kads import data
from kads import data_ext as dx

# Faz bazinda kampanya yapisi (plan ile birebir)
PHASE1 = [
    {"campaign": "Kozbeyli | Prospecting | Website Sales", "objective": "Sales (Conversions)",
     "daily_try": 350, "monthly_try": 10500, "audience": "Prospecting",
     "optimize": "Purchase (güvenilirse) — değilse begin_checkout / Lead",
     "concepts": ["Konsept1-TasKonak", "Konsept2-Manzara", "Konsept3-Kahvalti", "Konsept4-Evcil"]},
    {"campaign": "Kozbeyli | WhatsApp | Mesaj", "objective": "Engagement (Messaging → WhatsApp)",
     "daily_try": 150, "monthly_try": 4500, "audience": "Prospecting",
     "optimize": "Conversations (mesaj başlatma)",
     "concepts": ["Konsept5-WhatsApp", "Konsept2-Manzara"]},
]
PHASE2 = [
    {"campaign": "Kozbeyli | Prospecting | Website Sales", "objective": "Sales (Conversions)",
     "daily_try": 300, "monthly_try": 9000, "audience": "Prospecting",
     "optimize": "Purchase", "concepts": ["Konsept1-TasKonak", "Konsept2-Manzara", "Konsept3-Kahvalti"]},
    {"campaign": "Kozbeyli | Retargeting | Website Sales", "objective": "Sales (Conversions)",
     "daily_try": 100, "monthly_try": 3000, "audience": "Retargeting",
     "optimize": "Purchase", "concepts": ["Konsept2-Manzara", "Konsept4-Evcil"]},
    {"campaign": "Kozbeyli | WhatsApp | Mesaj", "objective": "Engagement (Messaging → WhatsApp)",
     "daily_try": 100, "monthly_try": 3000, "audience": "Prospecting",
     "optimize": "Conversations", "concepts": ["Konsept5-WhatsApp"]},
]


def campaign_rows() -> list[dict]:
    rows = []
    for faz, items in (("Ay 1", PHASE1), ("Ay 2+", PHASE2)):
        for c in items:
            rows.append({
                "Faz": faz, "Kampanya": c["campaign"], "Amaç": c["objective"],
                "Günlük TRY": c["daily_try"], "Aylık TRY": c["monthly_try"],
                "Kitle": c["audience"], "Optimizasyon": c["optimize"],
                "Durum": "PAUSED", "Kreatifler": ", ".join(c["concepts"]),
            })
    return rows


def copy_rows() -> list[dict]:
    rows = []
    for key, c in data.META_COPY.items():
        for i, pt in enumerate(c["primary_text"], 1):
            rows.append({
                "Konsept": key, "Tema": c["tema"], "Varyant": i,
                "Primary Text": pt, "Headline": " / ".join(c["headlines"]),
                "Description": c["description"], "CTA": c["cta"], "Hedef": c["destination"],
            })
    return rows


def _audiences_md() -> str:
    out = ["## Kitleler\n"]
    for name, a in data.META_AUDIENCES.items():
        out.append(f"### {name}")
        for k, v in a.items():
            v = ", ".join(v) if isinstance(v, list) else v
            out.append(f"- **{k}:** {v}")
        out.append("")
    return "\n".join(out)


def build_sheet_md() -> str:
    h = data.HOTEL
    lines = [
        f"# Meta Ads Manager — Kurulum Rehberi ({h['name']})",
        "",
        "Bütçe: Meta 15.000 TL/ay. Tüm kampanyalar **PAUSED** kurulur. Website Sales",
        "yalnızca Pixel+CAPI'de `Purchase` güvenilirse açılır; değilse önce tracking +",
        "WhatsApp akışı çalışır, en derin güvenilir olaya (`begin_checkout`) optimize edilir.",
        "",
        "Kreatif oranları: Reels/Stories **9:16**, Feed **4:5**. Yerleşim: **Advantage+**",
        "(küçük bütçede manuel bölme yok). İlk ay **en fazla 2 kampanya**.",
        "",
        "Resmî yol: `https://mcp.facebook.com/ads` connector (OAuth) veya Ads Manager elle.",
        "",
    ]
    for faz, items in (("## Faz 1 — İlk 30 gün (2 kampanya)", PHASE1),
                       ("## Faz 2 — Ay 2+ (3 kampanya)", PHASE2)):
        lines.append(faz)
        lines.append("")
        for c in items:
            lines += [
                f"### {c['campaign']}",
                f"- **Amaç (Objective):** {c['objective']}",
                f"- **Bütçe:** {c['daily_try']} TL/gün ({c['monthly_try']} TL/ay) — CBO uygun",
                f"- **Durum:** PAUSED (review'dan sonra ENABLE)",
                f"- **Kitle:** {c['audience']} (detay aşağıda)",
                f"- **Optimizasyon olayı:** {c['optimize']}",
                f"- **Yerleşim:** Advantage+ (otomatik)",
                f"- **Kreatifler:** {', '.join(c['concepts'])}",
                "",
            ]
    lines.append(_audiences_md())
    lines += [
        "## Reklam metinleri",
        "Konsept bazında primary text / başlık / CTA için `meta-reklam-metinleri.csv`.",
        "",
        "## Kurulum sırası (Ads Manager)",
        "1. Pixel + CAPI doğrula (Test Events: Purchase / InitiateCheckout / Lead).",
        "2. Kampanya oluştur (amaç), bütçe gir, PAUSED bırak.",
        "3. Ad set: kitle + yerleşim (Advantage+) + optimizasyon olayı.",
        "4. Reklamlar: her konsept için 9:16 + 4:5 kreatif, metni CSV'den yapıştır.",
        "5. Review → ölçüm doğrulanınca ENABLE (ikinci onay: `kads guard`).",
        "",
        "## KPI",
        f"- {data.KPI['whatsapp_formula']}",
        f"- Örnek: {data.KPI['ornek']}",
        f"- {data.KPI['blended_note']}",
    ]
    return "\n".join(lines)


def _write_csv(path: Path, rows: list[dict]) -> int:
    if not rows:
        return 0
    cols = list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return len(rows)



def placement_rows() -> list[dict]:
    rows = []
    for pl, spec in dx.META_PLACEMENT_SPECS.items():
        rows.append({"Yerleşim": pl, "Oran": spec["ratio"], "Çözünürlük": spec["px"],
                     "Medya": spec.get("media", ""),
                     "Süre/Limit": spec.get("duration", spec.get("primary_text_max", "")),
                     "Not": spec["note"]})
    return rows


def audiences_rows() -> list[dict]:
    return [{"Kitle": a["ad"], "Tip": a["tip"], "Kaynak": a["kaynak"],
             "Pencere": a["pencere"], "Kullanim": a["kullanim"]}
            for a in dx.RETARGETING_AUDIENCES]


def copy_ab_rows() -> list[dict]:
    """Her konsept için 3 reklam varyantı (A/B/C hook)."""
    rows = []
    for key, c in data.META_COPY.items():
        base = c["primary_text"][0]
        for variant, hook in dx.META_AB_HOOKS.items():
            rows.append({"Konsept": key, "Tema": c["tema"], "Varyant": variant,
                         "Hook": hook, "Primary Text": f"{hook} {base}",
                         "Headline": c["headlines"][0], "CTA": c["cta"]})
    return rows


def build(out_dir: Path) -> list[tuple[str, int]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "meta-kurulum-rehberi.md").write_text(build_sheet_md(), encoding="utf-8")
    res = [
        ("meta-kurulum-rehberi.md", build_sheet_md().count("\n") + 1),
        ("meta-kampanyalar.csv", _write_csv(out_dir / "meta-kampanyalar.csv", campaign_rows())),
        ("meta-reklam-metinleri.csv", _write_csv(out_dir / "meta-reklam-metinleri.csv", copy_rows())),
        ("meta-yerlesim-sablonlari.csv", _write_csv(out_dir / "meta-yerlesim-sablonlari.csv", placement_rows())),
        ("meta-reklam-ab-varyantlari.csv", _write_csv(out_dir / "meta-reklam-ab-varyantlari.csv", copy_ab_rows())),
        ("meta-retargeting-kitleleri.csv", _write_csv(out_dir / "meta-retargeting-kitleleri.csv", audiences_rows())),
    ]
    return res
