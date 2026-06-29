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


from kads.core.security import load_security_config, evaluate_change

def load_config() -> dict:
    return load_security_config()


def evaluate(change: dict, cfg: dict, approval: str | None) -> tuple[str, list[str]]:
    return evaluate_change(change, cfg, approval)



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
