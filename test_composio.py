
import os
from dotenv import load_dotenv
from composio import Composio

load_dotenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))

response = composio.client.tools.list()

print("Composio connection successful!")
print("Response received:", type(response).__name__)

print("\nFirst 3 tool details:")
print(response.model_dump_json(indent=2)[:2000])

