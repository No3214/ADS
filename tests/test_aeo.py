"""AEO/GEO: kads aeo alt komutları + görünürlük skoru."""
import json
from pathlib import Path

from kads import core
from kads import data_ext as dx
from kads.cli import main

ROOT = Path(__file__).resolve().parents[1]


# ---- komutlar ---------------------------------------------------------------
def test_aeo_all_ok():
    assert main(["aeo"]) == core.EX_OK


def test_aeo_schema_ok():
    assert main(["aeo", "schema"]) == core.EX_OK


def test_aeo_queries_ok():
    assert main(["aeo", "queries"]) == core.EX_OK


def test_aeo_score_ok():
    assert main(["aeo", "score"]) == core.EX_OK


def test_aeo_queries_json_pipe_clean(capsys):
    rc = main(["aeo", "queries", "--format", "json"])
    assert rc == core.EX_OK
    out = capsys.readouterr().out.strip()
    assert out and out[0] == "["
    json.loads(out)


def test_aeo_score_json_pipe_clean(capsys):
    rc = main(["aeo", "score", "--format", "json"])
    assert rc == core.EX_OK
    out = capsys.readouterr().out.strip()
    assert out and out[0] == "["
    json.loads(out)


def test_aeo_score_missing_file_noinput():
    assert main(["aeo", "score", "--results", "yok_boyle.csv"]) == core.EX_NOINPUT


# ---- veri + skor fonksiyonu -------------------------------------------------
def test_aeo_test_queries_structure():
    assert len(dx.AEO_TEST_QUERIES) >= 20
    for q in dx.AEO_TEST_QUERIES:
        assert {"sorgu", "kategori", "dil"} <= set(q.keys())
    dils = {q["dil"] for q in dx.AEO_TEST_QUERIES}
    assert "tr" in dils and "en" in dils, "TR + EN sorgu olmalı (Perplexity/Claude EN sever)"


def test_aeo_visibility_score_math():
    rows = [
        {"ChatGPT": "2", "Perplexity": "1", "Gemini": "0", "Claude": "2"},
        {"ChatGPT": "2", "Perplexity": "2", "Gemini": "1", "Claude": "1"},
    ]
    sc = dx.aeo_visibility_score(rows)
    # toplam 14 / max 16 = %87.5? -> 2+1+0+2 + 2+2+1+1 = 11 ; max 16 -> 68.8
    assert sc["overall_pct"] == 68.8
    assert sc["per_platform"]["ChatGPT"] == 100.0
    assert sc["filled"] == 8 and sc["total_cells"] == 8


def test_aeo_visibility_score_empty_is_zero():
    rows = [{"ChatGPT": "", "Perplexity": "", "Gemini": "", "Claude": ""}]
    sc = dx.aeo_visibility_score(rows)
    assert sc["overall_pct"] == 0.0 and sc["filled"] == 0
    assert all(v is None for v in sc["per_platform"].values())


def test_aeo_competitors_tracked():
    assert len(dx.AEO_COMPETITORS_TRACK) == 3
    assert "Bülbül Yuvası Hotel" in dx.AEO_COMPETITORS_TRACK


# ---- dosya varlıkları -------------------------------------------------------
def test_alinti_csv_regenerated():
    p = ROOT / "aeo" / "alinti-testi.csv"
    assert p.exists()
    lines = [ln for ln in p.read_text(encoding="utf-8-sig").splitlines() if ln.strip()]
    assert len(lines) - 1 >= 20  # başlık + >=20 sorgu
    assert "ChatGPT" in lines[0] and "kategori" in lines[0]


def test_aeo_strategy_doc_exists():
    assert (ROOT / "docs" / "aeo-strategy.md").exists()


def test_aeo_mastery_skill_valid():
    p = ROOT / "skills" / "aeo-mastery" / "SKILL.md"
    assert p.exists()
    txt = p.read_text(encoding="utf-8")
    assert txt.startswith("---")
    fm = txt.split("---", 2)[1]
    assert "name: aeo-mastery" in fm and "description:" in fm
    assert "aeo-strategy.md" in txt and "kads aeo" in txt
