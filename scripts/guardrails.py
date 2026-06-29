#!/usr/bin/env python3
"""
Kozbeyli Konağı — Reklam değişiklik güvenlik korkulukları (code-level guardrails)

Amaç: Claude tam otonom çalışırken bile, para harcayan/riskli işlemleri PROMPT
seviyesinde değil KOD seviyesinde denetlemek. Prompt'a "önce onay al" yazmak
yeterli değildir; bir talimat enjeksiyonu prompt kuralını atlayabilir. Bu dosya
her mutation'ı bağımsız olarak doğrular ve denetim kaydı (audit log) yazar.

Kullanım (Claude değişiklik skill'i tarafından çağrılır):
    python3 scripts/guardrails.py --check change.json
    python3 scripts/guardrails.py --check change.json --approval "ONAYLA | meta | act_123 | create_campaign | 350"

change.json örneği:
    {
      "platform": "google",                 # google | meta
      "account_id": "123-456-7890",         # allowlist'te olmalı
      "action": "create_campaign",          # izinli aksiyon olmalı
      "entity": "campaign",
      "status": "PAUSED",                    # yeni kampanya PAUSED olmalı
      "daily_budget_try": 296,               # günlük tavan altında olmalı
      "monthly_budget_try": 9000,            # aylık tavan altında olmalı
      "old_value": null,
      "new_value": {"name": "Marka - Search", "status": "PAUSED"}
    }

Çıkış kodu: 0 = izinli (ALLOW), 1 = reddedildi (DENY), 2 = onay bekliyor (NEEDS_APPROVAL).
Hiçbir koşulda gerçek API çağrısı YAPMAZ; yalnızca karar verir ve loglar.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
from kads import core

LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "ads-change-audit.jsonl"

# ---- Sabit politika (config dosyası kaybolsa bile güvenli varsayılan) --------
HARD_BLOCKED_ACTIONS = {
    "delete",
    "remove",
    "delete_campaign",
    "delete_adset",
    "delete_ad",
    "update_billing",
    "change_billing",
    "add_payment_method",
    "update_payment",
    "add_user",
    "remove_user",
    "update_user",
    "manage_users",
    "upload_customer_list",
    "upload_user_list",
    "create_customer_match",
}
# ENABLED'a geçiren aksiyonlar ikinci, ayrı bir onay ister.
ENABLE_ACTIONS = {"enable", "resume", "activate", "set_enabled", "unpause"}
# İzin verilen mutation aksiyonları (allowlist mantığı: listede yoksa reddet).
ALLOWED_ACTIONS = {
    "create_campaign",
    "create_ad_group",
    "create_adset",
    "create_ad",
    "create_keyword",
    "create_criteria",
    "create_budget",
    "update_budget",
    "update_bid",
    "update_targeting",
    "update_schedule",
    "pause",
    "pause_campaign",
    "pause_adset",
    "pause_ad",
} | ENABLE_ACTIONS


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).astimezone().isoformat()


def _digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def load_config() -> dict:
    """ads-assets.yaml'i bağımlılıksız (mini parser) okur; yalnızca ihtiyaç
    duyulan alanları çeker. PyYAML kurulu değilse de çalışır."""
    env = core.load_env()
    cfg = {
        "google_monthly_try": float(env.get("GOOGLE_MONTHLY_BUDGET_TRY", "15000")),
        "meta_monthly_try": float(env.get("META_MONTHLY_BUDGET_TRY", "15000")),
        "google_daily_try": float(env.get("GOOGLE_AVG_DAILY_BUDGET_TRY", "493")),
        "meta_daily_try": float(env.get("META_DAILY_BUDGET_TRY", "500")),
        "writes_enabled": env.get("ADS_WRITES_ENABLED", "false").lower() == "true",
        "google_allowlist": set(),
        "meta_allowlist": set(),
    }
    # Allowlist'i .env'den oku (virgül ile ayrılmış). Boşsa config'ten doldurulur.
    g = _digits(env.get("GOOGLE_ADS_CUSTOMER_ID", ""))
    if len(g) == 10:
        cfg["google_allowlist"].add(g)
    m = env.get("META_AD_ACCOUNT_ID", "").strip()
    if re.fullmatch(r"act_\d+", m):
        cfg["meta_allowlist"].add(m)

    # ads-assets.yaml içindeki ek allowlist satırlarını da tara (opsiyonel).
    yaml_path = ROOT / "config" / "ads-assets.yaml"
    if yaml_path.exists():
        text = yaml_path.read_text(encoding="utf-8", errors="ignore")
        for acc in re.findall(r"act_\d+", text):
            cfg["meta_allowlist"].add(acc)
        for cid in re.findall(r"\b(\d{3}-\d{3}-\d{4})\b", text):
            cfg["google_allowlist"].add(_digits(cid))
        # write_guardrails.enabled: true/false
        m2 = re.search(r"write_guardrails:\s*\n\s*enabled:\s*(true|false)", text)
        if m2:
            cfg["writes_enabled"] = cfg["writes_enabled"] and (m2.group(1) == "true")
    return cfg


def evaluate(change: dict, cfg: dict, approval: str | None) -> tuple[str, list[str]]:
    """Bir değişikliği değerlendirir. (decision, reasons) döndürür.
    decision in {ALLOW, DENY, NEEDS_APPROVAL}."""
    reasons: list[str] = []
    platform = (change.get("platform") or "").lower()
    action = (change.get("action") or "").lower()
    account = (change.get("account_id") or "").strip()
    status = (change.get("status") or "").upper()
    daily = change.get("daily_budget_try")
    monthly = change.get("monthly_budget_try")

    # 0) Global yazma kapısı
    if not cfg["writes_enabled"]:
        reasons.append("Gerçek yazma kapalı (ADS_WRITES_ENABLED!=true veya write_guardrails.enabled!=true). Yalnızca dry-run/önizleme.")
        return "DENY", reasons

    # 1) Platform
    if platform not in {"google", "meta"}:
        reasons.append(f"Bilinmeyen platform: '{platform}'. google veya meta olmalı.")
        return "DENY", reasons

    # 2) Sert engelli aksiyonlar (asla)
    if action in HARD_BLOCKED_ACTIONS:
        reasons.append(f"Aksiyon kalıcı olarak engellendi: '{action}' (silme/ödeme/kullanıcı/liste yükleme yok).")
        return "DENY", reasons

    # 3) Aksiyon allowlist
    if action not in ALLOWED_ACTIONS:
        reasons.append(f"Aksiyon izinli listede değil: '{action}'.")
        return "DENY", reasons

    # 4) Hesap allowlist
    if platform == "google":
        allow = cfg["google_allowlist"]
        acc_key = _digits(account)
        if not allow:
            reasons.append("Google hesap allowlist boş. GOOGLE_ADS_CUSTOMER_ID (10 hane) tanımlayın.")
            return "DENY", reasons
        if acc_key not in allow:
            reasons.append(f"Google hesabı allowlist dışında: '{account}'. İzinli: {sorted(allow)}")
            return "DENY", reasons
    else:  # meta
        allow = cfg["meta_allowlist"]
        if not allow:
            reasons.append("Meta hesap allowlist boş. META_AD_ACCOUNT_ID (act_...) tanımlayın.")
            return "DENY", reasons
        if account not in allow:
            reasons.append(f"Meta hesabı allowlist dışında: '{account}'. İzinli: {sorted(allow)}")
            return "DENY", reasons

    # 5) Yeni kampanya/adset/adgroup/ad PAUSED olmalı.
    # GUVENLIK: status alani BOS/eksik gelirse de reddet (bypass yok). Aksiyon
    # adindan da yakala ki entity atlanirsa bile kampanya create PAUSED zorunlu olsun.
    _status_creates = {"create_campaign", "create_adset", "create_ad_group", "create_ad"}
    creates_entity = action in _status_creates or (
        action.startswith("create") and change.get("entity") in {"campaign", "adset", "ad_group", "ad"})
    if creates_entity and status != "PAUSED":
        reasons.append(f"Yeni varlik PAUSED olusturulmali; gelen status='{status or '(yok)'}'.")
        return "DENY", reasons

    # 6) Bütçe tavanları
    daily_cap = cfg["google_daily_try"] if platform == "google" else cfg["meta_daily_try"]
    monthly_cap = cfg["google_monthly_try"] if platform == "google" else cfg["meta_monthly_try"]
    if daily is not None:
        try:
            if float(daily) > float(daily_cap):
                reasons.append(f"Günlük bütçe tavanı aşıldı: {daily} > {daily_cap} TL ({platform}).")
                return "DENY", reasons
        except (TypeError, ValueError):
            reasons.append(f"Geçersiz daily_budget_try: {daily!r}")
            return "DENY", reasons
    if monthly is not None:
        try:
            if float(monthly) > float(monthly_cap):
                reasons.append(f"Aylık bütçe tavanı aşıldı: {monthly} > {monthly_cap} TL ({platform}).")
                return "DENY", reasons
        except (TypeError, ValueError):
            reasons.append(f"Geçersiz monthly_budget_try: {monthly!r}")
            return "DENY", reasons

    # 7) Onay kapısı: her mutation açık onay ister; ENABLE ikinci/ayrı onay ister.
    needs = _approval_matches(approval, platform, account, action, daily)
    if action in ENABLE_ACTIONS:
        # ENABLE için onay metni AYRI bir ikinci-onay işaretçisi taşımalı:
        # baş token 'ONAYLA-2'/'APPROVE-2' OLMALI ya da 'ETKINLESTIR/ETKİNLEŞTİR'
        # kelimesi geçmeli. (Aksiyon adı 'enable' tek başına yeterli sayılmaz.)
        head = re.split(r"[|;]", (approval or ""))[0].strip().lower()
        second_marker = head.startswith("onayla-2") or head.startswith("approve-2") \
            or re.search(r"etkinle\u015ftir|etkinlestir|i\u015fte etkinle", (approval or ""), re.I)
        if not (needs and second_marker):
            reasons.append(
                "ENABLED işlemi AYRI ikinci onay ister. Biçim: "
                "'ONAYLA-2 | platform | hesap | enable | <gunluk_butce>'."
            )
            return "NEEDS_APPROVAL", reasons
    if not needs:
        reasons.append("Açık onay gerekli. Biçim: 'ONAYLA | platform | hesap_id | aksiyon | gunluk_butce'.")
        return "NEEDS_APPROVAL", reasons

    reasons.append("Tüm korkuluklar geçildi: allowlist OK, PAUSED OK, bütçe OK, onay OK.")
    return "ALLOW", reasons


def _approval_matches(approval: str | None, platform: str, account: str, action: str, daily) -> bool:
    """Onay metni biçimi: 'ONAYLA | platform | hesap | aksiyon | gunluk_butce'
    (ENABLE için 'ONAYLA-2 | ...'). Alanlar eşleşmeli."""
    if not approval:
        return False
    parts = [p.strip() for p in re.split(r"[|;]", approval)]
    if len(parts) < 4:
        return False
    head = parts[0].lower()
    if not (head.startswith("onayla") or head.startswith("approve")):
        return False
    p_platform = parts[1].lower()
    p_account = parts[2]
    p_action = parts[3].lower()
    if p_platform != platform:
        return False
    if _digits(p_account) and _digits(p_account) != _digits(account) and p_account != account:
        return False
    if p_action and p_action != action:
        return False
    return True


def write_log(change: dict, decision: str, reasons: list[str]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": _now(),
        "platform": change.get("platform"),
        "account_id": change.get("account_id"),
        "action": change.get("action"),
        "entity": change.get("entity"),
        "status": change.get("status"),
        "daily_budget_try": change.get("daily_budget_try"),
        "monthly_budget_try": change.get("monthly_budget_try"),
        "old_value": change.get("old_value"),
        "new_value": change.get("new_value"),
        "decision": decision,
        "reasons": reasons,
    }
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Kozbeyli reklam değişiklik korkulukları")
    ap.add_argument("--check", required=True, help="Değişiklik tanımı JSON dosyası")
    ap.add_argument("--approval", default=None, help="Açık onay metni (opsiyonel)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    try:
        change = json.loads(Path(args.check).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"[HATA] Değişiklik dosyası okunamadı: {exc}", file=sys.stderr)
        return 1

    cfg = load_config()
    decision, reasons = evaluate(change, cfg, args.approval)
    write_log(change, decision, reasons)

    if not args.quiet:
        print(f"KARAR: {decision}")
        for r in reasons:
            print(f"  - {r}")
        print(f"(denetim kaydı: {LOG_FILE})")

    return {"ALLOW": 0, "DENY": 1, "NEEDS_APPROVAL": 2}[decision]


if __name__ == "__main__":
    raise SystemExit(main())
