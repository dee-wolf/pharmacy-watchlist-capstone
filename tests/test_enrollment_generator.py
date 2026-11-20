import pandas as pd
import pytest
from src.generators.enrollment import generate_enrollment

def test_generate_enrollment(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result = generate_enrollment(3)
    assert len(result) == 3

def test_generate_ennrollment_rejects_non_integer():
    with pytest.raises(TypeError):
        generate_enrollment("3")

def test_generate_enrollment_rejects_bool():
    with pytest.raises(TypeError):
        generate_enrollment(True)

def test_generate_ennrollment_rejects_zero():
    with pytest.raises(ValueError):
        generate_enrollment(0)

def test_generate_ennrollment_rejects_negative():
    with pytest.raises(ValueError):
        generate_enrollment(-5)

def test_generate_enrollment_NPI_column(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result = generate_enrollment(250)
    assert result.columns == pd.Index(["Pharmacy NPI"])

def test_generate_enrollment_NPI_uniqueness(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result = generate_enrollment()
    assert result["Pharmacy NPI"].nunique() == 250

def test_generate_enrollment_NPI_number(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result = generate_enrollment()
    assert result["Pharmacy NPI"].iloc[0] == "TEST-000001"
    assert result["Pharmacy NPI"].iloc[249] == "TEST-000250"

def test_generate_enrollment_creation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    generate_enrollment()
    assert (tmp_path / "data" / "raw" / "enrolled_pharmacies.xlsx").exists()

def test_generate_enrollment_proper_default(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    result = generate_enrollment()
    assert len(result) == 250
