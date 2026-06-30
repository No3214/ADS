#!/usr/bin/env python3
"""
kads.calendar — çok kanallı içerik takvimi üreteci (IG/FB/TikTok/LinkedIn/X + Google İşletme).
WEEK_PLAN'ı başlangıç tarihinden itibaren N gün döşer. Deterministik.
"""

from __future__ import annotations

import csv
import datetime as _dt
from pathlib import Path

from kads import data
from kads.data_ext import PEAK_TIMES, WEEK_PLAN

_GUN = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]


def _post_text(concept_key: str, channel: str) -> str:
    c = data.META_COPY[concept_key]
    head = c["headlines"][0]
    cta = c["cta"]
    link = " kozbeylikonagi.com" if channel in ("X", "LinkedIn", "Facebook") else ""
    return f"{head} — {cta}.{link}".strip()


def generate(days: int = 30, start: _dt.date | None = None) -> list[dict]:
    start = start or _dt.date.today()
    rows = []
    for i in range(days):
        d = start + _dt.timedelta(days=i)
        for channel, concept, fmt in WEEK_PLAN.get(d.weekday(), []):
            rows.append(
                {
                    "tarih": d.isoformat(),
                    "gün": _GUN[d.weekday()],
                    "saat": PEAK_TIMES.get(channel, "11:00"),
                    "kanal": channel,
                    "konsept": concept,
                    "format": fmt,
                    "metin": _post_text(concept, channel),
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=["tarih", "gün", "saat", "kanal", "konsept", "format", "metin"],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)
