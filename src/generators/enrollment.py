import pandas as pd

def generate_enrollment(num_pharmacies=250):
    test_npis = []
    if isinstance(num_pharmacies, bool) or not isinstance(num_pharmacies, int):
        raise TypeError("Please enter a whole number.")
    if num_pharmacies <= 0:
        raise ValueError("Please enter a whole number greater than zero.")
    for i in range(1, num_pharmacies + 1):
        npi = f"TEST-{i:06d}"
        test_npis.append(npi)
    df = pd.DataFrame({
        "Pharmacy NPI":test_npis
    })
    df.to_excel("data/raw/enrolled_pharmacies.xlsx", index=False)
    return df

if __name__ == "__main__":
    npis = generate_enrollment(500)
    print(npis.head())
    print(npis.shape)
