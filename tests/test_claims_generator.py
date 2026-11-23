import pandas as pd
import pytest
from src.generators.claims import generate_claims

def test_generate_claims_defaults(tmp_path, monkeypatch):
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result = generate_claims(watchlist)
    assert result.shape[0] == 1500

def test_generate_claims_same_results(tmp_path, monkeypatch):
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result1 = generate_claims(watchlist, seed=42)
    result2 = generate_claims(watchlist, seed=42)
    pd.testing.assert_frame_equal(result1, result2)

def test_generate_claims_different_seeds(tmp_path, monkeypatch):
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result1 = generate_claims(watchlist, seed=42)
    result2 = generate_claims(watchlist, seed=99)
    assert not result1.equals(result2)

def test_generate_claims_claim_number(tmp_path, monkeypatch):
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result = generate_claims(watchlist, num_claims = 100)
    assert result.shape[0] == 100

def test_generate_claims_invalid_pharm_num():
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    with pytest.raises(TypeError):
        generate_claims(watchlist, num_claims="100")

def test_generate_claims_zero_pharms():
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    with pytest.raises(ValueError):
        generate_claims(watchlist, num_claims=0)

def test_generate_claims_negative_pharms():
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    with pytest.raises(ValueError):
        generate_claims(watchlist, num_claims=-10)

def test_generate_claims_invalid_claims_num():
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    with pytest.raises(TypeError):
        generate_claims(watchlist, test_claims="100")

def test_generate_claims_negative_test():
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    with pytest.raises(ValueError):
        generate_claims(watchlist, test_claims=-10)

def test_generate_claims_teste_greater_than_total():
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    with pytest.raises(ValueError):
        generate_claims(watchlist, num_claims= 10, test_claims= 11)

def test_generate_claims_test_claims_correct(tmp_path, monkeypatch):
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result = generate_claims(watchlist, num_claims = 100, test_claims=10)
    assert result["Member Name"].str.startswith("SB").sum() == 10

def test_generate_claims_eligibility_testing(tmp_path, monkeypatch):
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result = generate_claims(watchlist)
    assert result["Pharmacy NPI"].str.startswith("TEST-").all()

def test_generate_claims_no_participating_pharms():
    watchlist = pd.DataFrame({
        "NPI": ["OUT-000001", "OUT-000002", "OUT-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    with pytest.raises(ValueError):
        generate_claims(watchlist)

def test_generate_claims_columns_correct(tmp_path, monkeypatch):
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result = generate_claims(watchlist)
    assert list(result.columns) == [
        "Member Name",
        "Pharmacy Name",
        "Pharmacy NPI",
        "Total Paid Amount"
        ]

def test_generate_claims_claim_totals_correct(tmp_path, monkeypatch):
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result = generate_claims(watchlist)
    assert (result["Total Paid Amount"] >= 5.00).all()
    assert (result["Total Paid Amount"] <= 5000.00).all()

def test_generate_claims_makes_claims_file(tmp_path, monkeypatch):
    watchlist = pd.DataFrame({
        "NPI": ["TEST-000001", "TEST-000002", "TEST-000003"],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result = generate_claims(watchlist)
    assert (tmp_path / "data" / "raw" / "cognos_claims_minimal.xlsx").exists()
