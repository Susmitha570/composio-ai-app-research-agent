
import pandas as pd

# Load the dataset
df = pd.read_csv("data/apps.csv")

print("DATASET VALIDATION")
print("------------------")

print("Total apps:", len(df))
print("Total categories:", df["category"].nunique())

print("\nApps in each category:")
print(df["category"].value_counts())

print("\nDuplicate apps:", df["app_name"].duplicated().sum())

print("\nStatus counts:")
print(df["status"].value_counts())

# Validation checks
assert len(df) == 100, "Dataset should contain 100 apps"
assert df["category"].nunique() == 10, "Dataset should contain 10 categories"
assert df["app_name"].duplicated().sum() == 0, "Duplicate apps found"

print("\nAll validation checks passed!")
