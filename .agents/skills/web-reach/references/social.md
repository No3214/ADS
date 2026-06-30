# Social platforms

Reachability varies a lot. The honest 2026 picture: X (read) and Bluesky are
doable keyless; Reddit, TikTok, and Instagram have largely closed the keyless
door and want a backend. Always confirm with `doctor.py`.

## X / Twitter — `x.py` (keyless)

Uses the public syndication endpoints that power embedded tweets.

```bash
python3 scripts/x.py user nasa --n 20     # an account's recent timeline
python3 scripts/x.py tweet 20             # a single tweet by id
```

- **Works keyless:** a known account's recent tweets (text, likes, retweets,
  replies, quotes, permalink) and any public tweet by id.
- **Does NOT work keyless:** keyword search across all of X, replies/threads,
  protected or suspended accounts.
- **Keyword search needs a backend:** xAI Grok live search (`XAI_API_KEY`),
  Apify/Bright Data/ScrapeCreators actors, or a logged-in twitter CLI.

Endpoints, if you need them raw:
- Timeline: `https://syndication.twitter.com/srv/timeline-profile/screen-name/<handle>`
  (tweets live in `__NEXT_DATA__` → `props.pageProps.timeline.entries[].content.tweet`).
- Single tweet: `https://cdn.syndication.twimg.com/tweet-result?id=<id>&lang=en&token=a`.

## Reddit — usually needs a backend now

Reddit blocks unauthenticated and datacenter traffic aggressively; `.json`
endpoints and even reader proxies frequently return 403 / "whoa there, pardner".

Try, in order:
1. **Discovery via host `web_search`** with `site:reddit.com <topic>` to find
   threads, then attempt `fetch.py` on each (works only where Reddit is not
   blocking that egress path).
2. **Official OAuth API** if you have a Reddit app: get a token from
   `https://www.reddit.com/api/v1/access_token`, then call
   `https://oauth.reddit.com/...` with `Authorization: Bearer`.
3. **A scraping backend:** Apify Reddit actors, Bright Data, or ScrapeCreators
   (`SCRAPECREATORS_API_KEY`). These are the reliable path for comments at scale.
4. **Old/RSS:** `https://www.reddit.com/r/<sub>/.rss` or `.../comments/<id>.rss`
   sometimes slips through; treat as best-effort and verify.

Do not fabricate Reddit content when blocked — report it and name the backend
that would unlock it.

## Bluesky — public AppView API (keyless, but IP-sensitive)

No login needed; some datacenter IPs get WAF-blocked (`doctor.py` will show it).

```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=topic&limit=25&sort=latest"
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=handle.bsky.social&limit=25"
```

`recent.py --sources bsky` uses `searchPosts` and degrades gracefully if blocked.

## TikTok / Instagram / Threads — backend required

There is no reliable keyless read path in 2026. Use a backend actor
(Apify / Bright Data / ScrapeCreators) keyed by the env var the doctor detects.
If none is present, tell the user this platform needs a connector and stop —
do not improvise fake engagement numbers.

## Mastodon / Lemmy / lobste.rs — open and friendly

Fediverse instances expose public APIs. lobste.rs is covered in `dev.md`.
Mastodon: `https://<instance>/api/v1/timelines/tag/<tag>` and
`https://<instance>/api/v2/search?q=...` are usually keyless per-instance.
