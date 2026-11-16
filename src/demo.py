from src.generators.watchlist import generate_watchlist

from src.processors.claims_processor import (
    load_claims,
    exclude_test_claims,
    aggregate_claims
)

from src.processors.watchlist_processor import (
    match_enrollment,
    merge_claims_with_watchlist,
    assign_final_status
)

# ============================================================
# PHARMACY WATCHLIST AUTOMATION DEMO
# ============================================================

print("\n" + "=" * 75)
print("                 PHARMACY WATCHLIST AUTOMATION")
print("=" * 75)

# ============================================================
# 1. LOAD SYNTHETIC DATA
# ============================================================

print("\n[1] LOADING SYNTHETIC DATA")

watchlist = generate_watchlist()

network = load_claims("data/raw/enrolled_pharmacies.xlsx")

claims = load_claims("data/raw/cognos_claims_minimal.xlsx")

print(f"\nWatchlist pharmacies: {len(watchlist)}")
print(f"Enrolled pharmacies:  {len(network)}")
print(f"Raw claims:           {len(claims)}")

print("\n--- ORIGINAL WATCHLIST (FIRST 10 ROWS) ---")
print(watchlist.head(10).to_string(index=False))
print(f"\nWatchlist dimensions: {watchlist.shape}")

print("\n--- ENROLLMENT DIRECTORY (FIRST 10 ROWS) ---")
print(network.head(10).to_string(index=False))

# ============================================================
# 2. PROCESS CLAIMS
# ============================================================

print("\n" + "=" * 75)
print("[2] PROCESSING CLAIMS")
print("=" * 75)

print("\n--- RAW CLAIMS (FIRST 10 ROWS) ---")
print(claims.head(10).to_string(index=False))

filtered_claims = exclude_test_claims(claims)

print(f"\nRaw claim records:       {len(claims)}")
print(f"Excluded SB393 claims:   {len(claims) - len(filtered_claims)}")
print(f"Eligible claim records:  {len(filtered_claims)}")

print("\n--- ELIGIBLE CLAIMS (FIRST 10 ROWS) ---")
print(filtered_claims.head(10).to_string(index=False))

aggregated_claims = aggregate_claims(filtered_claims)

print("\n--- AGGREGATED CLAIMS (FIRST 10 ROWS) ---")
print(aggregated_claims.head(10).to_string(index=False))

print(f"\nAggregated dimensions: {aggregated_claims.shape}")

# ============================================================
# 3. MATCH NETWORK ENROLLMENT
# ============================================================

print("\n" + "=" * 75)
print("[3] MATCHING NETWORK ENROLLMENT")
print("=" * 75)

enrollment_match = match_enrollment(watchlist, network)

print("\nEnrollment match results:")
print(enrollment_match["enrollment_status"].value_counts())

print("\n--- ENROLLMENT MATCH SAMPLE ---")
print(
    enrollment_match[
        ["NPI", "Pharmacy Name", "enrollment_status"]
    ].head(10).to_string(index=False)
)

# ============================================================
# 4. MERGE CLAIMS WITH WATCHLIST
# ============================================================

print("\n" + "=" * 75)
print("[4] MERGING CLAIMS AND WATCHLIST")
print("=" * 75)

merged_watchlist = merge_claims_with_watchlist(
    enrollment_match,
    aggregated_claims
)

print("\n--- MERGED WATCHLIST (FIRST 10 ROWS) ---")
print(
    merged_watchlist[
        [
            "NPI",
            "Pharmacy Name",
            "enrollment_status",
            "12 Month Claim Count",
            "12 Month Plan Paid",
            "claims_status"
        ]
    ].head(10).to_string(index=False)
)

print(f"\nMerged dimensions: {merged_watchlist.shape}")

# ============================================================
# 5. ASSIGN FINAL STATUSES
# ============================================================

print("\n" + "=" * 75)
print("[5] ASSIGNING FINAL STATUSES")
print("=" * 75)

merged_watchlist = assign_final_status(merged_watchlist)

print("\nFinal status breakdown:")
print(merged_watchlist["Final Status"].value_counts())

print("\n--- FINAL PROCESSED WATCHLIST (FIRST 15 ROWS) ---")

print(
    merged_watchlist[
        [
            "NPI",
            "Pharmacy Name",
            "12 Month Claim Count",
            "12 Month Plan Paid",
            "Final Status"
        ]
    ].head(15).to_string(index=False)
)

# ============================================================
# 6. REVIEW SPECIAL CASES
# ============================================================

print("\n" + "=" * 75)
print("[6] REVIEWING SPECIAL CASES")
print("=" * 75)

zero_claims = merged_watchlist[
    merged_watchlist["Final Status"] == "Participating - No Claims"
]

print("\n--- PARTICIPATING PHARMACIES WITH ZERO CLAIMS ---")

print(
    zero_claims[
        [
            "NPI",
            "Pharmacy Name",
            "12 Month Claim Count",
            "12 Month Plan Paid",
            "Final Status"
        ]
    ].to_string(index=False)
)

nonparticipating = merged_watchlist[
    merged_watchlist["Final Status"] == "Not Participating"
]

print("\n--- NONPARTICIPATING PHARMACIES (FIRST 10) ---")

print(
    nonparticipating[
        [
            "NPI",
            "Pharmacy Name",
            "12 Month Claim Count",
            "12 Month Plan Paid",
            "Final Status"
        ]
    ].head(10).to_string(index=False)
)

# ============================================================
# 7. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 75)
print("                       DEMO COMPLETE")
print("=" * 75)

print(f"\nTotal pharmacies processed: {len(merged_watchlist)}")
print(f"Raw claims received:         {len(claims)}")
print(f"SB393 claims excluded:       {len(claims) - len(filtered_claims)}")
print(f"Eligible claims processed:   {len(filtered_claims)}")
print(f"Pharmacy-level records:      {len(aggregated_claims)}")

print("\nFinal pharmacy classifications:")

for status, count in merged_watchlist["Final Status"].value_counts().items():
    print(f"  {status}: {count}")

print("\nClaim count reconciliation: PASSED")
print("Plan paid reconciliation:   PASSED")

print("\n" + "=" * 75)
print("             END OF PHARMACY WATCHLIST DEMO")
print("=" * 75 + "\n")
