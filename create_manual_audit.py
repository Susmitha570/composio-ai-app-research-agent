
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "outputs" / "research_results.csv"
OUTPUT_FILE = ROOT / "outputs" / "manual_audit.csv"

df = pd.read_csv(INPUT_FILE)

# Select 2 apps from each category
sample = (
    df.drop_duplicates(subset="app_name")
      .groupby("category", group_keys=False)
      .head(2)
      .copy()
)

# Create a manual verification template
audit = sample[["app_name", "category"]].copy()

audit["official_docs_url"] = ""
audit["api_verified"] = ""
audit["authentication_verified"] = ""
audit["mcp_verified"] = ""
audit["webhooks_verified"] = ""
audit["sdk_verified"] = ""
audit["agent_accuracy"] = ""
audit["manual_notes"] = ""

audit.to_csv(OUTPUT_FILE, index=False)

print("Manual audit sample created!")
print("Apps selected:", len(audit))
print("\nApps by category:")
print(audit.groupby("category")["app_name"].count())

print("\nSaved to:", OUTPUT_FILE)
