
"""
Generate synthetic pharmacy watchlist data
for the Pharmacy Watchlist Analytics Pipeline.
"""

from src.generators.watchlist import generate_watchlist
from src.generators.enrollment import generate_enrollment
from src.generators.claims import generate_claims


def generate_synthetic_data():
    print("Starting synthetic data generation...")

    print("\nGenerating synthetic pharmacy watchlist...")
    watchlist = generate_watchlist()
    print(f"Generated {len(watchlist)} watchlist records.")

    print("\nGenerating synthetic enrollment directory...")
    enrollment = generate_enrollment()
    print(f"Generated {len(enrollment)} enrollment records.")

    print("\nGenerating synthetic COGNOS claims data...")
    claims = generate_claims(watchlist)
    print(f"Generated {len(claims)} claims records.")

    print("\nSynthetic data generation complete!")
    return watchlist, enrollment, claims

if __name__ == "__main__":
    generate_synthetic_data()
