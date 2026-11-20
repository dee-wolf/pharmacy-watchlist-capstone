import pandas as pd
from src.validators.watchlist_validator import validate_watchlist
import pytest

def test_validate_watchlist():
    test_df = pd.DataFrame({
        "NPI": [
            "TEST-001",
            "TEST-002",
            "OUT-001"
        ]
    })
    validate_watchlist(test_df, expected_count=3, expected_participating=2, expected_nonparticipating=1)

def test_validate_watchlist_wrong_record_count():
    test_df = pd.DataFrame({
        "NPI": [
            "TEST-001",
            "TEST-002",
            "OUT-001"
        ]
    })
    with pytest.raises(ValueError):
        validate_watchlist(test_df, expected_count=4, expected_participating=2, expected_nonparticipating=1)

def test_validate_watchlist_duplicate_npis():
    test_df = pd.DataFrame({
        "NPI": [
            "TEST-001",
            "TEST-001",
            "OUT-001"
        ]
    })
    with pytest.raises(ValueError):
        validate_watchlist(test_df, expected_count=4, expected_participating=2, expected_nonparticipating=1)

def test_validate_watchlist_wrong_participating_count():
    test_df = pd.DataFrame({
        "NPI": [
            "TEST-001",
            "TEST-002",
            "OUT-001"
        ]
    })
    with pytest.raises(ValueError):
        validate_watchlist(test_df, expected_count=3, expected_participating=3, expected_nonparticipating=1)

def test_validate_watchlist_wrong_nonparticipating_count():
    test_df = pd.DataFrame({
        "NPI": [
            "TEST-001",
            "TEST-002",
            "OUT-001"
        ]
    })
    with pytest.raises(ValueError):
        validate_watchlist(test_df, expected_count=3, expected_participating=2, expected_nonparticipating=2)
