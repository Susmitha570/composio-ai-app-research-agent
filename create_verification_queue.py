
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

input_file = ROOT / "outputs" / "research_results.csv"
output_file = ROOT / "outputs" / "verification_queue.csv"

df = pd.read_csv(input_file)

pending = df[
    df["research_status"].astype(str).str.strip()
    .str.lower().isin(["needs verification", "pending"])
].copy()

columns = [
    "app_name",
    "category",
    "authentication_methods",
    "credential_access",
    "api_breadth",
    "mcp_available",
    "buildability_verdict",
    "main_blocker",
    "evidence_urls",
    "research_status"
]

pending[columns].to_csv(output_file, index=False)

print("Verification queue created successfully!")
print("Apps requiring verification:", len(pending))
print("Saved to:", output_file)
