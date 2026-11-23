
import pandas as pd
from pathlib import Path

# Project paths
ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "outputs" / "agent_findings.csv"
OUTPUT_FILE = ROOT / "outputs" / "evidence_summary.csv"

# Load agent findings
df = pd.read_csv(INPUT_FILE).fillna("")

# Evidence categories
categories = [
    "API",
    "Authentication",
    "MCP",
    "Webhooks",
    "SDK"
]

summary = []

# Count evidence by category
for category in categories:

    keyword = category.lower()

    matching_rows = df[
        df["detected_evidence"].str.lower().str.contains(
            keyword, regex=False
        )
    ]

    unique_apps = matching_rows["app_name"].nunique()

    page_count = len(matching_rows)

    summary.append({
        "evidence_category": category,
        "unique_apps_with_matches": unique_apps,
        "page_records_with_matches": page_count
    })

# Save summary report
summary_df = pd.DataFrame(summary)

summary_df.to_csv(OUTPUT_FILE, index=False)

# Display results
print("\n========== EVIDENCE SUMMARY ==========\n")

print(summary_df.to_string(index=False))

print("\n========== SCAN STATUS SUMMARY ==========\n")

print(df["scan_status"].value_counts().to_string())

print("\nTotal page records:", len(df))
print("Unique apps:", df["app_name"].nunique())

print("\nEvidence summary saved successfully!")
print("Output file:", OUTPUT_FILE)

print("\nNote: These are keyword matches, not confirmed capabilities.")
