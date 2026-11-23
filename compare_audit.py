
import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
AUDIT_FILE = BASE_DIR / "outputs" / "manual_audit.csv"
FINDINGS_FILE = BASE_DIR / "outputs" / "agent_findings.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "audit_comparison.csv"

# Load the two files
audit = pd.read_csv(AUDIT_FILE)
findings = pd.read_csv(FINDINGS_FILE)

# Capabilities to compare
capabilities = {
    "api_verified": "API",
    "authentication_verified": "Authentication",
    "mcp_verified": "MCP",
    "webhooks_verified": "Webhooks",
    "sdk_verified": "SDK"
}

# Combine all findings for each app
findings["app_name"] = findings["app_name"].astype(str).str.strip()
audit["app_name"] = audit["app_name"].astype(str).str.strip()

agent_evidence = {}

for _, row in findings.iterrows():
    app = row["app_name"]

    evidence = str(row.get("detected_evidence", ""))
    title = str(row.get("page_title", ""))
    sample = str(row.get("page_text_sample", ""))

    combined_text = (evidence + " " + title + " " + sample).lower()

    if app not in agent_evidence:
        agent_evidence[app] = ""

    agent_evidence[app] += " " + combined_text

# Compare manual audit with agent evidence
results = []

for _, row in audit.iterrows():
    app = row["app_name"]
    agent_text = agent_evidence.get(app, "")

    result = {
        "app_name": app,
        "category": row["category"]
    }

    verified_count = 0
    detected_count = 0

    for column, keyword in capabilities.items():
        manual_value = str(row[column]).strip().lower()

        # Only compare capabilities manually marked Yes
        if manual_value == "yes":
            verified_count += 1

            found = keyword.lower() in agent_text
            result[column + "_detected_by_agent"] = (
                "Yes" if found else "No"
            )

            if found:
                detected_count += 1
        else:
            result[column + "_detected_by_agent"] = "Not compared"

    result["manual_yes_count"] = verified_count
    result["agent_detected_count"] = detected_count

    if verified_count > 0:
        result["evidence_detection_agreement_percent"] = round(
            detected_count / verified_count * 100, 2
        )
    else:
        result["evidence_detection_agreement_percent"] = "N/A"

    results.append(result)

# Save comparison report
comparison = pd.DataFrame(results)
comparison.to_csv(OUTPUT_FILE, index=False)

print("Comparison completed successfully!")
print("Apps compared:", len(comparison))
print("Output saved to:", OUTPUT_FILE)
print()
print(comparison.to_string(index=False))
