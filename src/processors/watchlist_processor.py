import pandas as pd

def merge_claims_with_watchlist(enrollment_match, aggregated_claims):
    claims_to_merge = aggregated_claims[
        ["Pharmacy NPI", "Claim_Count", "Plan_Paid"]
    ]
    merged_watchlist = enrollment_match.merge(
        claims_to_merge,
        how="left",
        left_on="NPI",
        right_on="Pharmacy NPI",
        indicator="claims_status"
    )
    merged_watchlist = merged_watchlist.drop(
        columns=["Pharmacy NPI_x", "Pharmacy NPI_y"]
    )
    merged_watchlist = merged_watchlist.rename(
        columns={
            "Claim_Count": "12 Month Claim Count",
            "Plan_Paid": "12 Month Plan Paid"
        }
    )
    return merged_watchlist

def assign_final_status(merged_watchlist):
    merged_watchlist["Final Status"] = "Review"
    merged_watchlist.loc[
        merged_watchlist["enrollment_status"] == "left_only",
        "Final Status"
    ] = "Not Participating"
    merged_watchlist.loc[
        (merged_watchlist["enrollment_status"] == "both") &
        (merged_watchlist["claims_status"] == "left_only"),
        "Final Status"
    ] = "Participating - No Claims"
    merged_watchlist.loc[
        (merged_watchlist["enrollment_status"] == "both") &
        (merged_watchlist["claims_status"] == "both"),
        "Final Status"
    ] = "Participating - Has Claims"
    no_claims = (
        merged_watchlist["Final Status"] == "Participating - No Claims"
    )

    merged_watchlist.loc[
        no_claims,
        ["12 Month Claim Count", "12 Month Plan Paid"]
    ] = 0
    return merged_watchlist

def match_enrollment(watchlist, network):
    matched_watchlist = watchlist.merge(
        network,
        how="left",
        left_on="NPI",
        right_on="Pharmacy NPI",
        indicator="enrollment_status"
    )
    return matched_watchlist

if __name__ == "__main__":
    from src.generators.watchlist import generate_watchlist
    from src.processors.claims_processor import (
        load_claims,
        exclude_test_claims,
        aggregate_claims
    )

    watchlist = generate_watchlist()

    loaded_claims = load_claims("data/raw/cognos_claims_minimal.xlsx")
    filtered_claims = exclude_test_claims(loaded_claims)
    aggregated_claims = aggregate_claims(filtered_claims)

    network = load_claims("data/raw/enrolled_pharmacies.xlsx")

    enrollment_match = match_enrollment(watchlist, network)

    merged_watchlist = merge_claims_with_watchlist(
        enrollment_match, aggregated_claims
    )
    merged_watchlist = assign_final_status(merged_watchlist)
    no_claims = merged_watchlist[
        (merged_watchlist["enrollment_status"] == "both") &
        (merged_watchlist["12 Month Claim Count"].isna())
    ]
    print(merged_watchlist[
        merged_watchlist["Final Status"] == "Participating - No Claims"
    ])

    print(merged_watchlist[
        merged_watchlist["Final Status"] == "Not Participating"
    ][["12 Month Claim Count", "12 Month Plan Paid"]].isna().sum())
