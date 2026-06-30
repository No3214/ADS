#!/usr/bin/env python3
"""'What are people saying lately?' -- fan a topic out across the keyless
sources that are reachable, keep recent high-signal items, dedupe, and emit a
consolidated result. Unreachable sources are skipped and reported, never faked.

Usage:
  recent.py "<topic>" [--days 30] [--n 8] [--sources hn,lobsters,github]
                       [--handles nasa,sama] [--md]

Sources:
  hn        Hacker News stories in window, ranked by points       (keyless)
  lobsters  lobste.rs recent stories matching the topic           (keyless)
  github    repositories matching the topic, recently pushed      (keyless)
  bsky      Bluesky posts matching the topic                      (keyless; may be WAF-blocked)
  handles   recent tweets from specific X accounts you name        (keyless)

This engine deliberately does NOT do open web search -- finding arbitrary URLs
is the host's built-in web_search job. Run those, then fetch each result with
fetch.py. This engine covers the platform firehoses that web_search misses.
"""
import argparse
import sys
import os
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import http_json, http_get, out  # noqa: E402


def from_hn(topic, days, n):
    since = int(time.time()) - days * 86400
    params = urllib.parse.urlencode({
        "query": topic, "tags": "story",
        "numericFilters": "created_at_i>%d" % since,
        "hitsPerPage": str(n)})
    url = "https://hn.algolia.com/api/v1/search?" + params
    j = http_json(url).get("json") or {}
    return [{"source": "hn", "title": h.get("title"), "url": h.get("url"),
             "engagement": h.get("points"), "comments": h.get("num_comments"),
             "when": h.get("created_at"),
             "discuss": "https://news.ycombinator.com/item?id=%s" % h.get("objectID")}
            for h in j.get("hits", []) if h.get("title")]


def from_lobsters(topic, n):
    r = http_json("https://lobste.rs/search.json?q=%s" % urllib.parse.quote(topic))
    rows = r.get("json") if isinstance(r.get("json"), list) else None
    if rows is None:  # search endpoint rejected the query; filter the newest feed
        nj = http_json("https://lobste.rs/newest.json").get("json")
        tl = topic.lower()
        rows = [s for s in (nj or [])
                if tl in ((s.get("title") or "") + (s.get("url") or "")).lower()]
    out_ = []
    for s in (rows or [])[:n]:
        out_.append({"source": "lobsters", "title": s.get("title"),
                     "url": s.get("url"), "engagement": s.get("score"),
                     "comments": s.get("comment_count"),
                     "when": s.get("created_at"),
                     "discuss": s.get("short_id_url") or s.get("comments_url")})
    return out_


def from_github(topic, days, n):
    q = "%s pushed:>%s" % (
        topic, time.strftime("%Y-%m-%d", time.gmtime(time.time() - days * 86400)))
    url = ("https://api.github.com/search/repositories?q=%s&sort=updated&per_page=%d"
           % (urllib.parse.quote(q), n))
    h = {"Accept": "application/vnd.github+json"}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        h["Authorization"] = "Bearer " + tok
    j = http_json(url, headers=h).get("json") or {}
    return [{"source": "github", "title": r["full_name"],
             "url": r["html_url"], "engagement": r["stargazers_count"],
             "comments": r.get("open_issues_count"), "when": r.get("pushed_at"),
             "discuss": r["html_url"]}
            for r in j.get("items", [])]


def from_bsky(topic, n):
    url = ("https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts"
           "?q=%s&limit=%d&sort=latest" % (urllib.parse.quote(topic), n))
    r = http_json(url)
    posts = (r.get("json") or {}).get("posts")
    if posts is None:
        return None  # signals unreachable/blocked
    return [{"source": "bsky",
             "title": (p.get("record", {}).get("text", "") or "")[:140],
             "url": "https://bsky.app/profile/%s/post/%s"
                    % (p["author"]["handle"], p["uri"].rsplit("/", 1)[-1]),
             "engagement": p.get("likeCount"), "comments": p.get("replyCount"),
             "when": p.get("indexedAt"), "discuss": None}
            for p in posts]


def from_handles(handles, n):
    import re
    import json
    items = []
    for handle in handles:
        handle = handle.strip().lstrip("@")
        u = ("https://syndication.twitter.com/srv/timeline-profile/screen-name/"
             + handle)
        b = http_get(u, timeout=25)["body"]
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', b, re.S)
        if not m:
            continue
        try:
            ents = json.loads(m.group(1))["props"]["pageProps"]["timeline"]["entries"]
        except Exception:
            continue
        for e in ents[:n]:
            t = e.get("content", {}).get("tweet")
            if not t:
                continue
            items.append({"source": "x:@%s" % handle,
                          "title": (t.get("full_text") or t.get("text") or "")[:160],
                          "url": "https://x.com/%s/status/%s" % (handle, t.get("id_str")),
                          "engagement": t.get("favorite_count"),
                          "comments": t.get("reply_count"),
                          "when": t.get("created_at"), "discuss": None})
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--sources", default="hn,lobsters,github")
    ap.add_argument("--handles", default="")
    ap.add_argument("--md", action="store_true")
    a = ap.parse_args()

    want = [s.strip() for s in a.sources.split(",") if s.strip()]
    items, skipped = [], []

    def run(name, fn):
        try:
            res = fn()
            if res is None:
                skipped.append({"source": name, "reason": "unreachable/blocked"})
            else:
                items.extend(res)
        except Exception as e:  # noqa: BLE001
            skipped.append({"source": name, "reason": str(e)})

    if "hn" in want:
        run("hn", lambda: from_hn(a.topic, a.days, a.n))
    if "lobsters" in want:
        run("lobsters", lambda: from_lobsters(a.topic, a.n))
    if "github" in want:
        run("github", lambda: from_github(a.topic, a.days, a.n))
    if "bsky" in want:
        run("bsky", lambda: from_bsky(a.topic, a.n))
    if a.handles:
        run("handles", lambda: from_handles(a.handles.split(","), a.n))

    # dedupe by url, sort by engagement desc (None last)
    seen, deduped = set(), []
    for it in items:
        k = it.get("url")
        if k and k in seen:
            continue
        seen.add(k)
        deduped.append(it)
    deduped.sort(key=lambda x: (x.get("engagement") or -1), reverse=True)

    if a.md:
        print("# What people are saying about: %s (last %d days)\n" % (a.topic, a.days))
        for it in deduped:
            eng = it.get("engagement")
            print("- **[%s]** %s%s" % (
                it["source"], it["title"] or it["url"],
                "  _(%s)_" % eng if eng is not None else ""))
            if it.get("url"):
                print("  %s" % it["url"])
        if skipped:
            print("\n_Skipped sources: %s_" % ", ".join(
                "%s (%s)" % (s["source"], s["reason"]) for s in skipped))
        return

    out({"ok": True, "topic": a.topic, "days": a.days,
         "count": len(deduped), "items": deduped, "skipped": skipped})


if __name__ == "__main__":
    main()
