import pandas as pd
from src.processors.claims_processor import exclude_test_claims, aggregate_claims
import pytest

def test_exclude_test_claims():
    test_df = pd.DataFrame({
        "Member Name": [
            "Jane Smith",
            "SB393 TEST",
            " SB393 TEST ",
            "sb393 test"
        ]
    })
    filtered_df = exclude_test_claims(test_df)
    assert len(filtered_df) == 1
    assert filtered_df["Member Name"].iloc[0] == "Jane Smith"

def test_aggregate_claims():
    test_df = pd.DataFrame({
        "Pharmacy Name": [
            "Feywild Pharmacy",
            "Feywild Pharmacy",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ],
        "Pharmacy NPI": [
            "TEST-001",
            "TEST-001",
            "TEST-002",
            "TEST-003"
        ],
        "Total Paid Amount": [
            100,
            50,
            200,
            25
        ]
    })
    aggregates = aggregate_claims(test_df)
    assert aggregates.loc[aggregates["Pharmacy Name"] == "Feywild Pharmacy", "Claim_Count"].iloc[0] == 2
    assert aggregates.loc[aggregates["Pharmacy Name"] == "Feywild Pharmacy", "Plan_Paid"].iloc[0] == 150
    assert aggregates["Pharmacy Name"].iloc[0] == "Neverwinter Drugs"

def test_aggregate_claims_with_zero_paid():
    test_df = pd.DataFrame({
        "Pharmacy Name": [
            "Feywild Pharmacy",
            "Feywild Pharmacy"
        ],
        "Pharmacy NPI": [
            "TEST-001",
            "TEST-001"
        ],
        "Total Paid Amount": [
            0,
            0
        ]
    })
    aggregates = aggregate_claims(test_df)
    assert aggregates.loc[aggregates["Pharmacy Name"] == "Feywild Pharmacy", "Claim_Count"].iloc[0] == 2
    assert aggregates.loc[aggregates["Pharmacy Name"] == "Feywild Pharmacy", "Plan_Paid"].iloc[0] == 0

def test_aggregate_claims_with_empty_dataframe():
    test_df = pd.DataFrame(columns=[
        "Pharmacy Name",
        "Pharmacy NPI",
        "Total Paid Amount"
    ])

    aggregates = aggregate_claims(test_df)
    assert aggregates.empty
    assert list(aggregates.columns) == [
        "Pharmacy Name",
        "Pharmacy NPI",
        "Claim_Count",
        "Plan_Paid"
    ]

def test_exclude_test_claims_when_all_records_are_test_claims():
    test_df = pd.DataFrame({
        "Member Name": [
            "SB393 TEST",
            " SB393 TEST ",
            "sb393 test"
        ]
    })
    filtered_df = exclude_test_claims(test_df)
    assert filtered_df.empty

def test_exclude_test_claims_preserves_original_dataframe():
    test_df = pd.DataFrame({
        "Member Name": [
            "Jane Smith",
            "SB393 TEST",
            "John Doe"
        ]
    })
    original_df = test_df.copy()
    pd.testing.assert_frame_equal(original_df, test_df)

def test_aggregate_claims_with_missing_payment():
    test_df = pd.DataFrame({
        "Pharmacy Name": ["Feywild Pharmacy"],
        "Pharmacy NPI": ["TEST-001"],
        "Total Paid Amount": [None]
    })

    with pytest.raises(ValueError):
        aggregate_claims(test_df)

def test_aggregate_claims_with_invalid_payment():
    test_df = pd.DataFrame({
        "Pharmacy Name": ["Feywild Pharmacy"],
        "Pharmacy NPI": ["TEST-001"],
        "Total Paid Amount": ["UNKNOWN"]
    })

    with pytest.raises(ValueError):
        aggregate_claims(test_df)

def test_two_pharmacies_one_npi():
    test_df = pd.DataFrame({
        "Pharmacy Name": [
            "Feywild Pharmacy",
            "Neverwinter Pharmacy"

        ],
        "Pharmacy NPI": [
            "TEST-001",
            "TEST-001"
        ],
        "Total Paid Amount": [
            100,
            200
        ]
    })
    with pytest.raises(ValueError):
        aggregate_claims(test_df)

def test_one_pharmacy_multiple_npis():
    test_df = pd.DataFrame({
        "Pharmacy Name": [
            "Feywild Pharmacy",
            "Feywild Pharmacy"
        ],
        "Pharmacy NPI": [
            "TEST-001",
            "TEST-002"
        ],
        "Total Paid Amount": [
            100,
            200
        ]
    })
    aggregates = aggregate_claims(test_df)
    assert aggregates.shape[0] == 2
    assert aggregates["Pharmacy NPI"].nunique() == 2
    assert aggregates["Plan_Paid"].sum() == 300

def test_aggregate_claims_with_negative_payment():
    test_df = pd.DataFrame({
        "Pharmacy Name": ["Feywild Pharmacy"],
        "Pharmacy NPI": ["TEST-001"],
        "Total Paid Amount": [-100]
    })

    with pytest.raises(ValueError):
        aggregate_claims(test_df)

def test_aggregate_claims_with_numeric_strings():
    test_df = pd.DataFrame({
        "Pharmacy Name": [
            "Feywild Pharmacy",
            "Feywild Pharmacy"
        ],
        "Pharmacy NPI": [
            "TEST-001",
            "TEST-001"
        ],
        "Total Paid Amount": [
            "100.00",
            "50.50"
        ]
    })

    aggregates = aggregate_claims(test_df)

    assert aggregates["Claim_Count"].iloc[0] == 2
    assert aggregates["Plan_Paid"].iloc[0] == 150.50
