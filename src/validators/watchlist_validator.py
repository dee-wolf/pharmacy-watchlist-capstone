import pandas as pd
from generators.watchlist_reasons import watchlist_reasons

def validate_watchlist(
    watchlist,
    expected_count=300,
    expected_participating=250,
    expected_nonparticipating=50
):
    if len(watchlist) != expected_count:
        raise ValueError(
            f"Expected {expected_count} records, received {len(watchlist)}."
        )
    if len(watchlist) != watchlist["NPI"].nunique():
        raise ValueError("Duplicate pharmacy NPIs detected.")
    participating_count = watchlist["NPI"].str.startswith("TEST-").sum()
    nonparticipating_count = watchlist["NPI"].str.startswith("OUT-").sum()
    if expected_participating != participating_count:
        raise ValueError(
            f"Expected {expected_participating} pharmacies participating, received {participating_count}"
        )
    if expected_nonparticipating != nonparticipating_count:
        raise ValueError(
            f"Expected {expected_nonparticipating} pharmacies NOT participating, received {nonparticipating_count}"
        )
