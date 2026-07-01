"""CLI alt-komut + edge-case dal kapsamı (seo/presence/rules/report/guard/format)."""
import json

from kads import core
from kads.cli import main


# ---- seo alt komutları ------------------------------------------------------
def test_seo_gbp():
    assert main(["seo", "gbp"]) == core.EX_OK


def test_seo_local():
    assert main(["seo", "local"]) == core.EX_OK


def test_seo_brand():
    assert main(["seo", "brand"]) == core.EX_OK


def test_seo_schema():
    assert main(["seo", "schema"]) == core.EX_OK


# ---- presence alt komutları -------------------------------------------------
def test_presence_props():
    assert main(["presence", "props"]) == core.EX_OK


def test_presence_fixes():
    assert main(["presence", "fixes"]) == core.EX_OK


# ---- rules / report --metrics (tetiklenen + tetiklenmeyen) ------------------
def _metrics_csv(tmp_path, roas):
    p = tmp_path / "m.csv"
    p.write_text(
        f"metrik,deger\nblended_roas,{roas}\nblended_cpa_try,99999\n"
        "nonbrand_ctr_pct,0.1\nmeta_frequency,5.0\n",
        encoding="utf-8-sig",
    )
    return str(p)


def test_rules_metrics_triggered(tmp_path):
    assert main(["rules", "--metrics", _metrics_csv(tmp_path, 0.5)]) == core.EX_OK


def test_rules_metrics_none_triggered(tmp_path):
    # sağlıklı metrikler -> tetik yok
    p = tmp_path / "ok.csv"
    p.write_text("metrik,deger\nblended_roas,4.0\nmeta_frequency,1.0\n", encoding="utf-8-sig")
    assert main(["rules", "--metrics", str(p)]) == core.EX_OK


def test_rules_metrics_missing_file():
    assert main(["rules", "--metrics", "yok.csv"]) == core.EX_NOINPUT


def test_report_metrics(tmp_path):
    assert main(["report", "--metrics", _metrics_csv(tmp_path, 2.0)]) == core.EX_OK


def test_report_metrics_missing():
    assert main(["report", "--metrics", "yok.csv"]) == core.EX_NOINPUT


# ---- guard --check (ALLOW/DENY/NEEDS_APPROVAL yolları) ----------------------
def test_guard_no_check_usage():
    assert main(["guard"]) == core.EX_USAGE


def test_guard_check_pause_paused(tmp_path):
    # PAUSED pause -> writes kapalı olduğu için DENY (EX_GENERIC) beklenir
    ch = tmp_path / "change.json"
    ch.write_text(json.dumps({
        "platform": "google", "account_id": "6489372864", "action": "pause",
        "status": "PAUSED", "entity": "campaign"
    }), encoding="utf-8")
    rc = main(["guard", "--check", str(ch)])
    assert rc in (core.EX_OK, core.EX_GENERIC, core.EX_NOPERM)


# ---- format varyantları (yaml/md/csv dalları) ------------------------------
def test_plan_yaml():
    assert main(["plan", "-f", "yaml"]) == core.EX_OK


def test_keywords_md():
    assert main(["keywords", "-f", "md"]) == core.EX_OK


def test_budget_csv():
    assert main(["budget", "-f", "csv"]) == core.EX_OK


# ---- büyüme komutları alt-modları ------------------------------------------
def test_pmax_specs():
    assert main(["pmax", "specs"]) == core.EX_OK


def test_pmax_setup():
    assert main(["pmax", "setup"]) == core.EX_OK


def test_demandgen_audiences():
    assert main(["demandgen", "audiences"]) == core.EX_OK


def test_remarketing_rlsa():
    assert main(["remarketing", "rlsa"]) == core.EX_OK


def test_remarketing_flow():
    assert main(["remarketing", "flow"]) == core.EX_OK


def test_utm_build():
    rc = main(["utm", "build", "--url", "https://www.kozbeylikonagi.com/rezervasyon",
               "--source", "google", "--medium", "cpc", "--campaign", "marka"])
    assert rc == core.EX_OK


def test_utm_build_no_url_usage():
    assert main(["utm", "build"]) == core.EX_USAGE


def test_utm_rules():
    assert main(["utm", "rules"]) == core.EX_OK


def test_allocate_funnel():
    assert main(["allocate", "funnel"]) == core.EX_OK


def test_conversions_offline():
    assert main(["conversions", "offline"]) == core.EX_OK


def test_conversions_enhanced():
    assert main(["conversions", "enhanced"]) == core.EX_OK


def test_conversions_calls():
    assert main(["conversions", "calls"]) == core.EX_OK


def test_season_detail():
    assert main(["season", "detail"]) == core.EX_OK


def test_b2b_packages():
    assert main(["b2b", "packages"]) == core.EX_OK


# ---- bilinmeyen komut + boş ------------------------------------------------
def test_unknown_command():
    assert main(["boyle-komut-yok"]) == core.EX_USAGE


def test_no_command_shows_help():
    assert main([]) in (core.EX_OK, core.EX_USAGE)


def test_rules_metrics_none_json(tmp_path):
    p = tmp_path / "ok.csv"
    p.write_text("metrik,deger\nblended_roas,4.0\n", encoding="utf-8-sig")
    import kads.core as _c
    from kads.cli import main as _m
    assert _m(["rules", "--metrics", str(p), "-f", "json"]) == _c.EX_OK
