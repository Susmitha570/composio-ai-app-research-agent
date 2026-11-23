
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Locate project folders
project_root = Path(__file__).resolve().parents[1]

input_file = project_root / "data" / "apps.csv"
output_file = project_root / "outputs" / "website_scan.csv"

# Load original app dataset
df = pd.read_csv(input_file)

# Test with the first 5 apps only
sample = df.head(5)

results = []

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; AppResearchBot/1.0)"
}

for _, app in sample.iterrows():

    app_name = app["app_name"]
    website = app["website"]

    print(f"\nResearching: {app_name}")

    result = {
        "app_name": app_name,
        "website": website,
        "http_status": "",
        "page_title": "",
        "meta_description": "",
        "scan_status": ""
    }

    try:
        if pd.isna(website) or not str(website).strip():
            raise ValueError("Website URL is missing")

        response = requests.get(
            website,
            headers=headers,
            timeout=20
        )

        result["http_status"] = response.status_code

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        if soup.title:
            result["page_title"] = soup.title.get_text(strip=True)

        meta = soup.find("meta", attrs={"name": "description"})

        if meta:
            result["meta_description"] = meta.get("content", "")

        result["scan_status"] = "Success"

    except Exception as error:
        result["scan_status"] = f"Failed: {error}"

    results.append(result)

    print("Status:", result["scan_status"])

# Save scan results
pd.DataFrame(results).to_csv(output_file, index=False)

print("\nWebsite scanning completed!")
print("Apps scanned:", len(results))
print("Results saved to:", output_file)
