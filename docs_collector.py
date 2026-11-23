
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "apps.csv"
OUTPUT_FILE = ROOT / "outputs" / "documentation_links.csv"

df = pd.read_csv(INPUT_FILE)

# Test with the same first five apps
sample = df.head(5)

headers = {
    "User-Agent": "Mozilla/5.0"
}

results = []

for _, app in sample.iterrows():

    app_name = app["app_name"]

    # Collect available starting URLs
    urls = []

    for column in ["docs_hint", "website"]:
        value = app.get(column)

        if pd.notna(value) and str(value).startswith("http"):
            urls.append(str(value).strip())

    urls = list(dict.fromkeys(urls))

    print(f"\nChecking documentation for: {app_name}")

    found_links = []
    scan_notes = []

    for url in urls:

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=20
            )

            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):

                href = urljoin(url, link["href"])

                if urlparse(href).scheme not in ["http", "https"]:
                    continue

                text = link.get_text(" ", strip=True).lower()
                target = href.lower()

                keywords = [
                    "api",
                    "developer",
                    "documentation",
                    "docs",
                    "authentication",
                    "oauth",
                    "mcp"
                ]

                if any(word in text or word in target for word in keywords):
                    found_links.append(href)

            scan_notes.append(f"Checked: {url}")

        except Exception as error:
            scan_notes.append(f"Failed: {url} - {error}")

    found_links = list(dict.fromkeys(found_links))

    results.append({
        "app_name": app_name,
        "starting_urls": " | ".join(urls),
        "documentation_links": " | ".join(found_links),
        "number_of_links": len(found_links),
        "scan_notes": " | ".join(scan_notes)
    })

    print("Documentation links found:", len(found_links))

pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)

print("\nDocumentation collection completed!")
print("Apps processed:", len(results))
print("Saved to:", OUTPUT_FILE)
