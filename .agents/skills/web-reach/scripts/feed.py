#!/usr/bin/env python3
"""Fetch and parse an RSS or Atom feed. Falls back to Jina Reader if the host
blocks a direct request. RSS is the most underrated way to pull fresh,
structured content from blogs, news sites, subreddits, YouTube channels, status
pages, and changelogs without any API.

Usage:
  feed.py <feed-url> [--n 15]

Handy feed URL patterns:
  YouTube channel : https://www.youtube.com/feeds/videos.xml?channel_id=<id>
  Subreddit       : https://www.reddit.com/r/<sub>/.rss   (may be blocked; see social.md)
  GitHub releases : https://github.com/<owner>/<repo>/releases.atom
  Any WordPress   : <site>/feed/
"""
import argparse
import sys
import os
import re
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import http_get, reader_fetch, out  # noqa: E402


def _txt(el, *tags):
    for t in tags:
        c = el.find(t)
        if c is not None and (c.text or c.get("href")):
            return (c.text or c.get("href") or "").strip()
    return None


def parse(xml, n):
    xml = re.sub(r'xmlns="[^"]+"', "", xml, count=1)  # drop default ns for simple finds
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        return None, "xml parse error: %s" % e
    items = []
    # RSS <item> or Atom <entry>
    nodes = root.iter("item")
    nodes = list(nodes) or list(root.iter("entry"))
    for it in nodes[:n]:
        link = _txt(it, "link")
        if link is None:
            le = it.find("link")
            link = le.get("href") if le is not None else None
        items.append({
            "title": _txt(it, "title"),
            "link": link,
            "published": _txt(it, "pubDate", "published", "updated"),
            "summary": (_txt(it, "description", "summary", "content") or "")[:400],
        })
    return items, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--n", type=int, default=15)
    a = ap.parse_args()
    r = http_get(a.url, timeout=25)
    body = r["body"]
    if r["status"] != 200 or "<rss" not in body and "<feed" not in body:
        rr = reader_fetch(a.url, fmt="html")
        if "<rss" in rr["body"] or "<feed" in rr["body"]:
            body = rr["body"]
        else:
            out({"ok": False, "status": r["status"],
                 "error": "could not retrieve a parseable feed",
                 "hint": "host may block direct + reader; try a backend"})
            return
    items, err = parse(body, a.n)
    if err:
        out({"ok": False, "error": err})
        return
    out({"ok": True, "count": len(items), "items": items})


if __name__ == "__main__":
    main()
