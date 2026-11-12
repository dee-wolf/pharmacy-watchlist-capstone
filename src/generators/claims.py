import pandas as pd
import random
from datetime import datetime
from .watchlist import generate_watchlist
from .member_names import generate_member_names

def generate_claims(watchlist, num_claims = 1500, seed = 1, test_claims=30):
    if isinstance(num_claims, bool) or not isinstance(num_claims, int):
        raise TypeError("Please enter a whole number for the number of claims.")
    if num_claims <= 0:
        raise ValueError("Please enter a whole number greater than zero for the number of claims.")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("Please enter a whole nummber for the seed.")
    if isinstance(test_claims, bool) or not isinstance(test_claims, int):
        raise TypeError("Please enter a whole number for the number of test claims.")
    if test_claims < 0:
        raise ValueError("Please enter zero or a positive number of test claims.")
    if test_claims > num_claims:
        raise ValueError("Test claims cannot exceed total claims.")
    claims_rng = random.Random(seed)
    participating_pharmacies = watchlist[watchlist["NPI"].str.startswith("TEST-")]
    npis = list(participating_pharmacies["NPI"])
    if not npis:
        raise ValueError("NPI List is empty.")
    pharmacy_names = list(participating_pharmacies["Pharmacy Name"])
    claim_npis = claims_rng.choices(npis, k=num_claims)
    pharmacy_lookup = dict(zip(npis, pharmacy_names))
    claim_pharmacy_names = [pharmacy_lookup[npi] for npi in claim_npis]
    members = generate_member_names()
    claim_members = claims_rng.choices(members, k=num_claims)
    claim_paid_amounts = [round(claims_rng.uniform(5.00, 5000.00), 2) for _ in range(num_claims)]
    test_indices = claims_rng.sample(range(num_claims), k=test_claims)
    for index in test_indices:
        claim_members[index] = "SB393 TEST"
    claims_df = pd.DataFrame({
        "Member Name": claim_members,
        "Pharmacy Name": claim_pharmacy_names,
        "Pharmacy NPI": claim_npis,
        "Total Paid Amount": claim_paid_amounts
    })
    claims_df.to_excel("data/raw/cognos_claims_minimal.xlsx", index=False)
    return claims_df

if __name__ == "__main__":
    from .watchlist import generate_watchlist

    watchlist = generate_watchlist()
    claims = generate_claims(watchlist)
    print(claims.head())
    print(claims.shape)
    print(claims.dtypes)
