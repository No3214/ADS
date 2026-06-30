#!/usr/bin/env python3
"""GitHub via the REST API. repo/repos/issues/user/file work keyless at a low
rate limit; set GITHUB_TOKEN in the environment for higher limits and to enable
`code` search (code search requires authentication).

Usage:
  github.py repos <query> [--n 10] [--sort stars|updated|forks]
  github.py repo  <owner/name>
  github.py code  <query> [--n 10]          # needs GITHUB_TOKEN
  github.py issues <owner/name> [--state open|closed|all] [--n 10]
  github.py user  <login>
  github.py file  <owner/name> <path> [--ref main]
"""
import argparse
import sys
import os
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import http_json, http_get, out  # noqa: E402

API = "https://api.github.com"


def _headers():
    h = {"Accept": "application/vnd.github+json"}
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        h["Authorization"] = "Bearer " + tok
    return h


def _limited(j):
    return (isinstance(j, dict) and isinstance(j.get("message"), str)
            and "rate limit" in j["message"].lower())


_RL = {"ok": False, "error": "GitHub rate limit hit -- set GITHUB_TOKEN for 5000/hr"}


def repos(q, n, sort):
    url = "%s/search/repositories?q=%s&per_page=%d&sort=%s" % (
        API, urllib.parse.quote(q), n, sort)
    j = (http_json(url, headers=_headers()).get("json") or {})
    if _limited(j):
        return _RL
    items = [{
        "full_name": r["full_name"], "stars": r["stargazers_count"],
        "desc": r.get("description"), "lang": r.get("language"),
        "updated": r.get("pushed_at"), "url": r["html_url"],
    } for r in j.get("items", [])]
    return {"ok": True, "count": len(items), "total": j.get("total_count"),
            "items": items}


def repo(name):
    j = http_json("%s/repos/%s" % (API, name), headers=_headers()).get("json")
    if _limited(j):
        return _RL
    if not j or "full_name" not in j:
        return {"ok": False, "error": "repo not found: %s" % name}
    return {"ok": True, "full_name": j["full_name"], "stars": j["stargazers_count"],
            "forks": j["forks_count"], "open_issues": j["open_issues_count"],
            "desc": j.get("description"), "lang": j.get("language"),
            "topics": j.get("topics"), "updated": j.get("pushed_at"),
            "homepage": j.get("homepage"), "url": j["html_url"]}


def code(q, n):
    if not (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")):
        return {"ok": False, "error": "code search requires GITHUB_TOKEN"}
    url = "%s/search/code?q=%s&per_page=%d" % (API, urllib.parse.quote(q), n)
    j = (http_json(url, headers=_headers()).get("json") or {})
    if _limited(j):
        return _RL
    items = [{"repo": r["repository"]["full_name"], "path": r["path"],
              "url": r["html_url"]} for r in j.get("items", [])]
    return {"ok": True, "count": len(items), "total": j.get("total_count"),
            "items": items}


def issues(name, state, n):
    url = "%s/repos/%s/issues?state=%s&per_page=%d" % (API, name, state, n)
    j = http_json(url, headers=_headers()).get("json") or []
    items = [{"number": i["number"], "title": i["title"], "state": i["state"],
              "comments": i["comments"], "user": i["user"]["login"],
              "is_pr": "pull_request" in i, "url": i["html_url"]}
             for i in j if isinstance(i, dict)]
    return {"ok": True, "count": len(items), "items": items}


def user(login):
    j = http_json("%s/users/%s" % (API, login), headers=_headers()).get("json")
    if _limited(j):
        return _RL
    if not j or "login" not in j:
        return {"ok": False, "error": "user not found: %s" % login}
    return {"ok": True, "login": j["login"], "name": j.get("name"),
            "bio": j.get("bio"), "followers": j.get("followers"),
            "public_repos": j.get("public_repos"), "company": j.get("company"),
            "blog": j.get("blog"), "url": j["html_url"]}


def file(name, path, ref):
    raw = "https://raw.githubusercontent.com/%s/%s/%s" % (name, ref, path)
    r = http_get(raw, timeout=25)
    if r["status"] == 200:
        return {"ok": True, "source": raw, "content": r["body"]}
    return {"ok": False, "status": r["status"], "source": raw,
            "error": "not found (check --ref branch/tag)"}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("repos"); p.add_argument("query"); p.add_argument("--n", type=int, default=10); p.add_argument("--sort", default="stars")
    p = sub.add_parser("repo"); p.add_argument("name")
    p = sub.add_parser("code"); p.add_argument("query"); p.add_argument("--n", type=int, default=10)
    p = sub.add_parser("issues"); p.add_argument("name"); p.add_argument("--state", default="open"); p.add_argument("--n", type=int, default=10)
    p = sub.add_parser("user"); p.add_argument("login")
    p = sub.add_parser("file"); p.add_argument("name"); p.add_argument("path"); p.add_argument("--ref", default="main")
    a = ap.parse_args()
    if a.cmd == "repos":
        out(repos(a.query, a.n, a.sort))
    elif a.cmd == "repo":
        out(repo(a.name))
    elif a.cmd == "code":
        out(code(a.query, a.n))
    elif a.cmd == "issues":
        out(issues(a.name, a.state, a.n))
    elif a.cmd == "user":
        out(user(a.login))
    elif a.cmd == "file":
        out(file(a.name, a.path, a.ref))


if __name__ == "__main__":
    main()
