"""kads CLI kapsam genisletme + json temizligi (regresyon) + edge case'ler."""

import json

import pytest

from kads import core
from kads.cli import main


# --- daha once testi olmayan komutlar ---------------------------------------
def test_config_ok():
    assert main(["config"]) == core.EX_OK


def test_config_json_ok():
    assert main(["config", "-f", "json"]) == core.EX_OK


def test_budget_ok():
    assert main(["budget", "-f", "json"]) == core.EX_OK


def test_keywords_ok():
    assert main(["keywords", "-f", "json"]) == core.EX_OK


def test_creative_google_ok():
    assert main(["creative", "google"]) == core.EX_OK


def test_creative_meta_ok():
    assert main(["creative", "meta"]) == core.EX_OK


def test_brief_ok(tmp_path):
    assert main(["brief", "--out", str(tmp_path)]) == core.EX_OK


def test_monitor_code():
    assert main(["monitor", "-f", "json"]) in (core.EX_OK, core.EX_UNAVAILABLE)


def test_doctor_code():
    assert main(["doctor", "-f", "json"]) in (core.EX_OK, core.EX_CONFIG)


def test_guard_usage_code():
    assert main(["guard"]) == core.EX_USAGE


# --- edge case'ler -----------------------------------------------------------
def test_unknown_command():
    assert main(["voo-doo-xyz"]) == core.EX_USAGE


def test_empty_args_help():
    assert main([]) == core.EX_OK


def test_help_explicit():
    assert main(["help"]) == core.EX_OK


def test_bad_format_falls_back():
    assert main(["plan", "--format", "xml"]) == core.EX_OK


def test_rules_missing_metrics():
    assert main(["rules", "--metrics", "/yok/olmayan-xyz-123.csv"]) == core.EX_NOINPUT


def test_report_missing_metrics():
    assert main(["report", "--metrics", "/yok/olmayan-xyz-123.csv"]) == core.EX_NOINPUT


def test_publish_bad_days(tmp_path):
    assert main(["publish", "--days", "abc", "--out", str(tmp_path)]) == core.EX_OK


# --- json temizligi: pipe-clean (regresyon kilidi) ---------------------------
JSON_READONLY = [
    ["mcp"],
    ["presence"],
    ["golive"],
    ["aeo"],
    ["b2b"],
    ["seo"],
    ["season"],
    ["season", "detail"],
    ["funnel"],
    ["offers"],
    ["conversions"],
    ["conversions", "offline"],
    ["conversions", "enhanced"],
    ["allocate"],
    ["allocate", "funnel"],
    ["utm"],
    ["utm", "rules"],
    ["attribution"],
    ["pmax"],
    ["pmax", "specs"],
    ["demandgen"],
    ["remarketing"],
    ["remarketing", "flow"],
    ["competitors"],
    ["audiences"],
    ["plan"],
    ["budget"],
    ["keywords"],
    ["kpi"],
    ["tracking"],
    ["godtier-audit"],
    ["inject-audiences"],
]


@pytest.mark.parametrize("cmd", JSON_READONLY, ids=lambda c: "_".join(c))
def test_json_pipe_clean(capsys, cmd):
    rc = main(cmd + ["--format", "json"])
    assert rc == core.EX_OK
    out = capsys.readouterr().out.strip()
    if out:
        json.loads(out)  # gecersiz JSON ise burada patlar


def test_json_monitor(capsys):
    rc = main(["monitor", "--format", "json"])
    assert rc in (core.EX_OK, core.EX_UNAVAILABLE)
    json.loads(capsys.readouterr().out.strip())


@pytest.mark.parametrize("cmd", [["publish"], ["report"], ["brief"]])
def test_json_file_writers(capsys, tmp_path, cmd):
    rc = main(cmd + ["--out", str(tmp_path), "--format", "json"])
    assert rc == core.EX_OK
    out = capsys.readouterr().out.strip()
    if out:
        json.loads(out)


def test_no_adtext_length_violations():
    # RSA + A/B + Display + Meta basliklari hepsi limit icinde (regresyon kilidi)
    from kads import cli

    assert cli._length_problems() == []


def test_version_single_source():
    # Tek kaynak: kads.__version__ == cli.VERSION, gecerli semver (drift olmaz)
    import re

    from kads import __version__, cli

    assert cli.VERSION == __version__
    assert re.fullmatch(r"\d+\.\d+\.\d+", __version__)
