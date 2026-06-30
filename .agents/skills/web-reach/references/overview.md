# Overview — how web-reach fits together

## The one idea

The host already has two strong tools: `web_search` (find URLs) and `web_fetch`
(open easy pages). web-reach fills the gap they leave: **opening the pages and
platform objects that resist, and sweeping the platform firehoses that search
does not surface.** Do not duplicate the host's search inside this skill — drive
discovery with `web_search`, then hand the hard URLs to web-reach.

## Decision flow

```
Need internet content
        │
        ├─ Don't have a URL yet? ─────────► host web_search to find candidates
        │
        ├─ Have a URL, web_fetch worked? ─► just use what web_fetch returned
        │
        ├─ Have a URL, web_fetch failed? ─► scripts/fetch.py <url>   (auto-escalates)
        │
        ├─ It's a known platform object? ─► the platform script:
        │        x.py · hn.py · github.py · feed.py   (+ social.md / video.md)
        │
        └─ "What are people saying lately?" ─► scripts/recent.py "<topic>" --days N
                                               (plus web_search + fetch.py for the open web)
```

## Why a doctor step exists

The same command can succeed in one environment and 403 in another, because
egress policy and datacenter-IP reputation differ. Three things vary:

1. **Tools** — `yt-dlp`, `gh`, `node`, `ffmpeg` may or may not be installed.
2. **Keys/backends** — `JINA_API_KEY`, `GITHUB_TOKEN`, Exa/Tavily/Apify/etc.
3. **Connectivity** — some hosts (Reddit, Bluesky, YouTube) are blocked on some
   egress paths even though the technique is sound.

`scripts/doctor.py` measures all three and prints routing advice. Run it first
and whenever something fails unexpectedly.

## Tiered fetch strategy (what `fetch.py` does)

1. **Direct** — plain HTTP with a real browser User-Agent. Fast; works for most
   static/public pages.
2. **Jina Reader** (`https://r.jina.ai/<url>`) — renders JavaScript server-side,
   returns clean markdown, and because the request only leaves to `r.jina.ai`, it
   also slips past many *local* egress blocks and soft anti-bot walls. Set
   `JINA_API_KEY` for reliability; anonymous use can be rate-limited per IP.
3. **Wayback** — if the live page is dead or hostile, fetch the nearest Internet
   Archive snapshot.

`fetch.py` records each attempt in `steps[]` so the path is auditable, and only
reports `ok:true` when it actually got usable content.

## Output discipline

Every script prints JSON (and `recent.py` offers `--md`). When you turn results
into an answer: keep the source URL and timestamp, summarize in your own words,
quote only short attributed phrases, and surface anything that was `skipped` or
`blocked` so the user knows the coverage limits.
