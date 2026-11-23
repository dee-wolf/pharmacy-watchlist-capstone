import pytest
from src.generators.name_parts import generate_pharmacy_names

def test_generate_pharmacy_names():
    result = generate_pharmacy_names()
    assert len(result) == 310

def test_generate_pharmacy_names_unique():
    result = generate_pharmacy_names()
    assert len(result) == len(set(result))

def test_generate_pharmacy_names_expected_combinations():
    result = generate_pharmacy_names()
    assert "Raven Road Apothecary" in result
    assert "Willow Creek Pharmacy" in result
    assert "Nicky Rx" in result
