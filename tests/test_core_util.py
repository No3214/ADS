"""core util'ler: emit biçimleri, mask, is_placeholder, kv, banner."""
import json

from kads import core


def test_emit_json(capsys):
    core.emit([{"a": 1, "b": "x"}], fmt="json")
    out = capsys.readouterr().out.strip()
    assert json.loads(out) == [{"a": 1, "b": "x"}]


def test_emit_json_empty(capsys):
    core.emit([], fmt="json")
    assert capsys.readouterr().out.strip() == "[]"


def test_emit_table_empty(capsys):
    core.emit([], fmt="table")
    assert "veri yok" in capsys.readouterr().out


def test_emit_csv(capsys):
    core.emit([{"a": 1, "b": 2}], fmt="csv")
    out = capsys.readouterr().out
    assert "a,b" in out and "1,2" in out


def test_emit_yaml(capsys):
    core.emit([{"a": "x:y"}], fmt="yaml")
    out = capsys.readouterr().out
    assert "a:" in out  # özel karakterli değer JSON-quote edilir


def test_emit_md(capsys):
    core.emit([{"a": "x|y"}], fmt="md", title="T")
    out = capsys.readouterr().out
    assert "| a |" in out and "\\|" in out  # pipe kaçışlı


def test_emit_table_basic(capsys):
    core.emit([{"ad": "Kozbeyli", "puan": 4.2}], fmt="table", title="Rapor")
    out = capsys.readouterr().out
    assert "Kozbeyli" in out


def test_mask_secret():
    assert core.mask("REFRESH_TOKEN", "abc123") == "***gizli***"
    assert core.mask("PLATFORM", "google") == "google"
    assert core.mask("TOKEN", "") == ""
    assert core.mask("SECRET", "replace-me") == "replace-me"  # placeholder maskeleme


def test_is_placeholder():
    assert core.is_placeholder("") is True
    assert core.is_placeholder("replace-me") is True
    assert core.is_placeholder("act_REPLACE_ME") is True
    assert core.is_placeholder("gerçek_deger") is False


def test_kv_and_banner(capsys):
    core.kv("Başlık", [("alan1", "deger1")], fmt="table")
    core.banner("Test")
    out = capsys.readouterr().out
    assert "alan1" in out and "Test" in out
