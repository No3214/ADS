from typing import Any, Dict

from kads import core


def audit_tracking_health() -> Dict[str, Any]:
    """ENV-KONFIG hazırlık skoru (DİKKAT: canlı tag-fire DEĞİL).

    Bu fonksiyon yalnızca .env'de ID'lerin tanımlı/placeholder-olmadığını puanlar —
    GTM içinde etiketin gerçekten ateşlediğini doğrulamaz. Canlı doğrulanmış boşluklar
    için tek gerçek kaynak: kads.data_ext.TRACKING_STATE (çıktıda 'live_gaps'). Karar
    motoru bu skoru 'ölçüm canlı' kanıtı SAYMAMALI; otonom bütçe artışı live_gaps boşken yapılmalı.
    """
    env = core.load_env()
    results = {}
    total_components = 5
    healthy_count = 0.0

    # 1. GA4
    ga4_id = env.get("GA4_MEASUREMENT_ID")
    if ga4_id and not core.is_placeholder(ga4_id):
        results["GA4"] = {
            "status": "healthy",
            "score": 100.0,
            "details": f"ID {ga4_id} configured",
        }
        healthy_count += 1.0
    else:
        results["GA4"] = {
            "status": "error",
            "score": 0.0,
            "details": "GA4_MEASUREMENT_ID is missing or placeholder",
        }

    # 2. GTM
    gtm_id = env.get("GTM_CONTAINER_ID")
    if gtm_id and not core.is_placeholder(gtm_id):
        results["GTM"] = {
            "status": "healthy",
            "score": 100.0,
            "details": f"Container {gtm_id} configured",
        }
        healthy_count += 1.0
    else:
        results["GTM"] = {
            "status": "error",
            "score": 0.0,
            "details": "GTM_CONTAINER_ID is missing or placeholder",
        }

    # 3. Meta Pixel
    pixel_id = env.get("META_PIXEL_ID")
    if pixel_id and not core.is_placeholder(pixel_id):
        results["MetaPixel"] = {
            "status": "healthy",
            "score": 100.0,
            "details": f"Pixel {pixel_id} configured",
        }
        healthy_count += 1.0
    else:
        results["MetaPixel"] = {
            "status": "error",
            "score": 0.0,
            "details": "META_PIXEL_ID is missing or placeholder",
        }

    # 4. Meta CAPI (Server-Side)
    capi_token = env.get("META_ACCESS_TOKEN")
    if capi_token and not core.is_placeholder(capi_token):
        results["MetaCAPI"] = {
            "status": "healthy",
            "score": 100.0,
            "details": "CAPI Access Token present",
        }
        healthy_count += 1.0
    else:
        results["MetaCAPI"] = {
            "status": "stale",
            "score": 50.0,
            "details": "META_ACCESS_TOKEN is missing (browser-only fallback)",
        }
        healthy_count += 0.5

    # 5. Google OCT (Offline Conversion Tracking)
    oct_id = env.get("GOOGLE_ADS_CUSTOMER_ID")
    if oct_id and not core.is_placeholder(oct_id):
        results["GoogleOCT"] = {
            "status": "healthy",
            "score": 100.0,
            "details": "OCT upload flow enabled",
        }
        healthy_count += 1.0
    else:
        results["GoogleOCT"] = {
            "status": "error",
            "score": 0.0,
            "details": "GOOGLE_ADS_CUSTOMER_ID is missing",
        }

    blended_score = (healthy_count / total_components) * 100.0

    # Canlı doğrulanmış açık kalemler (env-presence ile karışmasın diye ayrı).
    live_gaps = []
    try:
        from kads.data_ext import TRACKING_STATE
        live_gaps = [
            {"bilesen": r["bilesen"], "durum": r["durum"]}
            for r in TRACKING_STATE
            if r.get("durum") in ("EKSİK", "KAPALI", "YOK")
        ]
    except Exception:
        pass

    return {
        "score": round(blended_score, 1),
        "status": "healthy" if blended_score >= 80.0 else "unhealthy",
        "components": results,
        "scope": "env-config-readiness",  # canlı tag-fire değil
        "live_gaps": live_gaps,
        "note": "env-presence skoru; canlı boşluklar için live_gaps + 'kads tracking'. live_gaps boş değilse ölçüm canlı sayılmaz.",
    }
