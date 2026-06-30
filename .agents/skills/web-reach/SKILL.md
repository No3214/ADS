---
name: web-reach
description: Reach web content that the built-in web_search and web_fetch cannot retrieve, and answer "what are people saying lately" across platforms. Use this whenever a normal fetch comes back blocked, empty, JavaScript-only, login-walled, anti-bot, or paywalled; when the user shares or asks about a Reddit thread, an X/Twitter post or account, a YouTube transcript, a Hacker News discussion, a GitHub repo/issue/file, TikTok, Bluesky, an RSS feed, or an archived or dead page; when the user says you "couldn't open" a link, wants the comments or the transcript, or wants a deep dive; and when the request is recency-driven (last N days, this week, latest, current sentiment) about any topic. Keyless by default, with optional Exa, Tavily, Apify, Bright Data, or Perplexity backends when their keys are present. Run scripts/doctor.py first to see what works in the current environment.
license: Proprietary. LICENSE.txt has complete terms.
---

# web-reach

Reach into the parts of the internet the built-in tools cannot, and pull the
content back as clean, structured text. Two jobs:

1. **Fetch one hard target** — a specific URL or platform object (Reddit thread,
   X account, YouTube transcript, JS-rendered or anti-bot page, archived page).
2. **Survey recent chatter** — "what are people saying about X in the last N
   days" across several platform firehoses at once.

## When this earns its place

The built-in `web_fetch` is good at static, public, friendly pages, and
`web_search` is good at finding URLs. Reach for **web-reach** the moment that
breaks down:

- A fetch returns blocked / empty / a cookie or CAPTCHA wall / "enable
  JavaScript" / 403 / "just a moment".
- The user pastes a link and you "can't open it" — try harder here.
- The target is a **platform object**: Reddit comments, an X/Twitter post or
  timeline, a YouTube transcript, a Hacker News thread, a GitHub repo/issue/file,
  a TikTok or Bluesky post, an RSS feed.
- The user wants **the comments**, **the transcript**, or a **deep dive**.
- The request is **recency-driven**: "last 30 days", "this week", "latest",
  "what's the current take on…".

## Core mental model: discovery vs fetch

Keep these two separate.

- **Discovery (finding URLs)** is the host's built-in `web_search` job. It is
  usually the best available search. Use it to locate candidate URLs.
- **Fetch / extract (opening the hard ones)** is **this skill's** job. Once you
  have a URL that `web_fetch` chokes on, bring it here.

So the normal flow for "research X" is: built-in `web_search` to find links →
`scripts/fetch.py` (or a platform script) to actually read the ones that resist.
For "what are people saying", add `scripts/recent.py` to sweep the platform
firehoses that `web_search` does not surface well.

## Step 0 — always run the doctor first

Egress policy, IP reputation, installed tools, and available API keys differ in
every environment. Do not assume a method works. Probe:

```bash
python3 scripts/doctor.py          # human summary + routing advice
python3 scripts/doctor.py --json   # machine-readable
```

It reports which tools exist, which keys/backends are set, and which techniques
are live right now, then tells you how to route. If a fetch later fails
unexpectedly, run it again — the environment may differ from your expectation.

## Routing table

| You need… | Use | Notes |
|---|---|---|
| Any single URL that `web_fetch` can't open | `fetch.py <url>` | auto-escalates direct → Jina Reader → Wayback |
| A JS-rendered / anti-bot / geo / login-walled page | `fetch.py <url>` | Reader renders server-side and returns markdown |
| A dead / removed / changed page | `fetch.py <url> --mode wayback` | nearest archived snapshot |
| X/Twitter account timeline or one tweet | `x.py user <handle>` / `x.py tweet <id>` | keyless; keyword search needs a backend |
| Hacker News search or a thread's comments | `hn.py search <q> [--recent]` / `hn.py thread <id>` | open Algolia API, excellent recency |
| GitHub repo / repos / code / issues / user / file | `github.py …` | set `GITHUB_TOKEN` for higher limits + code search |
| An RSS/Atom feed (blog, news, channel, releases) | `feed.py <url>` | reader fallback if the host blocks us |
| "What are people saying lately about X" | `recent.py "<topic>" --days N` | fan-out across reachable platforms |
| Reddit, TikTok, Instagram, Threads | see `references/social.md` | usually needs a backend/key now |
| YouTube transcript | see `references/video.md` | yt-dlp / captionTracks / backend |

All scripts are pure-Python (stdlib only) and print JSON to stdout; `recent.py`
also has `--md`. Each prints its own `--help`.

## Quick start (the keyless workhorses)

```bash
# 1) Read a stubborn page as clean markdown
python3 scripts/fetch.py "https://example.com/js-heavy" --max 8000

# 2) Read an X account or a single tweet (no key)
python3 scripts/x.py user nasa --n 20
python3 scripts/x.py tweet 1789123456789

# 3) Hacker News: recent discussion + a thread's comments
python3 scripts/hn.py search "vector database" --recent --days 14 --min-points 20
python3 scripts/hn.py thread 39495591

# 4) GitHub
python3 scripts/github.py repos "llm agent framework" --n 10
python3 scripts/github.py file openai/openai-python README.md

# 5) Recency sweep across platforms, rendered as a brief
python3 scripts/recent.py "local-first software" --days 30 --md
python3 scripts/recent.py "mars" --sources hn,github --handles nasa,esa --md
```

## Recency mode in depth

`recent.py` fans a topic across the **keyless** sources that are reachable (Hacker
News, lobste.rs, GitHub, optionally Bluesky, plus any X handles you name),
dedupes by URL, and sorts by engagement. It deliberately does **not** do open
web search — pair it with the host's `web_search` for the open web, then
`fetch.py` each result. Unreachable sources are reported in `skipped`, never
faked. Full methodology, time-window handling, and synthesis guidance:
`references/recency.md`.

## Optional backends (use them if the doctor finds them)

Keyless covers a lot, but a few platforms (Reddit, TikTok, Instagram, X keyword
search, reliable YouTube transcripts) are locked down. If the environment has a
key or connector, prefer it for those targets:

- `JINA_API_KEY` — higher-rate, more reliable page fetching.
- `GITHUB_TOKEN` — GitHub code search and 5000/hr limits.
- Exa / Tavily / Perplexity — strong neural search + extraction (discovery).
- Apify / Bright Data / ScrapeCreators — Reddit, TikTok, Instagram, YouTube.
- xAI Grok — live X keyword search.

`references/search.md` and `references/social.md` show exactly when and how to
fall back to each.

## Working rules

- **Workspace.** Do scratch work in `/tmp` and cache under `~/.web-reach`. Do not
  write into the conversation's working/output directory unless the user asked
  for a saved file.
- **Never fabricate.** If a source is blocked or returns nothing, say so and show
  the `skipped`/`steps` evidence. Do not invent posts, counts, dates, or quotes.
- **Cite and date.** Carry the source URL and timestamp through to your answer so
  the user can verify.
- **Copyright.** Quote sparingly (a short phrase, attributed); summarize in your
  own words. Never reproduce full articles, transcripts, or lyrics.
- **Degrade gracefully.** Try the keyless path, escalate to reader/Wayback, then
  to a backend; report what finally worked and what did not.

## Reference files

Read the matching file when you go deep on a category:

- `references/overview.md` — the routing model and how the pieces fit.
- `references/web.md` — arbitrary pages: reader, Wayback, headers, anti-bot.
- `references/social.md` — X, Reddit, Bluesky, TikTok, Instagram, Threads.
- `references/video.md` — YouTube transcripts and podcasts.
- `references/dev.md` — GitHub, lobste.rs, package registries.
- `references/search.md` — discovery: built-in search first, then fallbacks.
- `references/recency.md` — the "last N days" methodology.
