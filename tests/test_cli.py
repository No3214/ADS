"""kads CLI smoke + cikis kodlari."""
from kads.cli import main
from kads import core


def test_plan_ok(): assert main(["plan", "--format", "json"]) == core.EX_OK
def test_validate_ok(): assert main(["validate"]) == core.EX_OK
def test_build_all(tmp_path): assert main(["build", "all", "--out", str(tmp_path)]) == core.EX_OK
def test_presence_ok(): assert main(["presence", "fixes", "--format", "csv"]) == core.EX_OK
def test_seo_schema_ok(): assert main(["seo", "schema"]) == core.EX_OK
def test_kpi_calc(): assert main(["kpi", "--revenue", "90000", "--spend", "30000"]) == core.EX_OK
def test_version_ok(): assert main(["version"]) == core.EX_OK
def test_bad_command_usage_code(): assert main(["nonsense-xyz"]) == core.EX_USAGE


def test_rules_ok(): from kads.cli import main; assert main(["rules", "--format", "json"]) == 0
def test_audiences_ok(): from kads.cli import main; assert main(["audiences", "-f", "csv"]) == 0
def test_mcp_ok(): from kads.cli import main; assert main(["mcp"]) == 0
def test_skills_ok(): from kads.cli import main; assert main(["skills"]) == 0
def test_report_tmpl_ok(tmp_path): from kads.cli import main; assert main(["report", "--out", str(tmp_path)]) == 0


def test_golive_ok(): from kads.cli import main; assert main(["golive"]) == 0
def test_golive_json_ok(): from kads.cli import main; assert main(["golive", "--format", "json"]) == 0


def test_competitors_ok(): from kads.cli import main; assert main(["competitors", "-f", "json"]) == 0
def test_calendar_ok(): from kads.cli import main; assert main(["calendar", "--days", "7"]) == 0
def test_publish_ok(tmp_path): from kads.cli import main; assert main(["publish", "--out", str(tmp_path)]) == 0
def test_setup_ok(): from kads.cli import main; assert main(["setup"]) == 0


def test_status_ok(): from kads.cli import main; assert main(["status", "-f", "json"]) == 0


def test_apify_ok(): from kads.cli import main; assert main(["apify", "-f", "json"]) == 0


def test_aeo_ok(): from kads.cli import main; assert main(["aeo", "-f", "json"]) == 0
def test_aeo_schema_ok(): from kads.cli import main; assert main(["aeo", "schema", "-f", "csv"]) == 0


def test_season_ok(): from kads.cli import main; assert main(["season", "-f", "json"]) == 0
def test_funnel_ok(): from kads.cli import main; assert main(["funnel", "-f", "csv"]) == 0
def test_offers_ok(): from kads.cli import main; assert main(["offers", "-f", "json"]) == 0


def test_web_ok(): from kads.cli import main; assert main(["web", "-f", "json"]) == 0


def test_b2b_ok(): from kads.cli import main; assert main(["b2b", "-f", "json"]) == 0
def test_b2b_packages_ok(): from kads.cli import main; assert main(["b2b", "packages", "-f", "csv"]) == 0
def test_selfcheck_ok(): from kads.cli import main; assert main(["selfcheck", "-f", "json"]) == 0
