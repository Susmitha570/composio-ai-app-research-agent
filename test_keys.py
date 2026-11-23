import os
from dotenv import load_dotenv

load_dotenv()

print("Composio:", bool(os.getenv("COMPOSIO_API_KEY")))
print("OpenAI:", bool(os.getenv("OPENAI_API_KEY")))