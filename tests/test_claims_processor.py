import pandas as pd
from src.processors.claims_processor import exclude_test_claims, aggregate_claims

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
    filtered_df = exclude_test_claims(test_df)
    pd.testing.assert_frame_equal(original_df, test_df)
