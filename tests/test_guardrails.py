"""scripts/guardrails.py kod seviyesinde guvenlik testleri."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("guardrails", ROOT / "scripts" / "guardrails.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

BASE_CFG = {
    "google_monthly_try": 15000, "meta_monthly_try": 15000,
    "google_daily_try": 493, "meta_daily_try": 500,
    "writes_enabled": True,
    "google_allowlist": {"1234567890"}, "meta_allowlist": {"act_123"},
}


def cfg(**over):
    c = dict(BASE_CFG); c.update(over)
    c["google_allowlist"] = set(c["google_allowlist"]); c["meta_allowlist"] = set(c["meta_allowlist"])
    return c


def test_writes_disabled_denies():
    d, _ = g.evaluate({"platform": "google", "action": "create_campaign",
                       "account_id": "1234567890", "status": "PAUSED", "daily_budget_try": 100},
                      cfg(writes_enabled=False), None)
    assert d == "DENY"


def test_hard_blocked_action_denied():
    d, _ = g.evaluate({"platform": "meta", "action": "delete_campaign",
                       "account_id": "act_123"}, cfg(), "ONAYLA | meta | act_123 | delete_campaign | 0")
    assert d == "DENY"


def test_account_not_in_allowlist():
    d, _ = g.evaluate({"platform": "google", "action": "create_campaign",
                       "account_id": "9999999999", "status": "PAUSED", "daily_budget_try": 100},
                      cfg(), "ONAYLA | google | 9999999999 | create_campaign | 100")
    assert d == "DENY"


def test_new_campaign_must_be_paused():
    d, _ = g.evaluate({"platform": "google", "action": "create_campaign", "entity": "campaign",
                       "account_id": "1234567890", "status": "ENABLED", "daily_budget_try": 100},
                      cfg(), "ONAYLA | google | 1234567890 | create_campaign | 100")
    assert d == "DENY"


def test_budget_cap_enforced():
    d, _ = g.evaluate({"platform": "google", "action": "update_budget",
                       "account_id": "1234567890", "daily_budget_try": 99999},
                      cfg(), "ONAYLA | google | 1234567890 | update_budget | 99999")
    assert d == "DENY"


def test_needs_approval_without_approval():
    d, _ = g.evaluate({"platform": "google", "action": "create_campaign", "entity": "campaign",
                       "account_id": "1234567890", "status": "PAUSED", "daily_budget_try": 100},
                      cfg(), None)
    assert d == "NEEDS_APPROVAL"


def test_enable_requires_second_approval():
    chg = {"platform": "meta", "action": "enable", "account_id": "act_123", "daily_budget_try": 100}
    d1, _ = g.evaluate(chg, cfg(), "ONAYLA | meta | act_123 | enable | 100")
    assert d1 == "NEEDS_APPROVAL"  # birinci onay yetmez
    d2, _ = g.evaluate(chg, cfg(), "ONAYLA-2 | meta | act_123 | enable | 100")
    assert d2 == "ALLOW"


def test_valid_create_allows():
    d, _ = g.evaluate({"platform": "google", "action": "create_campaign", "entity": "campaign",
                       "account_id": "1234567890", "status": "PAUSED", "daily_budget_try": 148},
                      cfg(), "ONAYLA | google | 1234567890 | create_campaign | 148")
    assert d == "ALLOW"
