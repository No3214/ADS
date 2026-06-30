# Developer sources — GitHub, lobste.rs, registries

These are some of the most reliable keyless sources on the web.

## GitHub — `github.py`

```bash
python3 scripts/github.py repos "llm agent" --n 10 --sort stars
python3 scripts/github.py repo  openai/openai-python
python3 scripts/github.py user  torvalds
python3 scripts/github.py issues openai/openai-python --state open --n 10
python3 scripts/github.py file  openai/openai-python README.md --ref main
python3 scripts/github.py code  "def stream_response" --n 10   # needs GITHUB_TOKEN
```

Limits & keys:
- **Unauthenticated:** ~60 requests/hour (core) and ~10/min (search). Easy to
  exhaust during a session; the script reports `GitHub rate limit hit` clearly
  rather than pretending the repo/user does not exist.
- **`GITHUB_TOKEN` (or `GH_TOKEN`):** raises core to 5000/hr and **enables code
  search**, which is auth-only. Set it whenever you have one.
- Files are fetched via `raw.githubusercontent.com` (no rate limit); pass the
  correct branch/tag with `--ref` (e.g. `master` for the Linux kernel).

Useful raw endpoints:
- Releases as a feed: `https://github.com/<owner>/<repo>/releases.atom` → `feed.py`
- Commits as a feed: `https://github.com/<owner>/<repo>/commits/<branch>.atom`

## lobste.rs — keyless

```bash
curl -s "https://lobste.rs/newest.json"               # latest stories
curl -s "https://lobste.rs/t/ai.json"                 # a tag's stories
curl -s "https://lobste.rs/search.json?q=<query>"     # q only; extra params 400
```

The search JSON endpoint rejects `what`/`order` params (returns
"Unpermitted query or form parameter"). `recent.py` handles this by falling back
to filtering `newest.json` client-side, so just use `recent.py --sources lobsters`.

## Hacker News

See the routing table and `hn.py` — Algolia (`search`, `search_by_date`,
`items/<id>`) is open, fast, and the best recency signal for tech topics.

## Package registries (keyless JSON)

- npm: `https://registry.npmjs.org/<package>` (full metadata + versions).
- PyPI: `https://pypi.org/pypi/<package>/json`.
- crates.io: `https://crates.io/api/v1/crates/<crate>` (set a descriptive
  User-Agent; `lib.py` already sends one).

These are great for "latest version", maintenance status, dependency, and
download-trend questions without scraping.
