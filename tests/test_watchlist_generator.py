import pandas as pd
import pytest
from src.generators.watchlist import generate_watchlist

def test_watchlist_generator_pharmacy_num_type():
    with pytest.raises(TypeError):
        generate_watchlist(True)

def test_watchlist_generator_participating_count_type():
    with pytest.raises(TypeError):
        generate_watchlist(participating_count=False)

def test_watchlist_generator_seed_type():
    with pytest.raises(TypeError):
        generate_watchlist(seed="42")

def test_watchlist_reporting_month_type():
    with pytest.raises(TypeError):
        generate_watchlist(reporting_month=112026)

def test_watchlist_reporting_normal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    generate_watchlist(num_pharmacies=3, participating_count=2, seed=23)
    assert (tmp_path / "data" / "raw" / "monthly_watchlist.xlsx").exists()
    assert (tmp_path / "data" / "raw" / "enrolled_pharmacies.xlsx").exists()

def test_watchlist_reporting_seed_repeatability(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result1 = generate_watchlist(num_pharmacies=3, participating_count=2, seed=25)
    result2 = generate_watchlist(num_pharmacies=3, participating_count=2, seed=25)
    pd.testing.assert_frame_equal(result1, result2)

def test_watchlist_reporting_different_seed_results(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result1 = generate_watchlist(num_pharmacies=3, participating_count=2, seed=25)
    result2 = generate_watchlist(num_pharmacies=3, participating_count=2, seed=32)
    assert not result1.equals(result2)

def test_watchlist_reporting_month_format():
    with pytest.raises(ValueError):
        generate_watchlist(reporting_month="November 2026")

def test_watchlist_seed_format():
    with pytest.raises(TypeError):
        generate_watchlist(seed=True)
