import pandas as pd
import pytest
from src.processors.watchlist_processor import match_enrollment, merge_claims_with_watchlist, assign_final_status


def test_match_enrollment_preserves_watchlist_records():
    watchlist = pd.DataFrame({
        "NPI": ["TEST-001", "TEST-002", "TEST-003"],
        "Pharmacy Name": [
            "Feywild Pharmacy",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    network = pd.DataFrame({
        "Pharmacy NPI": ["TEST-001", "TEST-003"]
    })
    matched_watchlist = match_enrollment(watchlist, network)
    assert matched_watchlist.shape[0] == 3
    assert (matched_watchlist["enrollment_status"] == "both").sum() == 2
    assert (matched_watchlist["enrollment_status"] == "left_only").sum() == 1

def test_match_enrollment_not_modifying_originals():
    watchlist = pd.DataFrame({
        "NPI": ["TEST-001", "TEST-002", "TEST-003"],
        "Pharmacy Name": [
            "Feywild Pharmacy",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    network = pd.DataFrame({
        "Pharmacy NPI": ["TEST-001", "TEST-003"]
    })
    network_copy = network.copy()
    watchlist_copy = watchlist.copy()
    match_enrollment(watchlist, network)
    pd.testing.assert_frame_equal(network, network_copy)
    pd.testing.assert_frame_equal(watchlist, watchlist_copy)

def test_match_enrollment_actually_matching():
    watchlist = pd.DataFrame({
        "NPI": ["TEST-001", "TEST-002", "TEST-003"],
        "Pharmacy Name": [
            "Feywild Pharmacy",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ]
    })
    network = pd.DataFrame({
        "Pharmacy NPI": ["TEST-001", "TEST-003"]
    })
    matched_watchlist = match_enrollment(watchlist, network)
    assert matched_watchlist.loc[matched_watchlist["NPI"] == "TEST-001", "enrollment_status"].iloc[0] == "both"
    assert matched_watchlist.loc[matched_watchlist["NPI"] == "TEST-002", "enrollment_status"].iloc[0] == "left_only"

def test_match_enrollment_handling_empty_df():
    watchlist = pd.DataFrame({
        "NPI": [],
        "Pharmacy Name": []
    })
    network = pd.DataFrame({
        "Pharmacy NPI": ["TEST-001", "TEST-003"]
    })
    matched_watchlist = match_enrollment(watchlist, network)
    assert matched_watchlist.empty
    assert list(matched_watchlist) == [
        "NPI",
        "Pharmacy Name",
        "Pharmacy NPI",
        "enrollment_status",
    ]

def test_merge_claims_with_watchlist():
    enrollment_match = pd.DataFrame({
        "NPI": [
            "TEST-001",
            "TEST-003",
            "TEST-004"
        ],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drug",
            "Waterdeep Pharmacy"
        ],
        "Pharmacy NPI": [
            "TEST-001",
            None,
            "TEST-004"
        ],
        "enrollment_status": [
            "both",
            "left_only",
            "both"
        ]
    })
    aggregated_claims = pd.DataFrame({
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Waterdeep Pharmacy"
        ],
        "Pharmacy NPI": [
            "TEST-001",
            "TEST-004"
        ],
        "Claim_Count": [
            2,
            1
        ],
        "Plan_Paid": [
            225,
            150
        ]
    })
    merged = merge_claims_with_watchlist(enrollment_match, aggregated_claims)
    assert merged.shape[0] == 3
    assert merged.loc[merged["NPI"] == "TEST-001", "12 Month Claim Count"].iloc[0] == 2
    assert merged.loc[merged["NPI"] == "TEST-001", "12 Month Plan Paid"].iloc[0] == 225
    assert pd.isna(merged.loc[merged["NPI"] == "TEST-003", "12 Month Claim Count"].iloc[0])
    assert pd.isna(merged.loc[merged["NPI"] == "TEST-003", "12 Month Plan Paid"].iloc[0])
    assert merged.loc[merged["NPI"] == "TEST-003", "claims_status"].iloc[0] == "left_only"
    assert merged.loc[merged["NPI"] == "TEST-004", "12 Month Claim Count"].iloc[0] == 1
    assert merged.loc[merged["NPI"] == "TEST-004", "12 Month Plan Paid"].iloc[0] == 150

def test_merge_claims_not_modifying_originals():
    enrollment_match = pd.DataFrame({
        "NPI": [
            "TEST-001",
            "TEST-003",
            "TEST-004"
        ],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drug",
            "Waterdeep Pharmacy"
        ],
        "Pharmacy NPI": [
            "TEST-001",
            None,
            "TEST-004"
        ],
        "enrollment_status": [
            "both",
            "left_only",
            "both"
        ]
    })
    aggregated_claims = pd.DataFrame({
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Waterdeep Pharmacy"
        ],
        "Pharmacy NPI": [
            "TEST-001",
            "TEST-004"
        ],
        "Claim_Count": [
            2,
            1
        ],
        "Plan_Paid": [
            225,
            150
        ]
    })
    enrollment_copy = enrollment_match.copy()
    aggregated_copy = aggregated_claims.copy()
    merge_claims_with_watchlist(enrollment_match, aggregated_claims)
    pd.testing.assert_frame_equal(enrollment_match, enrollment_copy)
    pd.testing.assert_frame_equal(aggregated_claims, aggregated_copy)

def test_assign_final_status():
    test_df = pd.DataFrame({
        "NPI": [
            "TEST-001",
            "TEST-003",
            "TEST-004"
        ],
        "Pharmacy Name": [
            "Feywild Apothecary",
            "Neverwinter Drugs",
            "Waterdeep Pharmacy"
        ],
        "enrollment_status": [
            "both",
            "left_only",
            "both"
        ],
        "claims_status": [
            "left_only",
            "left_only",
            "both"
        ],
        "12 Month Claim Count": [
            None,
            None,
            150
        ],
        "12 Month Plan Paid": [
            None,
            None,
            34815.50
        ]
    })
    final = assign_final_status(test_df)
    assert final.loc[final["Pharmacy Name"] == "Feywild Apothecary", "Final Status"].iloc[0] == "Participating - No Claims"
    assert final.loc[final["Pharmacy Name"] == "Feywild Apothecary", "12 Month Claim Count"].iloc[0] == 0
    assert final.loc[final["Pharmacy Name"] == "Feywild Apothecary", "12 Month Plan Paid"].iloc[0] == 0
    assert final.loc[final["Pharmacy Name"] == "Neverwinter Drugs", "Final Status"].iloc[0] == "Not Participating"
    assert pd.isna(final.loc[final["Pharmacy Name"] == "Neverwinter Drugs", "12 Month Claim Count"].iloc[0])
    assert pd.isna(final.loc[final["Pharmacy Name"] == "Neverwinter Drugs", "12 Month Plan Paid"].iloc[0])
    assert final.loc[final["Pharmacy Name"] == "Waterdeep Pharmacy", "Final Status"].iloc[0] == "Participating - Has Claims"
    assert final.loc[final["Pharmacy Name"] == "Waterdeep Pharmacy", "12 Month Claim Count"].iloc[0] == 150
    assert final.loc[final["Pharmacy Name"] == "Waterdeep Pharmacy", "12 Month Plan Paid"].iloc[0] == 34815.50

def test_assign_final_status_review_fallback():
    test_df = pd.DataFrame({
        "NPI": [
            "TEST-001"
        ],
        "Pharmacy Name": [
            "Feywild Apothecary"
        ],
        "enrollment_status": [
            "both"
        ],
        "claims_status": [
            "unexpected"
        ],
        "12 Month Claim Count": [
            None
        ],
        "12 Month Plan Paid": [
            None
        ]
    })
    final = assign_final_status(test_df)
    assert final.loc[final["Pharmacy Name"] == "Feywild Apothecary", "Final Status"].iloc[0] == "Review"

def test_assign_final_status_modifies_original():
    test_df = pd.DataFrame({
        "NPI": [
            "TEST-001"
        ],
        "Pharmacy Name": [
            "Feywild Apothecary"
        ],
        "enrollment_status": [
            "both"
        ],
        "claims_status": [
            "left_only"
        ],
        "12 Month Claim Count": [
            None
        ],
        "12 Month Plan Paid": [
            None
        ]
    })
    final = assign_final_status(test_df)
    assert "Final Status" in test_df.columns
    assert test_df.loc[0, "Final Status"] == "Participating - No Claims"
