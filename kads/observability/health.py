from typing import Any, Dict

from kads import core


def audit_tracking_health() -> Dict[str, Any]:
    """
    Evaluates GTM, GA4, Meta Pixel, Meta CAPI, and Google OCT configurations.
    Returns a health score and dictionary of status results.
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

    return {
        "score": round(blended_score, 1),
        "status": "healthy" if blended_score >= 80.0 else "unhealthy",
        "components": results,
    }
