import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Test OpenAI API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="Reply with: OpenAI API is working!"
    )
    print("OpenAI:", response.output_text)

except Exception as e:
    print("OpenAI error:", e)