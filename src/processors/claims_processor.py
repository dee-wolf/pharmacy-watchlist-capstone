import pandas as pd
import math

def load_claims(file_path):
    loaded_claims = pd.read_excel(file_path)
    return loaded_claims

def exclude_test_claims(loaded_claims):
    normalized_names = (loaded_claims["Member Name"].str.strip().str.upper())
    filtered_claims = loaded_claims[normalized_names != "SB393 TEST"]
    return filtered_claims

def aggregate_claims(filtered_claims):
    grouped_claims = filtered_claims.groupby(["Pharmacy Name", "Pharmacy NPI"])
    aggregated_claims = grouped_claims.agg(Claim_Count=("Pharmacy NPI", "size"), Plan_Paid=("Total Paid Amount", "sum"))
    aggregated_claims = aggregated_claims.reset_index()
    aggregated_claims = aggregated_claims.sort_values(by="Plan_Paid", ascending=False)
    total_aggregated_claims = aggregated_claims["Claim_Count"].sum()
    total_filtered_claims = len(filtered_claims)
    if total_aggregated_claims != total_filtered_claims:
        raise ValueError("Claim count reconciliation failed.")
    else:
        print("Claim count reconciliation passed!")
    total_aggregated_paid = aggregated_claims["Plan_Paid"].sum()
    total_filtered_paid = filtered_claims["Total Paid Amount"].sum()
    if not math.isclose(total_aggregated_paid, total_filtered_paid, abs_tol=0.01):
        raise ValueError("Plan paid reconciliation failed.")
    else:
        print("Plan paid reconciliation passed!")
    return aggregated_claims








if __name__ == "__main__":
    loaded_claims = load_claims("data/raw/cognos_claims_minimal.xlsx")
    filtered_claims = exclude_test_claims(loaded_claims)
    aggregated_claims = aggregate_claims(filtered_claims)
    print(aggregated_claims.head())
    print(aggregated_claims.shape)
