import re
from typing import List, Optional, Tuple

from kads.core import CONFIG_FILE, load_env

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

ENABLE_ACTIONS = {"enable", "resume", "activate", "set_enabled", "unpause"}

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


def _digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def load_security_config() -> dict:
    """Ortamdan güvenlik konfigürasyonunu (allowlist, tavan, writes) yükler."""
    env = load_env()
    cfg = {
        "google_monthly_try": float(env.get("GOOGLE_MONTHLY_BUDGET_TRY", "15000")),
        "meta_monthly_try": float(env.get("META_MONTHLY_BUDGET_TRY", "15000")),
        "google_daily_try": float(env.get("GOOGLE_AVG_DAILY_BUDGET_TRY", "493")),
        "meta_daily_try": float(env.get("META_DAILY_BUDGET_TRY", "500")),
        "writes_enabled": env.get("ADS_WRITES_ENABLED", "false").lower() == "true",
        "google_allowlist": set(),
        "meta_allowlist": set(),
    }
    g = _digits(env.get("GOOGLE_ADS_CUSTOMER_ID", ""))
    if len(g) == 10:
        cfg["google_allowlist"].add(g)
    m = env.get("META_AD_ACCOUNT_ID", "").strip()
    if re.fullmatch(r"act_\d+", m):
        cfg["meta_allowlist"].add(m)

    if CONFIG_FILE.exists():
        text = CONFIG_FILE.read_text(encoding="utf-8", errors="ignore")
        for acc in re.findall(r"act_\d+", text):
            cfg["meta_allowlist"].add(acc)
        for cid in re.findall(r"\b(\d{3}-\d{3}-\d{4})\b", text):
            cfg["google_allowlist"].add(_digits(cid))
        m2 = re.search(r"write_guardrails:\s*\n\s*enabled:\s*(true|false)", text)
        if m2:
            cfg["writes_enabled"] = cfg["writes_enabled"] and (m2.group(1) == "true")
    return cfg


def check_anti_loop_policy(change: dict) -> bool:
    """
    Anti-Loop Guard (L99 God Tier):
    Checks if the same action for this platform and account has failed 2 or more times in the last 24 hours.
    Returns True if looping is detected (should deny).
    """
    from datetime import datetime, timedelta
    try:
        from kads.data.warehouse.db import SessionLocal
        from kads.data.warehouse.models import FactActionJournal
        
        db = SessionLocal()
        try:
            action = change.get("action")
            platform = change.get("platform")
            
            one_day_ago = datetime.utcnow() - timedelta(days=1)
            
            # Query failed actions for the same platform and action type
            query = db.query(FactActionJournal).filter(
                FactActionJournal.platform == platform,
                FactActionJournal.action_type == action,
                FactActionJournal.status == "failed",
                FactActionJournal.executed_at >= one_day_ago
            )
            
            failed_count = query.count()
            if failed_count >= 2:
                return True
        finally:
            db.close()
    except Exception:
        # Fallback to False if database is unavailable (e.g. during simple tests)
        pass
    return False


def evaluate_change(
    change: dict, cfg: dict, approval: Optional[str]
) -> Tuple[str, List[str]]:
    """Değişikliği guardrail'lerden geçirir: (ALLOW/DENY/NEEDS_APPROVAL, gerekçeler)."""
    reasons = []
    
    if check_anti_loop_policy(change):
        reasons.append(
            "Anti-Loop Policy triggered: this action has failed 2 or more times in the last 24 hours. Halting to prevent runaway API spend."
        )
        return "DENY", reasons

    platform = (change.get("platform") or "").lower()
    action = (change.get("action") or "").lower()
    account = (change.get("account_id") or "").strip()
    status = (change.get("status") or "").upper()
    daily = change.get("daily_budget_try")
    monthly = change.get("monthly_budget_try")

    if not cfg["writes_enabled"]:
        reasons.append(
            "Gerçek yazma kapalı (ADS_WRITES_ENABLED!=true veya write_guardrails.enabled!=true). Yalnızca dry-run/önizleme."
        )
        return "DENY", reasons

    if platform not in {"google", "meta"}:
        reasons.append(f"Bilinmeyen platform: '{platform}'. google veya meta olmalı.")
        return "DENY", reasons

    if action in HARD_BLOCKED_ACTIONS:
        reasons.append(
            f"Aksiyon kalıcı olarak engellendi: '{action}' (silme/ödeme/kullanıcı/liste yükleme yok)."
        )
        return "DENY", reasons

    if action not in ALLOWED_ACTIONS:
        reasons.append(f"Aksiyon izinli listede değil: '{action}'.")
        return "DENY", reasons

    if platform == "google":
        allow = cfg["google_allowlist"]
        acc_key = _digits(account)
        if not allow:
            reasons.append(
                "Google hesap allowlist boş. GOOGLE_ADS_CUSTOMER_ID (10 hane) tanımlayın."
            )
            return "DENY", reasons
        if acc_key not in allow:
            reasons.append(
                f"Google hesabı allowlist dışında: '{account}'. İzinli: {sorted(allow)}"
            )
            return "DENY", reasons
    else:  # meta
        allow = cfg["meta_allowlist"]
        if not allow:
            reasons.append(
                "Meta hesap allowlist boş. META_AD_ACCOUNT_ID (act_...) tanımlayın."
            )
            return "DENY", reasons
        if account not in allow:
            reasons.append(
                f"Meta hesabı allowlist dışında: '{account}'. İzinli: {sorted(allow)}"
            )
            return "DENY", reasons

    _status_creates = {
        "create_campaign",
        "create_adset",
        "create_ad_group",
        "create_ad",
    }
    creates_entity = action in _status_creates or (
        action.startswith("create")
        and change.get("entity") in {"campaign", "adset", "ad_group", "ad"}
    )
    if creates_entity and status != "PAUSED":
        reasons.append(
            f"Yeni varlik PAUSED olusturulmali; gelen status='{status or '(yok)'}'."
        )
        return "DENY", reasons

    daily_cap = (
        cfg["google_daily_try"] if platform == "google" else cfg["meta_daily_try"]
    )
    monthly_cap = (
        cfg["google_monthly_try"] if platform == "google" else cfg["meta_monthly_try"]
    )
    if daily is not None:
        try:
            if float(daily) > float(daily_cap):
                reasons.append(
                    f"Günlük bütçe tavanı aşıldı: {daily} > {daily_cap} TL ({platform})."
                )
                return "DENY", reasons
        except (TypeError, ValueError):
            reasons.append(f"Geçersiz daily_budget_try: {daily!r}")
            return "DENY", reasons
    if monthly is not None:
        try:
            if float(monthly) > float(monthly_cap):
                reasons.append(
                    f"Aylık bütçe tavanı aşıldı: {monthly} > {monthly_cap} TL ({platform})."
                )
                return "DENY", reasons
        except (TypeError, ValueError):
            reasons.append(f"Geçersiz monthly_budget_try: {monthly!r}")
            return "DENY", reasons

    needs = _approval_matches(approval, platform, account, action)
    if action in ENABLE_ACTIONS:
        head = re.split(r"[|;]", (approval or ""))[0].strip().lower()
        second_marker = (
            head.startswith("onayla-2")
            or head.startswith("approve-2")
            or re.search(
                r"etkinle\u015ftir|etkinlestir|i\u015fte etkinle",
                (approval or ""),
                re.I,
            )
        )
        if not (needs and second_marker):
            reasons.append(
                "ENABLED işlemi AYRI ikinci onay ister. Biçim: "
                "'ONAYLA-2 | platform | hesap | enable | <gunluk_butce>'."
            )
            return "NEEDS_APPROVAL", reasons
    if not needs:
        reasons.append(
            "Açık onay gerekli. Biçim: 'ONAYLA | platform | hesap_id | aksiyon | gunluk_butce'."
        )
        return "NEEDS_APPROVAL", reasons

    reasons.append(
        "Tüm korkuluklar geçildi: allowlist OK, PAUSED OK, bütçe OK, onay OK."
    )
    return "ALLOW", reasons


def _approval_matches(
    approval: Optional[str], platform: str, account: str, action: str
) -> bool:
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
    if (
        _digits(p_account)
        and _digits(p_account) != _digits(account)
        and p_account != account
    ):
        return False
    if p_action and p_action != action:
        return False
    return True
