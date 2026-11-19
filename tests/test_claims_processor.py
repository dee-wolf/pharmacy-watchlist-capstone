import pandas as pd
from src.processors.claims_processor import exclude_test_claims

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
