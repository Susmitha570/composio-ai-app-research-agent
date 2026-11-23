
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)

# Load datasets
apps = pd.read_csv(BASE_DIR / "data" / "apps.csv")
research = pd.read_csv(OUTPUT_DIR / "research_results.csv")
audit = pd.read_csv(OUTPUT_DIR / "manual_audit.csv")
comparison = pd.read_csv(OUTPUT_DIR / "audit_comparison.csv")
findings = pd.read_csv(OUTPUT_DIR / "agent_findings.csv")

# Calculate totals
total_apps = apps["app_name"].nunique()
researched_apps = research["app_name"].nunique()
audited_apps = audit["app_name"].nunique()

# Average evidence detection agreement
scores = pd.to_numeric(
    comparison["evidence_detection_agreement_percent"],
    errors="coerce"
)
average_agreement = scores.mean()

# Agent scan status counts
scan_status = findings["scan_status"].value_counts()

# Category distribution
category_counts = apps.groupby("category")["app_name"].nunique()

# Research status distribution
research_status = research["research_status"].value_counts()

# Build report
report = []

report.append("COMPOSIO AI APP RESEARCH AGENT - FINAL SUMMARY")
report.append("=" * 55)
report.append("")
report.append(f"Total apps in dataset: {total_apps}")
report.append(f"Apps in research results: {researched_apps}")
report.append(f"Apps manually audited: {audited_apps}")
report.append(f"Agent page records collected: {len(findings)}")

report.append("")
report.append("EVIDENCE DETECTION")
report.append("-" * 30)
report.append(
    f"Average evidence-detection agreement: "
    f"{average_agreement:.2f}%"
    if pd.notna(average_agreement)
    else "Average evidence-detection agreement: N/A"
)
report.append(
    "Note: This is keyword evidence-detection agreement, "
    "not factual accuracy."
)

report.append("")
report.append("CATEGORY DISTRIBUTION")
report.append("-" * 30)
for category, count in category_counts.items():
    report.append(f"{category}: {count} apps")

report.append("")
report.append("RESEARCH STATUS")
report.append("-" * 30)
for status, count in research_status.items():
    report.append(f"{status}: {count}")

report.append("")
report.append("AGENT SCAN STATUS")
report.append("-" * 30)
for status, count in scan_status.items():
    report.append(f"{status}: {count}")

report.append("")
report.append("LIMITATIONS")
report.append("-" * 30)
report.append(
    "1. Keyword detection does not independently prove a capability."
)
report.append(
    "2. Some official documentation pages may block automated access."
)
report.append(
    "3. Some pages may time out or return errors."
)
report.append(
    "4. Manual verification is required before final capability claims."
)
report.append(
    "5. The audit covers a sample of 20 apps, not all 100 apps."
)

# Save report
report_text = "\n".join(report)

report_file = REPORT_DIR / "final_summary.txt"
report_file.write_text(report_text, encoding="utf-8")

print(report_text)
print("\nSummary saved to:", report_file)
