#!/usr/bin/env python3
"""
kads.report — raporlama: metrik CSV şablonu + KPI hesabı (blended ROAS/CPA).
Raporlama panosu (dashboard/rapor.html) bu şablonu okur/yapıştırır.
"""

from __future__ import annotations

import csv
from pathlib import Path

from kads.rules import METRICS_TEMPLATE

KPI_FIELDS = [
    "google_spend_try",
    "meta_spend_try",
    "tracked_revenue_try",
    "google_clicks",
    "google_impressions",
    "google_conversions",
    "meta_purchases",
    "meta_impressions",
    "meta_clicks",
    "meta_frequency",
    "whatsapp_leads",
]


def metrics_template_rows() -> list[dict]:
    rows = [{"metrik": k, "deger": v} for k, v in METRICS_TEMPLATE]
    rows += [{"metrik": k, "deger": 0} for k in KPI_FIELDS]
    return rows


def compute(metrics: dict) -> dict:
    g = float(metrics.get("google_spend_try", 0) or 0)
    m = float(metrics.get("meta_spend_try", 0) or 0)
    rev = float(metrics.get("tracked_revenue_try", 0) or 0)
    spend = g + m
    conv = float(metrics.get("google_conversions", 0) or 0) + float(
        metrics.get("meta_purchases", 0) or 0
    )
    roas = (rev / spend) if spend else 0
    cpa = (spend / conv) if conv else 0
    clicks = float(metrics.get("google_clicks", 0) or 0) + float(
        metrics.get("meta_clicks", 0) or 0
    )
    impr = float(metrics.get("google_impressions", 0) or 0) + float(
        metrics.get("meta_impressions", 0) or 0
    )
    ctr = (clicks / impr * 100) if impr else 0
    cpc = (spend / clicks) if clicks else 0
    return {
        "toplam_harcama_try": round(spend, 2),
        "izlenen_gelir_try": round(rev, 2),
        "blended_roas": round(roas, 2),
        "blended_cpa_try": round(cpa, 2),
        "blended_ctr_pct": round(ctr, 2),
        "blended_cpc_try": round(cpc, 2),
        "toplam_donusum": round(conv, 1),
    }


def write_template(path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = metrics_template_rows()
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["metrik", "deger"])
        for r in rows:
            w.writerow([r["metrik"], r["deger"]])
    return len(rows)
