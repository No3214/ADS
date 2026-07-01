#!/usr/bin/env python3
"""
kads.publish — içerik takvimini Postiz-hazır CSV'ye çevirir (otomatik publisher).
Postiz (gitroomhq/postiz-app, AGPL-3.0, self-host ÜCRETSİZ): IG/FB/TikTok/LinkedIn/X + 20 kanal,
REST API + n8n/Make + AI ajan. Bu CSV elle import veya n8n/API ile zamanlama için kullanılır.
"""

from __future__ import annotations

import csv
from pathlib import Path

from kads import calendar as cal


# Postiz/n8n dostu sütunlar
def to_postiz_rows(rows: list[dict]) -> list[dict]:
    """Takvimi Postiz içe-aktarma satırlarına dönüştürür."""
    out = []
    for r in rows:
        out.append(
            {
                "date": r["tarih"],
                "time": r["saat"],
                "channel": r["kanal"],
                "content": r["metin"],
                "media": r["format"],
                "concept": r["konsept"],
            }
        )
    return out


def write_csv(path: Path, days: int = 30) -> int:
    """Postiz-hazır yayın CSV'sini yazar; satır sayısını döndürür."""
    rows = to_postiz_rows(cal.generate(days=days))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(
            fh, fieldnames=["date", "time", "channel", "content", "media", "concept"]
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)
