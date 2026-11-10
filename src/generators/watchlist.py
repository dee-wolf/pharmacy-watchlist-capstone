import pandas as pd
import random
from datetime import datetime
from .enrollment import generate_enrollment
from .name_parts import pharmacy_names, pharmacy_types

def generate_watchlist(
    num_pharmacies=300,
    reporting_month="2026-11",
    participating_count=250
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
    enrollment_df = generate_enrollment(participating_count)
    participating_npis = enrollment_df["Pharmacy NPI"].tolist()
    nonparticipating_count = num_pharmacies - participating_count
    nonparticipating_npis = [f"OUT-{i:06d}" for i in range(1, nonparticipating_count + 1)]
    all_npis = participating_npis + nonparticipating_npis
    rng = random.Random(42)
    pharmacy_name = f"{rng.choice(pharmacy_names)} {rng.choice(pharmacy_types)}"
    print(pharmacy_name)
    rng.shuffle(all_npis)
    return

if __name__ == "__main__":
    watchlist = generate_watchlist()
    print(watchlist)
