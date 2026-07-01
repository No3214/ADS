"""Kod kalitesi kilidi: tüm CLI komut fonksiyonları docstring + type hint taşımalı."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _cli_functions():
    tree = ast.parse((ROOT / "kads" / "cli.py").read_text(encoding="utf-8"))
    return [n for n in tree.body if isinstance(n, ast.FunctionDef)]


def test_all_cmd_functions_have_docstring():
    miss = [n.name for n in _cli_functions()
            if n.name.startswith("cmd_") and not ast.get_docstring(n)]
    assert not miss, f"docstring eksik komutlar: {miss}"


def test_all_cmd_functions_return_int_hint():
    miss = [n.name for n in _cli_functions()
            if n.name.startswith("cmd_") and (n.returns is None
            or ast.unparse(n.returns) != "int")]
    assert not miss, f"'-> int' hint eksik: {miss}"


def test_all_cmd_functions_take_typed_args():
    bad = []
    for n in _cli_functions():
        if not n.name.startswith("cmd_"):
            continue
        a = n.args.args
        if not a or a[0].annotation is None or ast.unparse(a[0].annotation) != "list[str]":
            bad.append(n.name)
    assert not bad, f"args: list[str] hint eksik: {bad}"
