import pandas as pd

def generate_enrollment():
    test_npis = []
    for i in range(1, 251):
        npi = f"TEST-{i:06d}"
        test_npis.append(npi)
    return test_npis

if __name__ == "__main__":
    npis = generate_enrollment()
    df = pd.DataFrame({
        "Pharmacy NPI":npis
    })
    df.to_excel("data/raw/enrolled_pharmacies.xlsx", index=False)
    enrollment_df = pd.read_excel("data/raw/enrolled_pharmacies.xlsx")
    print(enrollment_df.head())
    print(enrollment_df.shape)
