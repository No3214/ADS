#!/usr/bin/env python3
"""
kads.platforms.google — Google Ads Editor icin import-hazir CSV ureteci.

Resmi Google Ads MCP yalnizca OKUMA yapar; yazma icin en guvenli yol Google Ads
Editor CSV import'tur (elle review + post). Bu modul, data.py'deki tek kaynaktan
Editor'un tanidigi sutunlarla CSV'ler uretir. TUM kampanyalar PAUSED olusturulur.

Ciktilar (out/google-editor/):
  01_campaigns.csv            Kampanyalar (PAUSED, gunluk butce, Maximize Clicks)
  02_ad_groups.csv            Reklam gruplari
  03_keywords.csv             Anahtar kelimeler (Phrase/Exact)
  04_responsive_search_ads.csv  RSA (Headline 1..15, Description 1..4)
  05_negative_keywords.csv    Hesap/kampanya negatifleri
  06_sitelinks.csv            Sitelink uzantilari
  07_callouts.csv             Callout uzantilari
  08_structured_snippets.csv  Yapilandirilmis snippet uzantilari
  IMPORT_REHBERI.md           Adim adim import talimati

Import (Google Ads Editor): Account > Import > "From file" (veya "Make multiple
changes" > paste). Posttan ONCE her seyi review et. Hicbir kampanya otomatik
ENABLED olmaz.
"""

from __future__ import annotations

import csv
from pathlib import Path

from kads import data
from kads import data_ext as dx

# Kampanya tanimlari: (kampanya adi, gunluk TRY, reklam gruplari)
CAMPAIGNS = [
    ("Kozbeyli | Marka | Search", 148, ["Marka"]),
    (
        "Kozbeyli | NonBrand | Search",
        296,
        ["NonBrand-Foca-Butik", "NonBrand-Foca-Genel", "NonBrand-Niche"],
    ),
    ("Kozbeyli | Test | Search", 49, ["NonBrand-Foca-Genel"]),
]
DEFAULT_MAX_CPC_TRY = 6.0  # CPC ust siniri (TR ortalama ~10,5 TL; marka cok altinda)


def _match_to_editor(term: str, match: str) -> tuple[str, str]:
    """(keyword_text, match_type) — Editor 'Phrase'/'Exact' bekler."""
    if match == "exact":
        return term, "Exact"
    if match == "phrase_and_exact":
        return term, "Phrase"  # ayrica Exact satiri da eklenir (asagida)
    return term, "Phrase"


def campaigns_rows() -> list[dict]:
    rows = []
    for name, daily, _ in CAMPAIGNS:
        rows.append(
            {
                "Campaign": name,
                "Campaign Type": "Search",
                "Status": "Paused",
                "Budget": f"{daily:.2f}",
                "Budget Type": "Daily",
                "Bid Strategy Type": "Maximize clicks",
                "Max CPC Bid Limit": f"{DEFAULT_MAX_CPC_TRY:.2f}",
                "Networks": "Google search",
                "Languages": "Turkish",
                "Location": "; ".join(data.GEO_TARGETS),
            }
        )
    return rows


def ad_groups_rows() -> list[dict]:
    rows = []
    for name, _, groups in CAMPAIGNS:
        for g in groups:
            rows.append(
                {
                    "Campaign": name,
                    "Ad Group": g,
                    "Status": "Paused",
                    "Default Max. CPC": f"{DEFAULT_MAX_CPC_TRY:.2f}",
                }
            )
    return rows


def keywords_rows() -> list[dict]:
    rows = []
    for name, _, groups in CAMPAIGNS:
        for g in groups:
            spec = data.KEYWORDS[g]
            for term in spec["terms"]:
                kw, mt = _match_to_editor(term, spec["match"])
                rows.append(
                    {
                        "Campaign": name,
                        "Ad Group": g,
                        "Keyword": kw,
                        "Match Type": mt,
                        "Status": "Paused",
                    }
                )
                if spec["match"] == "phrase_and_exact":
                    rows.append(
                        {
                            "Campaign": name,
                            "Ad Group": g,
                            "Keyword": term,
                            "Match Type": "Exact",
                            "Status": "Paused",
                        }
                    )
    return rows


def rsa_rows() -> list[dict]:
    rows = []
    for name, _, groups in CAMPAIGNS:
        for g in groups:
            asset_key = "Marka" if g == "Marka" else "NonBrand"
            a = data.RSA[asset_key]
            row = {
                "Campaign": name,
                "Ad Group": g,
                "Ad type": "Responsive search ad",
                "Status": "Paused",
                "Final URL": a["final_url"],
                "Path 1": a["path1"],
                "Path 2": a["path2"],
            }
            for i, h in enumerate(a["headlines"][:15], 1):
                row[f"Headline {i}"] = h
            for i, d in enumerate(a["descriptions"][:4], 1):
                row[f"Description {i}"] = d
            if g == "Marka":
                # OTA savunmasi: marka adi (H1+H2) her zaman 1. pozisyonda gorunsun
                row["Headline 1 position"] = 1
                row["Headline 2 position"] = 1
            rows.append(row)
    return rows


def negatives_rows() -> list[dict]:
    # Hesap duzeyinde paylasilan negatif liste; ayrica non-brand kampanyalara da uygula.
    rows = []
    for term in data.NEGATIVES:
        rows.append(
            {
                "Campaign": "(Shared negative list) Kozbeyli-Negatifler",
                "Keyword": term,
                "Match Type": "Phrase",
            }
        )
    return rows


def sitelinks_rows() -> list[dict]:
    return [
        {
            "Sitelink text": s["text"],
            "Description 1": s["desc1"],
            "Description 2": s["desc2"],
            "Final URL": s["url"],
        }
        for s in data.SITELINKS
    ]


def callouts_rows() -> list[dict]:
    return [{"Callout text": c} for c in data.CALLOUTS]


def snippets_rows() -> list[dict]:
    return [
        {"Header": s["header"], "Values": "; ".join(s["values"])}
        for s in data.STRUCTURED_SNIPPETS
    ]


def _write_csv(path: Path, rows: list[dict]) -> int:
    if not rows:
        return 0
    # Tum satirlardaki sutunlarin birlesimi (RSA degisken sutunlu).
    cols: list[str] = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:  # BOM: Excel TR uyumu
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return len(rows)


IMPORT_GUIDE = """# Google Ads Editor — Import Rehberi (Kozbeyli Konağı)

Bu klasördeki CSV'ler **import-hazırdır** ve tüm kampanyaları **PAUSED** oluşturur.

## Adımlar
1. Google Ads Editor'ü aç, doğru hesabı (10 haneli müşteri ID) indir.
2. **Account > Import > From file** ile sırasıyla CSV'leri içeri al:
   `01_campaigns` → `02_ad_groups` → `03_keywords` → `04_responsive_search_ads`
   → `05_negative_keywords` → `06_sitelinks` → `07_callouts` → `08_structured_snippets`.
3. Her import sonrası "Check changes" ile önizle. **Post etmeden** her şeyi review et.
4. Bütçeler **günlük TRY**; bid stratejisi **Maximize Clicks + CPC limiti**.
5. Post et → kampanyalar **PAUSED** hesapta oluşur.
6. ENABLE etme; ölçüm test rezervasyonuyla doğrulanana kadar bekle (docs/03).
   ENABLE gerektiğinde `/kozbeyli-ads-change` + `kads guard` ile ikinci onay.

## Notlar
- Negatifler paylaşılan liste olarak gelir; non-brand + test kampanyalarına bağla.
- RSA başlıkları ≤30, açıklamalar ≤90 karakter (kads validate ile doğrulandı).
- Uzantılar (sitelink/callout/snippet) Editor'de ilgili sekmelere paste edilebilir.
- Konum: şehir hedefi (radius değil). Dil: Türkçe.
"""


def display_rows() -> list[dict]:
    d = dx.GOOGLE_DISPLAY
    row = {
        "Campaign": d["campaign"],
        "Campaign Type": "Display",
        "Status": d["status"],
        "Budget": f"{d['daily_try']:.2f}",
        "Budget Type": "Daily",
        "Bid Strategy Type": d["bid"],
        "Ad type": "Responsive display ad",
        "Final URL": d["final_url"],
        "Business name": d["business_name"],
        "Long headline": d["long_headline"],
        "Audience": d["audience"],
        "Image note": d["image_note"],
    }
    for i, h in enumerate(d["short_headlines"][:5], 1):
        row[f"Headline {i}"] = h
    for i, ds in enumerate(d["descriptions"][:5], 1):
        row[f"Description {i}"] = ds
    return [row]


def rsa_ab_rows() -> list[dict]:
    """Her reklam grubunda 3 RSA varyanti (A/B/C aci); farkli Headline 1."""
    rows = []
    for name, _, groups in CAMPAIGNS:
        for g in groups:
            asset_key = "Marka" if g == "Marka" else "NonBrand"
            a = data.RSA[asset_key]
            for variant, angle_h in dx.AB_ANGLES.items():
                pool = [angle_h] + [h for h in a["headlines"] if h != angle_h]
                row = {
                    "Campaign": name,
                    "Ad Group": g,
                    "Variant": variant,
                    "Ad type": "Responsive search ad",
                    "Status": "Paused",
                    "Final URL": a["final_url"],
                    "Path 1": a["path1"],
                    "Path 2": a["path2"],
                    "Headline 1 position": 1,
                }
                for i, h in enumerate(pool[:15], 1):
                    row[f"Headline {i}"] = h
                for i, ds in enumerate(a["descriptions"][:4], 1):
                    row[f"Description {i}"] = ds
                rows.append(row)
    return rows


def build(out_dir: Path) -> list[tuple[str, int]]:
    """Tum CSV'leri uretir. (dosya, satir_sayisi) listesi dondurur."""
    out_dir.mkdir(parents=True, exist_ok=True)
    results = [
        (
            "01_campaigns.csv",
            _write_csv(out_dir / "01_campaigns.csv", campaigns_rows()),
        ),
        (
            "02_ad_groups.csv",
            _write_csv(out_dir / "02_ad_groups.csv", ad_groups_rows()),
        ),
        ("03_keywords.csv", _write_csv(out_dir / "03_keywords.csv", keywords_rows())),
        (
            "04_responsive_search_ads.csv",
            _write_csv(out_dir / "04_responsive_search_ads.csv", rsa_rows()),
        ),
        (
            "05_negative_keywords.csv",
            _write_csv(out_dir / "05_negative_keywords.csv", negatives_rows()),
        ),
        (
            "06_sitelinks.csv",
            _write_csv(out_dir / "06_sitelinks.csv", sitelinks_rows()),
        ),
        ("07_callouts.csv", _write_csv(out_dir / "07_callouts.csv", callouts_rows())),
        (
            "08_structured_snippets.csv",
            _write_csv(out_dir / "08_structured_snippets.csv", snippets_rows()),
        ),
        (
            "09_display_campaign.csv",
            _write_csv(out_dir / "09_display_campaign.csv", display_rows()),
        ),
        (
            "10_rsa_ab_variants.csv",
            _write_csv(out_dir / "10_rsa_ab_variants.csv", rsa_ab_rows()),
        ),
    ]
    (out_dir / "IMPORT_REHBERI.md").write_text(IMPORT_GUIDE, encoding="utf-8")
    return results
