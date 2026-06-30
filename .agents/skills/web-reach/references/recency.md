# Recency — "what are people saying lately"

This is the option-1 workflow: given a topic and a window, gather what was
posted recently across platforms, then synthesize honestly.

## The engine: `recent.py`

```bash
python3 scripts/recent.py "<topic>" --days 30 --n 8 --md
python3 scripts/recent.py "<topic>" --sources hn,github,lobsters,bsky
python3 scripts/recent.py "<topic>" --handles nasa,sama   # add specific X accounts
```

What it does:
- Fans the topic across the **keyless** sources that are reachable: Hacker News
  (stories in window, ranked by points), lobste.rs (recent matches), GitHub
  (repos pushed in window), optionally Bluesky (`searchPosts`), and any X handles
  you name (their recent tweets).
- Dedupes by URL and sorts by engagement (points/stars/likes), highest first.
- Reports unreachable sources in `skipped` and never fabricates items.

What it deliberately does **not** do: open-web search. That is the host
`web_search`'s job — see below.

## The full recipe (combine the layers)

1. **Platform firehoses:** run `recent.py` for the structured social/dev signal.
2. **Open web:** run the host `web_search` with a recency bound
   (`<topic> after:YYYY-MM-DD`, or "this week"/"latest"), collect links.
3. **Open the good ones:** `fetch.py` each promising URL `web_search` returns
   (news, blog posts, forum threads) since `web_fetch` may choke on them.
4. **Reddit/TikTok/etc.:** only if a backend is present (see `social.md`).
5. **Synthesize:** cluster by theme, note consensus vs. disagreement, attribute
   each claim to a dated source, and call out coverage gaps (what was skipped).

## Time windows

- `--days N` filters HN and GitHub by their native timestamps. For Bluesky and X
  handles, items are recent by nature; filter further by reading `when`.
- Match the window to intent: breaking news → 1–3 days; "current state" → 14–30;
  "has anything changed" → 30–90.
- Sort is engagement-first by default; when recency matters more than popularity,
  re-rank by the `when` field yourself.

## Honesty rules for synthesis

- Distinguish **volume** ("many posts mention X") from **truth** — popularity is
  not correctness, especially on social platforms.
- Show the spread: surface dissenting and minority takes, not just the top item.
- Keep every claim tied to a source URL + date so the user can verify.
- State the coverage limits plainly: which platforms were searched, which were
  blocked/skipped, and what a backend would have added.
- Never invent counts, quotes, dates, or posts to fill a thin result — a sparse
  but real answer beats a rich fabricated one.
