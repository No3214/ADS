"""cli.py alt-komut + format + --metrics/--approval dallarının kapsanması."""
import json

import pytest

from kads import core
from kads.cli import main


def _metrics_csv(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text(
        "metrik,deger\nblended_roas,0.5\nblended_cpa_try,99999\n"
        "nonbrand_ctr_pct,0.1\nmeta_frequency,5\nspend_pace_pct,150\nweekly_conversions,0\n",
        encoding="utf-8",
    )
    return p


def _report_csv(tmp_path):
    p = tmp_path / "r.csv"
    p.write_text(
        "metrik,deger\ngoogle_spend_try,5000\nmeta_spend_try,4000\n"
        "tracked_revenue_try,27000\ngoogle_conversions,6\nmeta_purchases,5\n"
        "google_clicks,1400\nmeta_clicks,800\ngoogle_impressions,30000\nmeta_impressions,50000\n",
        encoding="utf-8",
    )
    return p


# ---- seo / presence alt komutları -------------------------------------------
@pytest.mark.parametrize("sub", ["schema", "gbp", "local", "brand"])
def test_seo_subcommands(sub):
    assert main(["seo", sub]) == core.EX_OK


@pytest.mark.parametrize("sub", ["", "fixes", "props"])
def test_presence_subcommands(sub):
    args = ["presence"] + ([sub] if sub else [])
    assert main(args) == core.EX_OK


# ---- rules / report --metrics -----------------------------------------------
def test_rules_metrics_trigger(tmp_path):
    assert main(["rules", "--metrics", str(_metrics_csv(tmp_path))]) == core.EX_OK


def test_rules_metrics_json(tmp_path, capsys):
    rc = main(["rules", "--metrics", str(_metrics_csv(tmp_path)), "-f", "json"])
    assert rc == core.EX_OK
    out = capsys.readouterr().out.strip()
    assert out.startswith("["), "json pipe-temiz olmali"
    json.loads(out)


def test_report_metrics(tmp_path):
    assert main(["report", "--metrics", str(_report_csv(tmp_path))]) == core.EX_OK


def test_rules_report_missing_metrics_noinput():
    assert main(["rules", "--metrics", "yok.csv"]) == core.EX_NOINPUT
    assert main(["report", "--metrics", "yok.csv"]) == core.EX_NOINPUT


# ---- guard ------------------------------------------------------------------
def test_guard_no_check_usage():
    assert main(["guard"]) == core.EX_USAGE


def test_guard_check_returns_code(tmp_path):
    cj = tmp_path / "change.json"
    cj.write_text(
        json.dumps({"platform": "google", "account_id": "6489372864",
                    "action": "pause", "status": "PAUSED"}),
        encoding="utf-8",
    )
    rc = main(["guard", "--check", str(cj)])
    assert isinstance(rc, int) and rc >= 0  # ALLOW/DENY/NEEDS_APPROVAL -> sysexit


# ---- büyüme alt komutları ---------------------------------------------------
@pytest.mark.parametrize("cmd,sub", [
    ("pmax", "specs"), ("pmax", "setup"), ("demandgen", "audiences"),
    ("remarketing", "rlsa"), ("remarketing", "flow"),
("allocate", "funnel"), ("allocate", "rules"),
    ("conversions", "offline"), ("conversions", "enhanced"), ("conversions", "calls"),
    ("season", "detail"), ("b2b", "packages"), ("aeo", "schema"),
])
def test_growth_subcommands(cmd, sub):
    assert main([cmd, sub]) == core.EX_OK


# ---- format matrisi (yaml/md/csv pipe-temiz) --------------------------------
@pytest.mark.parametrize("cmd", ["plan", "budget", "keywords", "audiences", "competitors"])
@pytest.mark.parametrize("fmt", ["yaml", "md", "csv"])
def test_format_matrix(cmd, fmt):
    assert main([cmd, "-f", fmt]) == core.EX_OK


# ---- aeo score dolu CSV -> yorum dalı ---------------------------------------
def test_aeo_score_filled(tmp_path):
    p = tmp_path / "filled.csv"
    p.write_text(
        "sorgu,kategori,dil,ChatGPT,Perplexity,Gemini,Claude,tarih,not\n"
        "q1,butik,tr,2,1,0,2,,\nq2,marka,tr,1,2,1,1,,\n",
        encoding="utf-8",
    )
    assert main(["aeo", "score", "--results", str(p)]) == core.EX_OK


def test_utm_build_with_url():
    rc = main(["utm", "build", "--url", "https://www.kozbeylikonagi.com",
               "--source", "meta", "--medium", "paid_social", "--campaign", "prospecting"])
    assert rc == core.EX_OK


def test_utm_rules_and_plain():
    assert main(["utm", "rules"]) == core.EX_OK
    assert main(["utm"]) == core.EX_OK
