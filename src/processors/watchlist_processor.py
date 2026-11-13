import pandas as pd

def merge_claims_with_watchlist(watchlist, aggregated_claims):
    merged_watchlist = watchlist.merge(
        aggregated_claims,
        how="left",
        left_on="NPI",
        right_on="Pharmacy NPI",
    )
    return merged_watchlist

def match_enrollment(watchlist, network):
    matched_watchlist = watchlist.merge(
        network,
        how="left",
        left_on="NPI",
        right_on="Pharmacy NPI",
        indicator=True
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
    merged_watchlist = merge_claims_with_watchlist(
        watchlist, aggregated_claims
    )
    enrollment_match = match_enrollment(watchlist, network)

    print(enrollment_match["_merge"].value_counts())
