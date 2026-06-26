"""kads buyume katmani testleri: PMax / Demand Gen / Google remarketing."""
from kads.cli import main
from kads import data_growth as dg


def test_pmax_ok(): assert main(["pmax", "-f", "json"]) == 0
def test_pmax_specs_ok(): assert main(["pmax", "specs"]) == 0
def test_pmax_setup_ok(): assert main(["pmax", "setup", "-f", "json"]) == 0
def test_demandgen_ok(): assert main(["demandgen", "-f", "json"]) == 0
def test_demandgen_aud_ok(): assert main(["demandgen", "audiences", "-f", "csv"]) == 0
def test_demandgen_specs_ok(): assert main(["demandgen", "specs"]) == 0
def test_remarketing_ok(): assert main(["remarketing", "-f", "json"]) == 0
def test_remarketing_rlsa_ok(): assert main(["remarketing", "rlsa", "-f", "json"]) == 0
def test_remarketing_flow_ok(): assert main(["remarketing", "flow"]) == 0


def test_pmax_data():
    assert len(dg.PMAX_ASSET_GROUPS) >= 4
    assert all(g.get("final_url", "").startswith("https://") for g in dg.PMAX_ASSET_GROUPS)
    assert len(dg.PMAX_ASSET_SPECS) >= 8 and dg.PMAX_NOTE


def test_demandgen_data():
    assert len(dg.DEMAND_GEN_FORMATS) >= 3
    assert len(dg.DEMAND_GEN_AUDIENCES) >= 4


def test_remarketing_data():
    assert len(dg.GOOGLE_REMARKETING) >= 6
    assert all(isinstance(r["uyelik_gun"], int) and r["uyelik_gun"] > 0 for r in dg.GOOGLE_REMARKETING)
    assert len(dg.RLSA_RULES) >= 4 and len(dg.REMARKETING_FLOW) >= 5
