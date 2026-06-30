#!/usr/bin/env python3
"""Read X / Twitter content with no API key, via the public syndication
endpoints that power embedded tweets.

Usage:
  x.py user <handle> [--n 20]     # a user's recent tweets (newest first)
  x.py tweet <id>                 # a single tweet by numeric id

What this CAN do keyless: a known account's recent timeline, and any public
tweet by id (text, author, like/retweet/reply counts).
What it CANNOT do keyless: keyword search across all of X. For that you need a
backend or key -- see references/social.md (xAI live search, Apify, Bright Data,
ScrapeCreators, or a logged-in twitter CLI).
"""
import argparse
import sys
import os
import re
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import http_get, http_json, out  # noqa: E402


def user_timeline(handle, n):
    handle = handle.lstrip("@")
    url = ("https://syndication.twitter.com/srv/timeline-profile/screen-name/"
           + handle)
    r = http_get(url, timeout=25)
    m = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        r["body"], re.S)
    if not m:
        return {"ok": False, "status": r["status"],
                "error": "timeline payload not found (suspended/private/renamed?)"}
    try:
        data = json.loads(m.group(1))
        entries = data["props"]["pageProps"]["timeline"]["entries"]
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "status": r["status"], "error": "parse: %s" % e}
    tweets = []
    for e in entries:
        t = e.get("content", {}).get("tweet")
        if not t:
            continue
        tweets.append({
            "id": t.get("id_str"),
            "created_at": t.get("created_at"),
            "text": t.get("full_text") or t.get("text"),
            "likes": t.get("favorite_count"),
            "retweets": t.get("retweet_count"),
            "replies": t.get("reply_count"),
            "quotes": t.get("quote_count"),
            "url": t.get("permalink") and ("https://x.com" + t["permalink"])
                   or "https://x.com/%s/status/%s" % (handle, t.get("id_str")),
        })
    return {"ok": bool(tweets), "handle": handle, "count": len(tweets),
            "tweets": tweets[:n], "status": r["status"]}


def single_tweet(tid):
    url = ("https://cdn.syndication.twimg.com/tweet-result?id=%s&lang=en&token=a"
           % tid)
    r = http_json(url, timeout=20)
    d = r.get("json") or {}
    if not d:
        return {"ok": False, "status": r["status"],
                "error": "no data (deleted, protected, or rate-limited)"}
    u = d.get("user") or {}
    return {"ok": True, "id": d.get("id_str"), "created_at": d.get("created_at"),
            "text": d.get("text"), "likes": d.get("favorite_count"),
            "author": u.get("screen_name"), "name": u.get("name")}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    pu = sub.add_parser("user"); pu.add_argument("handle"); pu.add_argument("--n", type=int, default=20)
    pt = sub.add_parser("tweet"); pt.add_argument("id")
    a = ap.parse_args()
    if a.cmd == "user":
        out(user_timeline(a.handle, a.n))
    else:
        out(single_tweet(a.id))


if __name__ == "__main__":
    main()
