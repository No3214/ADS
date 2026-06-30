# Web pages — JS, anti-bot, walls, and dead links

Goal: turn any URL that `web_fetch` cannot open into clean, readable text.

## Default: `fetch.py`

```bash
python3 scripts/fetch.py "https://site.com/page"            # auto
python3 scripts/fetch.py "https://site.com/page" --max 8000 # cap length
python3 scripts/fetch.py "https://site.com/page" --raw      # raw HTML, not markdown
python3 scripts/fetch.py "https://site.com/page" --mode reader
python3 scripts/fetch.py "https://site.com/page" --mode wayback
```

Auto mode escalates direct → Jina Reader → Wayback and returns the first method
that yields real content. Inspect `steps[]` to see what happened.

## Jina Reader, directly

The reader is the single most useful primitive here.

```bash
curl -s "https://r.jina.ai/https://site.com/page"                 # markdown
curl -s -H "X-Return-Format: text" "https://r.jina.ai/https://…"  # plain text
curl -s -H "X-Return-Format: html" "https://r.jina.ai/https://…"  # cleaned HTML
curl -s -H "Authorization: Bearer $JINA_API_KEY" "https://r.jina.ai/https://…"
```

Why it works: it loads the page in a real headless browser on Jina's side, runs
the JavaScript, and returns the rendered result. That defeats client-side
rendering, lazy content, and many soft Cloudflare/anti-bot interstitials, and it
sidesteps *local* egress blocks because you only connect to `r.jina.ai`.

Limits: anonymous requests are rate-limited by IP reputation (you may see 401 /
429 on shared datacenter IPs). Set `JINA_API_KEY` when you have one. If the
**target itself** hard-blocks automated traffic (e.g. Reddit, some news sites),
the reader will surface the target's 403 — escalate to Wayback or a backend.

## Wayback Machine — dead, changed, or hostile pages

```bash
# nearest snapshot URL
curl -s "https://archive.org/wayback/available?url=https://site.com/page"
# then read it
python3 scripts/fetch.py "http://web.archive.org/web/2024/https://site.com/page"
```

Great for: deleted articles, edited pages (get an older version), and sites that
block live automated access but were archived earlier.

## Headers and etiquette

- A real browser User-Agent is set by default in `lib.py`; some sites need it.
- Be gentle: a couple of requests, not a crawl. The scripts already retry with
  backoff on transport errors.
- Never put secrets in URLs, and never submit forms or click irreversible
  actions when fetching on someone's behalf.

## When direct + reader + Wayback all fail

That usually means a hard anti-bot wall or auth requirement. Options, in order:

1. A managed backend if present: Exa `/contents`, Tavily `extract`, or Bright
   Data / Apify (see `references/search.md` and `references/social.md`).
2. Find an alternate source for the same content (mirror, cache, official API,
   press release, or an RSS feed via `feed.py`).
3. Tell the user it is not retrievable keyless and what backend would unlock it.
