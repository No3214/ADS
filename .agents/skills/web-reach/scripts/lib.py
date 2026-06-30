#!/usr/bin/env python3
"""Shared HTTP helpers for web-reach scripts.

Pure Python standard library only -- no `pip install` required, so these scripts
run in any environment that has python3. Every function returns plain dicts and
never raises on HTTP errors, so callers can branch on `status` cleanly.
"""
import json
import sys
import gzip
import time
import os
import urllib.request
import urllib.parse
import urllib.error

DEFAULT_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0 Safari/537.36"
)


def http_get(url, headers=None, timeout=25, retries=2):
    """GET a URL. Returns {status:int, body:str, url:str, error?:str}.

    status == 0 means a transport-level failure (DNS, refused, blocked egress
    before an HTTP response, timeout). Never raises for 4xx/5xx -- those come
    back with the real status code and whatever body was returned.
    """
    h = {"User-Agent": DEFAULT_UA, "Accept": "*/*"}
    if headers:
        h.update(headers)
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=h)
            r = urllib.request.urlopen(req, timeout=timeout)
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return {"status": getattr(r, "status", r.getcode()),
                    "body": raw.decode("utf-8", "replace"), "url": r.geturl()}
        except urllib.error.HTTPError as e:
            body = ""
            try:
                raw = e.read()
                if e.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                body = raw.decode("utf-8", "replace")
            except Exception:
                pass
            return {"status": e.code, "body": body, "url": url}
        except Exception as e:  # noqa: BLE001
            last = str(e)
            time.sleep(0.8 * (attempt + 1))
    return {"status": 0, "body": "", "url": url, "error": last}


def http_json(url, headers=None, timeout=25, retries=2):
    """Like http_get but also parses JSON into r['json'] (None on failure)."""
    r = http_get(url, headers, timeout, retries)
    try:
        r["json"] = json.loads(r["body"]) if r["body"].strip() else None
    except Exception as e:  # noqa: BLE001
        r["json"] = None
        r["json_error"] = str(e)
    return r


def reader_fetch(url, timeout=45, fmt=None, no_cache=False):
    """Fetch a page through Jina Reader (https://r.jina.ai/<url>).

    Reader renders JavaScript server-side and returns clean markdown, which
    defeats most client-side rendering, soft anti-bot walls, and -- because the
    request only leaves to r.jina.ai -- many local egress blocks. Set
    JINA_API_KEY in the environment to raise rate limits / improve reliability.
    fmt can be 'markdown' (default), 'text', or 'html'.
    """
    headers = {}
    if fmt:
        headers["X-Return-Format"] = fmt
    if no_cache:
        headers["X-No-Cache"] = "true"
    key = os.environ.get("JINA_API_KEY")
    if key:
        headers["Authorization"] = "Bearer " + key
    return http_get("https://r.jina.ai/" + url, headers=headers, timeout=timeout)


def wayback_lookup(url, timeout=20):
    """Return the closest Wayback Machine snapshot URL, or None."""
    q = urllib.parse.quote(url, safe="")
    r = http_json("https://archive.org/wayback/available?url=" + q, timeout=timeout)
    try:
        snap = r["json"]["archived_snapshots"]["closest"]
        if snap.get("available"):
            return snap["url"]
    except Exception:
        pass
    return None


def strip_html(s, limit=None):
    """Crude tag stripper for embedded HTML snippets (HN comments, etc.)."""
    import re
    s = re.sub(r"<[^>]+>", "", s or "")
    s = (s.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
           .replace("&#x27;", "'").replace("&quot;", '"').replace("&#x2F;", "/"))
    return s[:limit] if limit else s


def out(obj, pretty=True):
    print(json.dumps(obj, ensure_ascii=False, indent=2 if pretty else None))


def eprint(*a):
    print(*a, file=sys.stderr)
