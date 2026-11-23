

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlparse

# Project paths
ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "outputs" / "research_results.csv"
OUTPUT_FILE = ROOT / "outputs" / "agent_findings.csv"

# Check input file
if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

# Load research dataset
df = pd.read_csv(INPUT_FILE)

# Select apps requiring verification
pending = df[
    df["research_status"].astype(str).str.strip().str.lower()
    .isin(["needs verification", "pending"])
].copy()

# Test with first 5 apps
# Process all apps requiring verification

# Evidence keywords
evidence_keywords = {
    "API": [
        "api", "rest api", "graphql", "api reference"
    ],
    "Authentication": [
        "authentication", "oauth", "api key",
        "access token", "bearer token"
    ],
    "MCP": [
        "model context protocol", "mcp server",
        "mcp integration"
    ],
    "Webhooks": [
        "webhook", "webhooks"
    ],
    "SDK": [
        "sdk", "software development kit"
    ]
}

results = []

# Start research
for _, app in pending.iterrows():

    app_name = app["app_name"]

    urls = []

    # Collect website and documentation URLs
    for column in ["website", "docs_hint"]:

        value = app.get(column)

        if pd.notna(value):
            value = str(value).strip()

            if value.startswith(("http://", "https://")):
                urls.append(value)

    urls = list(dict.fromkeys(urls))

    if not urls:
        results.append({
            "app_name": app_name,
            "source_url": "",
            "http_status": "",
            "page_title": "",
            "page_text_sample": "",
            "candidate_links": "",
            "detected_evidence": "",
            "scan_status": "No valid URL found"
        })

        print("No URL found:", app_name)
        continue

    # Scan each URL
    for url in urls:

        try:
            response = requests.get(
                url,
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            soup = BeautifulSoup(response.text, "html.parser")

            title = (
                soup.title.get_text(strip=True)
                if soup.title else ""
            )

            # Remove unnecessary HTML elements
            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()

            page_text = " ".join(soup.stripped_strings)
            page_text = page_text[:3000]

            lower_text = page_text.lower()

            # Detect possible evidence
            detected_evidence = []

            for category, terms in evidence_keywords.items():

                matches = [
                    term for term in terms
                    if term in lower_text
                ]

                if matches:
                    detected_evidence.append(
                        category + ": " + ", ".join(matches)
                    )

            # Find relevant documentation links
            base_domain = urlparse(url).netloc

            candidate_links = []

            for link in soup.find_all("a", href=True):

                link_text = link.get_text(" ", strip=True)

                full_url = urljoin(url, link["href"])

                if urlparse(full_url).netloc != base_domain:
                    continue

                searchable_text = (
                    link_text + " " + full_url
                ).lower()

                if any(
                    term in searchable_text
                    for terms in evidence_keywords.values()
                    for term in terms
                ):
                    candidate_links.append(full_url)

            candidate_links = list(dict.fromkeys(candidate_links))

            results.append({
                "app_name": app_name,
                "source_url": url,
                "http_status": response.status_code,
                "page_title": title,
                "page_text_sample": page_text,
                "candidate_links": "; ".join(candidate_links[:20]),
                "detected_evidence": "; ".join(detected_evidence),
                "scan_status": (
                    "Collected"
                    if response.ok
                    else f"HTTP error: {response.status_code}"
                )
            })

            print("Collected:", app_name, "-", url)

        except requests.RequestException as error:

            results.append({
                "app_name": app_name,
                "source_url": url,
                "http_status": "",
                "page_title": "",
                "page_text_sample": "",
                "candidate_links": "",
                "detected_evidence": "",
                "scan_status": str(error)[:200]
            })

            print("Could not access:", app_name, "-", error)

# Save findings
output_df = pd.DataFrame(results)

output_df.to_csv(OUTPUT_FILE, index=False)

print("\nResearch agent test completed!")
print("Apps processed:", len(pending))
print("Pages collected:", len(results))
print("Output saved to:", OUTPUT_FILE)
print("\nNote: Keyword matches are leads for verification, not proof.")
