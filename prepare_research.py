
import pandas as pd
from pathlib import Path

# Locate the project folder
ROOT = Path(__file__).resolve().parents[1]

# Input files
apps_file = ROOT / "data" / "apps.csv"
research_file = ROOT / "data" / "research_input.csv"

# Output file
output_file = ROOT / "outputs" / "research_results.csv"

# Read both datasets
apps = pd.read_csv(apps_file)
research = pd.read_csv(research_file)

# Research columns
research_columns = [
    "description",
    "authentication_methods",
    "credential_access",
    "api_breadth",
    "mcp_available",
    "buildability_verdict",
    "main_blocker",
    "evidence_urls",
    "research_notes",
    "confidence",
    "research_status"
]

# Check for duplicate research records
if research["app_name"].duplicated().any():
    raise ValueError("Duplicate app names found in research_input.csv")

# Keep only the research columns needed
research = research[["app_name"] + research_columns]

apps["app_name"] = apps["app_name"].astype(str).str.strip()
research["app_name"] = research["app_name"].astype(str).str.strip()

print("Apps names:", apps["app_name"].head(5).tolist())
print("Research names:", research["app_name"].tolist())

# Combine original apps with research findings
final_df = apps.merge(
    research,
    on="app_name",
    how="left"
)

# Mark apps without research as Pending
final_df["research_status"] = (
    final_df["research_status"].fillna("Pending")
)

# Save consolidated results
output_file.parent.mkdir(parents=True, exist_ok=True)
final_df.to_csv(output_file, index=False)

print("\nRESEARCH DATASET GENERATED SUCCESSFULLY!")
print("----------------------------------------")
print("Total applications:", len(final_df))
print("Research completed:", (final_df["research_status"] == "Verified").sum())
print("Research pending:", (final_df["research_status"] == "Pending").sum())
print("Output file:", output_file)

