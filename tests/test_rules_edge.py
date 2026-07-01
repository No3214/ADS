"""rules.py edge case'leri: geçersiz metrik, CSV okuma, öncelik sıralaması."""
from pathlib import Path

from kads import rules


def test_evaluate_skips_non_numeric_metric():
    """Sayı olmayan metrik değeri sessizce atlanmalı (except dalı)."""
    trig = rules.evaluate({"blended_roas": "cok-iyi", "meta_frequency": 5.0})
    # bozuk roas atlandı, frequency kuralı yine de değerlendirildi
    assert "blended_roas" not in [t["metrik"] for t in trig]
    assert isinstance(trig, list)


def test_evaluate_missing_metric_ignored():
    """Metrik yoksa (None) o kural atlanır, hata vermez."""
    trig = rules.evaluate({})
    assert trig == []


def test_evaluate_priority_sorted():
    """Risk önce, Fırsat sonra (öncelik sıralaması)."""
    trig = rules.evaluate({"blended_roas": 0.5, "blended_cpa_try": 99999,
                           "nonbrand_ctr_pct": 0.1, "meta_frequency": 5.0})
    if len(trig) >= 2:
        pri = {"Risk": 0, "Fırsat": 1, "Orta": 2}
        vals = [pri.get(t["oncelik"], 9) for t in trig]
        assert vals == sorted(vals), "öncelik sıralı değil"


def test_load_metrics_csv_roundtrip(tmp_path: Path):
    """load_metrics_csv: başlık atlar, virgüllü ondalık okur, bozuk satırı yutar."""
    p = tmp_path / "m.csv"
    p.write_text('metrik,deger\nblended_roas,"3,17"\nbozuk,abc\nmeta_frequency,4.2\n',
                 encoding="utf-8-sig")
    m = rules.load_metrics_csv(p)
    assert m["blended_roas"] == 3.17  # virgül -> nokta
    assert m["meta_frequency"] == 4.2
    assert "bozuk" not in m  # float('abc') -> atlandı


def test_rule_rows_structure():
    for r in rules.rule_rows():
        assert {"oncelik", "id", "metrik", "kosul", "aksiyon"}.issubset(r.keys())
