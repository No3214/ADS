#!/usr/bin/env python3
"""Probe what web-reach can actually use right now: command-line tools, API
keys/backends in the environment, and live reachability of each technique's
endpoint (egress policy and IP reputation differ per environment). Run this
first, and any time a fetch fails, so you route to a method that works instead
of guessing.

Usage:
  doctor.py            # human-readable summary + routing advice
  doctor.py --json     # machine-readable
"""
import argparse
import sys
import os
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import http_get, out  # noqa: E402

TOOLS = ["curl", "yt-dlp", "gh", "node", "python3", "ffmpeg"]

KEYS = {
    "JINA_API_KEY": "higher-rate page fetching (Jina Reader)",
    "GITHUB_TOKEN": "GitHub higher limits + code search",
    "EXA_API_KEY": "Exa neural web search",
    "TAVILY_API_KEY": "Tavily search/extract",
    "PERPLEXITY_API_KEY": "Perplexity answer search",
    "BRAVE_API_KEY": "Brave web search",
    "APIFY_API_TOKEN": "Apify actors (Reddit/TikTok/IG/etc.)",
    "BRIGHTDATA_API_KEY": "Bright Data scraping",
    "SCRAPECREATORS_API_KEY": "social platform scraping (X/TikTok/IG/YT)",
    "XAI_API_KEY": "xAI Grok live X search",
}

PROBES = {
    "jina_reader": "https://r.jina.ai/https://example.com",
    "hn_algolia": "https://hn.algolia.com/api/v1/search?query=test&hitsPerPage=1",
    "github_api": "https://api.github.com/rate_limit",
    "x_syndication": "https://syndication.twitter.com/srv/timeline-profile/screen-name/x",
    "wayback": "https://archive.org/wayback/available?url=example.com",
    "bluesky_public": "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=test&limit=1",
    "reddit_direct": "https://www.reddit.com/r/programming/top.json?limit=1",
    "youtube_direct": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
}


def reachable(url):
    r = http_get(url, timeout=12, retries=0)
    ok = r["status"] == 200 and len(r["body"]) > 50
    return ok, r["status"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    tools = {t: bool(shutil.which(t)) for t in TOOLS}
    keys = {k: bool(os.environ.get(k)) for k in KEYS}
    conn = {}
    for name, url in PROBES.items():
        ok, code = reachable(url)
        conn[name] = {"ok": ok, "status": code}

    report = {"tools": tools, "keys": keys, "connectivity": conn}

    if a.json:
        out(report)
        return

    print("web-reach doctor\n================")
    print("\nTools:")
    for t, ok in tools.items():
        print("  %-8s %s" % (t, "yes" if ok else "no"))
    print("\nKeys / backends present:")
    any_key = False
    for k, ok in keys.items():
        if ok:
            any_key = True
            print("  %-22s yes  (%s)" % (k, KEYS[k]))
    if not any_key:
        print("  none -- running fully keyless")
    print("\nLive connectivity:")
    for name, v in conn.items():
        print("  %-16s %s (HTTP %s)" % (name, "reachable" if v["ok"] else "BLOCKED", v["status"]))

    print("\nRouting advice:")
    if conn["jina_reader"]["ok"]:
        print("  - General pages: fetch.py (auto) -> Jina Reader handles JS/anti-bot/blocked hosts.")
    else:
        print("  - Jina Reader BLOCKED here: rely on direct fetch + Wayback; set JINA_API_KEY if possible.")
    print("  - HN/GitHub/X-timeline/Wayback: use hn.py / github.py / x.py / fetch.py --mode wayback.")
    if not conn["reddit_direct"]["ok"]:
        print("  - Reddit is blocked keyless: use a backend key (Apify/Bright Data/ScrapeCreators) -- see references/social.md.")
    if not conn["youtube_direct"]["ok"]:
        print("  - YouTube blocked keyless here: use yt-dlp where reachable, else a transcript backend -- see references/video.md.")
    if not conn["bluesky_public"]["ok"]:
        print("  - Bluesky public API blocked on this IP: skip bsky source or route via a backend.")


if __name__ == "__main__":
    main()
