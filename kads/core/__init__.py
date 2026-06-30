#!/usr/bin/env python3
"""
kads.core — paylasilan altyapi: config yukleme, cikti bicimlendirme, cikis kodlari.

Tasarim ilkeleri (OpenCLI + Agent-Reach'ten esinlenildi):
  - Deterministik cikti: ayni komut, ayni sema. Pipe'lanabilir, script'lenebilir.
  - --format table|json|yaml|md|csv her komutta calisir.
  - Unix sysexits.h cikis kodlari (CI ve shell ile dogal entegrasyon).
  - Sifir zorunlu bagimlilik: PyYAML kurulu olmasa da calisir (mini-parser).
  - Secret'lar asla yazdirilmaz; maskelenir.

Tek kaynak: tum kampanya verisi kads/data.py icindedir.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT / ".env"
CONFIG_FILE = ROOT / "config" / "ads-assets.yaml"

# ---- Unix sysexits.h cikis kodlari (OpenCLI deseni) ------------------------
EX_OK = 0  # Basarili
EX_GENERIC = 1  # Genel/siniflandirilmamis hata
EX_USAGE = 2  # Hatali arguman / bilinmeyen komut
EX_NOINPUT = 66  # Bos sonuc (EX_NOINPUT)
EX_UNAVAILABLE = 69  # Servis yok (ornegin MCP baglanmamis)
EX_TEMPFAIL = 75  # Gecici hata, tekrar dene
EX_NOPERM = 77  # Yetki/onay gerekli (EX_NOPERM)
EX_CONFIG = 78  # Eksik kimlik veya hatali config (EX_CONFIG)

# ---- ANSI renkler (TTY ise) ------------------------------------------------
_TTY = sys.stdout.isatty() and os.getenv("NO_COLOR") is None


def _c(code: str, s: str) -> str:
    return f"\033[{code}m{s}\033[0m" if _TTY else s


def green(s: str) -> str:
    return _c("32", s)


def red(s: str) -> str:
    return _c("31", s)


def yellow(s: str) -> str:
    return _c("33", s)


def cyan(s: str) -> str:
    return _c("36", s)


def bold(s: str) -> str:
    return _c("1", s)


def dim(s: str) -> str:
    return _c("2", s)


# ---- Mini .env okuyucu (bagimliliksiz) -------------------------------------
def load_env(path: Path = ENV_FILE) -> dict:
    """Once gercek ortam degiskenleri, sonra .env dosyasi (varsa). Dosya degerleri
    ortam degiskenlerini EZMEZ (ortam onceliklidir)."""
    data: dict[str, str] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            data[k.strip()] = v.split(" #", 1)[0].strip().strip('"').strip("'")
    # Ortam degiskenleri onceliklidir.
    for k in list(data) + [
        "GA4_MEASUREMENT_ID",
        "GOOGLE_ADS_TAG_ID",
        "META_PIXEL_ID",
        "META_BUSINESS_ID",
        "GTM_CONTAINER_ID",
        "META_AD_ACCOUNT_ID",
        "GOOGLE_ADS_CUSTOMER_ID",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID",
        "GOOGLE_PROJECT_ID",
        "GOOGLE_ADS_DEVELOPER_TOKEN",
        "GOOGLE_MONTHLY_BUDGET_TRY",
        "META_MONTHLY_BUDGET_TRY",
        "GOOGLE_AVG_DAILY_BUDGET_TRY",
        "META_DAILY_BUDGET_TRY",
        "ADS_WRITES_ENABLED",
    ]:
        if os.getenv(k) is not None:
            data[k] = os.getenv(k, "")
    return data


SECRET_HINT = re.compile(r"(token|secret|password|credential|refresh)", re.I)


def mask(key: str, value: str) -> str:
    """Secret benzeri anahtarlarin degerini maskeler."""
    if not value:
        return ""
    if SECRET_HINT.search(key):
        return "***gizli***" if value not in ("replace-me", "") else value
    return value


def is_placeholder(value: str) -> bool:
    if not value:
        return True
    v = value.strip().lower()
    return v in ("", "replace-me", "act_replace_me", "xxx-xxx-xxxx") or "replace" in v


# ---- Cikti bicimlendirici (table|json|yaml|md|csv) -------------------------
def emit(
    rows: list[dict],
    fmt: str = "table",
    title: str | None = None,
    columns: list[str] | None = None,
) -> None:
    """Bir kayit listesini istenen bicimde stdout'a yazar. Deterministik."""
    fmt = (fmt or "table").lower()
    if not rows:
        if fmt == "json":
            print("[]")
        else:
            print(dim("(veri yok)"))
        return
    cols = columns or list(rows[0].keys())

    if fmt == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif fmt == "csv":
        import csv
        import io

        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})
        sys.stdout.write(buf.getvalue())
    elif fmt == "yaml":
        for r in rows:
            print("-")
            for c in cols:
                print(f"  {c}: {_yaml_scalar(r.get(c, ''))}")
    elif fmt == "md":
        print(f"### {title}\n" if title else "")
        print("| " + " | ".join(cols) + " |")
        print("| " + " | ".join("---" for _ in cols) + " |")
        for r in rows:
            print(
                "| "
                + " | ".join(str(r.get(c, "")).replace("|", "\\|") for c in cols)
                + " |"
            )
    else:  # table
        if title:
            print(bold(cyan(title)))
        widths = {
            c: max(len(str(c)), *(len(str(r.get(c, ""))) for r in rows)) for c in cols
        }
        header = "  ".join(bold(str(c).ljust(widths[c])) for c in cols)
        print(header)
        print(dim("  ".join("-" * widths[c] for c in cols)))
        for r in rows:
            print("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))


def _yaml_scalar(v) -> str:
    s = str(v)
    if s == "" or re.search(r"[:#\[\]{}\"']", s):
        return json.dumps(s, ensure_ascii=False)
    return s


def kv(title: str, pairs: list[tuple[str, str]], fmt: str = "table") -> None:
    """Anahtar-deger bloklarini bicimlendirir."""
    rows = [{"alan": k, "deger": v} for k, v in pairs]
    emit(rows, fmt=fmt, title=title, columns=["alan", "deger"])


def banner(text: str) -> None:
    try:
        line = "─" * (len(text) + 2)
        print(cyan(f"┌{line}┐"))
        print(cyan("│ ") + bold(text) + cyan(" │"))
        print(cyan(f"└{line}┘"))
    except UnicodeEncodeError:
        # Konsol UTF-8 degilse ASCII'ye dus (cp1254 vb. cokmesin).
        line = "-" * (len(text) + 2)
        print(cyan(f"+{line}+"))
        print(cyan("| ") + bold(text) + cyan(" |"))
        print(cyan(f"+{line}+"))
