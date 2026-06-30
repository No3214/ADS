#!/usr/bin/env python3
"""Fetch one URL's readable content, escalating past the walls that the
built-in web_fetch usually cannot pass: JavaScript-rendered pages, soft
anti-bot/CDN challenges, geo/login interstitials, and hosts blocked by local
network egress policy.

Usage:
  fetch.py <url>                      # auto: direct -> Jina Reader -> Wayback
  fetch.py <url> --mode reader        # force the reader path
  fetch.py <url> --mode wayback       # force the archived snapshot
  fetch.py <url> --raw                # return raw HTML instead of clean markdown
  fetch.py <url> --max 8000           # truncate content to N chars

Output is JSON: {ok, method, status, final_url, steps[], content}.
`steps` records every method tried so you can see how the content was obtained.
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import http_get, reader_fetch, wayback_lookup, out  # noqa: E402

BLOCK_HINTS = (
    "blocked by egress", "just a moment", "enable javascript", "captcha",
    "access denied", "are you a human", "cf-browser-verification",
    "whoa there, pardner", "attention required", "returned error 403",
    "target url returned error", "request has been blocked",
)


def looks_blocked(status, body):
    if status in (0, 401, 403, 429, 503):
        return True
    if not body or len(body.strip()) < 200:
        return True
    low = body[:2500].lower()
    return any(h in low for h in BLOCK_HINTS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--mode", default="auto",
                    choices=["auto", "direct", "reader", "wayback"])
    ap.add_argument("--raw", action="store_true",
                    help="return raw body instead of reader-cleaned markdown")
    ap.add_argument("--max", type=int, default=0,
                    help="truncate content to N chars (0 = no limit)")
    a = ap.parse_args()

    steps = []

    def emit(method, status, body, src, ok):
        if a.max and body and len(body) > a.max:
            body = body[:a.max] + "\n\n[...truncated %d chars...]" % (len(body) - a.max)
        out({"ok": ok, "method": method, "status": status,
             "final_url": src, "steps": steps, "content": body})
        sys.exit(0)

    # Forced single-method modes return whatever they get.
    if a.mode == "direct":
        r = http_get(a.url, timeout=25)
        steps.append({"method": "direct", "status": r["status"], "bytes": len(r["body"])})
        emit("direct", r["status"], r["body"], r["url"],
             not looks_blocked(r["status"], r["body"]))
    if a.mode == "reader":
        r = reader_fetch(a.url, fmt="html" if a.raw else None)
        steps.append({"method": "reader", "status": r["status"], "bytes": len(r["body"])})
        emit("reader", r["status"], r["body"], a.url,
             not looks_blocked(r["status"], r["body"]))
    if a.mode == "wayback":
        snap = wayback_lookup(a.url)
        steps.append({"method": "wayback", "snapshot": snap})
        if snap:
            r = reader_fetch(snap)
            if looks_blocked(r["status"], r["body"]):
                r = http_get(snap, timeout=25)
            emit("wayback", r["status"], r["body"], snap,
                 not looks_blocked(r["status"], r["body"]))
        emit("wayback", 0, "", a.url, False)

    # auto: escalate, return the first method that yields real content.
    r = http_get(a.url, timeout=25)
    steps.append({"method": "direct", "status": r["status"], "bytes": len(r["body"])})
    if not looks_blocked(r["status"], r["body"]):
        if a.raw:
            emit("direct", r["status"], r["body"], r["url"], True)
        # direct gave HTML; reader usually returns cleaner text, but direct is fine
        emit("direct", r["status"], r["body"], r["url"], True)
    last = ("direct", r["status"], r["body"], r["url"])

    r = reader_fetch(a.url, fmt="html" if a.raw else None)
    steps.append({"method": "reader", "status": r["status"], "bytes": len(r["body"])})
    if not looks_blocked(r["status"], r["body"]):
        emit("reader", r["status"], r["body"], a.url, True)
    last = ("reader", r["status"], r["body"], a.url)

    snap = wayback_lookup(a.url)
    steps.append({"method": "wayback", "snapshot": snap})
    if snap:
        r = reader_fetch(snap)
        if looks_blocked(r["status"], r["body"]):
            r = http_get(snap, timeout=25)
        if not looks_blocked(r["status"], r["body"]):
            emit("wayback", r["status"], r["body"], snap, True)
        last = ("wayback", r["status"], r["body"], snap)

    # Nothing clean -- return the best body we saw, flagged not-ok.
    emit(last[0], last[1], last[2], last[3], False)


if __name__ == "__main__":
    main()
