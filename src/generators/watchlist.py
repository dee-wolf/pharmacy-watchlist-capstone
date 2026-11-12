import pandas as pd
import random
from datetime import datetime
from .enrollment import generate_enrollment
from .name_parts import generate_pharmacy_names
from .watchlist_reasons import watchlist_reasons, reason_weights
from ..validators.watchlist_validator import validate_watchlist

def generate_watchlist(
    num_pharmacies=300,
    reporting_month="2026-11",
    participating_count=250,
    seed=42
):
    if isinstance(num_pharmacies, bool) or not isinstance(num_pharmacies, int):
        raise TypeError("Please enter a whole number.")
    if num_pharmacies <= 0:
        raise ValueError("Please enter a whole number greater than zero.")
    if isinstance(participating_count, bool) or not isinstance(participating_count, int):
        raise TypeError("Please enter a whole number.")
    if participating_count <= 0:
        raise ValueError("Please enter a whole number greater than zero.")
    if participating_count > num_pharmacies:
        raise ValueError("Participating pharmacies cannot exceed total pharmacies.")
    if not isinstance(reporting_month, str):
        raise TypeError("Please use a valid month in YYYY-MM format.")
    try:
        reporting_month = datetime.strptime(reporting_month, "%Y-%m")
    except ValueError:
        raise ValueError("Please use a valid month in YYYY-MM format.")
    if num_pharmacies > len(generate_pharmacy_names()):
        raise ValueError("Not enough unique pharmacy name combinations.")
    months = pd.date_range(end=reporting_month, periods=12, freq="MS")
    enrollment_df = generate_enrollment(participating_count)
    participating_npis = enrollment_df["Pharmacy NPI"].tolist()
    nonparticipating_count = num_pharmacies - participating_count
    nonparticipating_npis = [f"OUT-{i:06d}" for i in range(1, nonparticipating_count + 1)]
    all_npis = participating_npis + nonparticipating_npis
    full_names = generate_pharmacy_names()
    npi_rng = random.Random(seed)
    name_rng = random.Random(seed + 1)
    month_rng = random.Random(seed + 2)
    reason_rng = random.Random(seed + 3)
    detail_rng = random.Random(seed + 4)
    npi_rng.shuffle(all_npis)
    name_rng.shuffle(full_names)
    pharmacy_records = list(zip(all_npis, full_names))
    watchlist_df = pd.DataFrame(pharmacy_records, columns=["NPI", "Pharmacy Name"])
    additions = [reporting_month] * 25
    previous = [month_rng.choice(months[:-1]) for i in range(275)]
    all_months = additions + previous
    month_rng.shuffle(all_months)
    reasons = reason_rng.choices(list(reason_weights.keys()), weights=list(reason_weights.values()), k=num_pharmacies)
    details = [detail_rng.choice(watchlist_reasons[reason]) for reason in reasons]
    watchlist_df["Month Added to List"] = all_months
    watchlist_df["Watch List Reason"] = reasons
    watchlist_df["Addt'l Details of Watch/Review Findings"] = details
    watchlist_df.to_excel(
        "data/raw/monthly_watchlist.xlsx",
        index=False
    )
    return watchlist_df

if __name__ == "__main__":
    watchlist = generate_watchlist()
    validate_watchlist(watchlist)
    print("Watchlist validation passed!")
