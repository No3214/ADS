#!/usr/bin/env python3
"""
kads.rules — bütçe/teklif optimizasyon kuralları (deterministik öneri motoru).

Metrikleri (CSV: metrik,deger) okur, OPT_RULES'a göre tetiklenen kuralları ve
ÖNERİLEN aksiyonları döndürür. Otomatik UYGULAMAZ — her yazma yine guardrail +
açık onaydan geçer (docs/04). "Otomasyon" = öneri + guardrail'li değişiklik yolu.
"""
from __future__ import annotations

import csv
from pathlib import Path

from kads.data_ext import OPT_RULES

_OPS = {">": lambda a, b: a > b, ">=": lambda a, b: a >= b,
        "<": lambda a, b: a < b, "<=": lambda a, b: a <= b, "==": lambda a, b: a == b}


def rule_rows() -> list[dict]:
    return [{"id": r["id"], "metrik": r["metric"], "kosul": f'{r["op"]} {r["threshold"]}',
             "aksiyon": r["action"], "oncelik": r["pri"]} for r in OPT_RULES]


def evaluate(metrics: dict) -> list[dict]:
    """Tetiklenen kuralları döndürür. metrics: {metric_name: float}."""
    out = []
    for r in OPT_RULES:
        v = metrics.get(r["metric"])
        if v is None:
            continue
        try:
            if _OPS[r["op"]](float(v), float(r["threshold"])):
                out.append({"id": r["id"], "metrik": r["metric"], "deger": v,
                            "kosul": f'{r["op"]} {r["threshold"]}', "aksiyon": r["action"],
                            "oncelik": r["pri"]})
        except (TypeError, ValueError):
            continue
    pri = {"Risk": 0, "Fırsat": 1, "Orta": 2}
    return sorted(out, key=lambda x: pri.get(x["oncelik"], 9))


def load_metrics_csv(path: Path) -> dict:
    """metrik,deger satırlarını {metric: float} olarak okur."""
    m = {}
    with path.open(encoding="utf-8-sig") as fh:
        for row in csv.reader(fh):
            if len(row) >= 2 and row[0].strip().lower() not in ("metrik", "metric", ""):
                try:
                    m[row[0].strip()] = float(str(row[1]).replace(",", ".").strip())
                except ValueError:
                    pass
    return m


METRICS_TEMPLATE = [
    ("blended_roas", 0), ("blended_cpa_try", 0), ("nonbrand_ctr_pct", 0),
    ("meta_frequency", 0), ("cpc_try", 0), ("weekly_conversions", 0),
    ("conversions_30d", 0), ("spend_pace_pct", 0),
]
