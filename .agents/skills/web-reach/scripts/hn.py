#!/usr/bin/env python3
"""Hacker News via the open Algolia API (no key, no auth). Great for developer
and tech sentiment, and one of the most reliable recency sources on the web.

Usage:
  hn.py search <query> [--recent] [--days 30] [--n 10] [--min-points 0]
      default ranks by relevance/points; --recent ranks strictly by date.
  hn.py thread <id>               # a story plus its comment tree (flattened)

Examples:
  hn.py search "rag pipeline" --recent --days 14 --n 8
  hn.py thread 39495591
"""
import argparse
import sys
import os
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import http_json, out, strip_html  # noqa: E402


def search(q, recent, days, n, minpts):
    endpoint = "search_by_date" if recent else "search"
    params = {"query": q, "tags": "story", "hitsPerPage": str(n)}
    nf = []
    if days:
        nf.append("created_at_i>%d" % (int(time.time()) - days * 86400))
    if minpts:
        nf.append("points>=%d" % minpts)
    if nf:
        params["numericFilters"] = ",".join(nf)
    url = "https://hn.algolia.com/api/v1/%s?%s" % (
        endpoint, urllib.parse.urlencode(params))
    r = http_json(url)
    hits = (r.get("json") or {}).get("hits", [])
    items = [{
        "title": h.get("title"),
        "url": h.get("url"),
        "points": h.get("points"),
        "comments": h.get("num_comments"),
        "author": h.get("author"),
        "created": h.get("created_at"),
        "hn_url": "https://news.ycombinator.com/item?id=%s" % h.get("objectID"),
    } for h in hits]
    return {"ok": True, "query": q, "count": len(items), "items": items}


def thread(sid):
    r = http_json("https://hn.algolia.com/api/v1/items/%s" % sid)
    d = r.get("json") or {}
    if not d:
        return {"ok": False, "status": r["status"], "error": "story not found"}
    acc = []

    def walk(node, depth=0):
        for c in node.get("children", []) or []:
            if c.get("text"):
                acc.append({"by": c.get("author"), "depth": depth,
                            "text": strip_html(c["text"], 1000)})
            walk(c, depth + 1)

    walk(d)
    return {"ok": True, "title": d.get("title"), "url": d.get("url"),
            "points": d.get("points"), "author": d.get("author"),
            "comment_count": len(acc), "comments": acc[:40]}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    ps = sub.add_parser("search")
    ps.add_argument("query")
    ps.add_argument("--recent", action="store_true")
    ps.add_argument("--days", type=int, default=0)
    ps.add_argument("--n", type=int, default=10)
    ps.add_argument("--min-points", type=int, default=0, dest="minpts")
    pt = sub.add_parser("thread")
    pt.add_argument("id")
    a = ap.parse_args()
    if a.cmd == "search":
        out(search(a.query, a.recent, a.days, a.n, a.minpts))
    else:
        out(thread(a.id))


if __name__ == "__main__":
    main()
