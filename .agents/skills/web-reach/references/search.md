# Discovery (search) — find URLs to then fetch

web-reach is a **fetch** layer. For finding URLs, use search in this priority
order. Do not reinvent search inside this skill.

## 1. The host's built-in `web_search` (first choice)

If you are running with a `web_search` tool, it is almost always the best and
cheapest way to find candidate URLs. Use it, collect the links, then open the
hard ones with `scripts/fetch.py` or a platform script. This division — search
to discover, web-reach to fetch — is the intended workflow.

Targeted discovery patterns that pair well with fetch:
- `site:reddit.com <topic>` → then try to open threads.
- `<topic> after:2026-05-01` → recency-bounded.
- `<product> changelog` / `release notes` → often an RSS feed for `feed.py`.

## 2. Managed search backends (if keys/connectors exist)

`doctor.py` will flag these. They shine for semantic discovery and for returning
page **content** alongside links:

- **Exa** (`EXA_API_KEY`): `POST https://api.exa.ai/search` (neural/keyword), and
  `POST https://api.exa.ai/contents` to get clean text for result URLs in one
  step. Excellent for "find the best pages about X".
- **Tavily** (`TAVILY_API_KEY`): `POST https://api.tavily.com/search` with
  `include_raw_content`, and `/extract` for specific URLs.
- **Perplexity** (`PERPLEXITY_API_KEY`): answer-style search with citations via
  the chat completions API (`sonar` models) — good for a sourced synthesis.
- **Brave** (`BRAVE_API_KEY`): `https://api.search.brave.com/res/v1/web/search`
  classic web results.

## 3. Keyless engine scraping (last resort — often weak)

Without keys and without the host search, keyless web search is unreliable: many
engines return empty or challenge pages to datacenter IPs. If you must:

- DuckDuckGo HTML: `https://html.duckduckgo.com/html/?q=<query>` (POST the form
  for results; GET often returns just the form on flagged IPs).
- DuckDuckGo Lite: `https://lite.duckduckgo.com/lite/?q=<query>`.
- SearXNG public instances: `https://<instance>/search?q=<query>&format=json`.
- Reader-proxied search: `https://r.jina.ai/https://www.bing.com/search?q=<query>`
  (works only when the reader is not rate-limited on this IP).

Treat keyless search results as low-confidence and verify by fetching the pages.
`doctor.py` does not probe search engines, so test once before relying on them.

## Choosing

- Have host `web_search`? Use it. Done.
- No host search but have Exa/Tavily/Perplexity/Brave? Use the best available.
- Neither? Try keyless engines, expect gaps, and lean on the platform scripts
  (`hn.py`, `github.py`, `x.py`, `recent.py`) which do not need a search engine.
