import os
from google import genai
from google.genai.types import HttpOptions

from dotenv import load_dotenv

# Check if .env file exists and load it
if os.path.exists(".env"):
    load_dotenv()
else:
    print("Warning: .env file not found. Using environment variables directly.")
    GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")
    GOOGLE_CLOUD_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION") == "us-central1"
    GOOGLE_GENAI_USE_VERTEXAI = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI") == "True"

client = genai.Client(http_options=HttpOptions(api_version="v1"))

# Read the prompt from prompt.txt
try:
    with open("prompt.txt", "r") as f:
        prompt = f.read().strip()
except FileNotFoundError:
    print("Error: prompt.txt not found.")
    exit()

# Send text to Gemini
response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=prompt
)

# Prompt and response tokens count
usage_metadata = response.usage_metadata

# Print out token values with max 8-digits and right-align
# TODO: Flexible digits' size.

if usage_metadata:
    print("Usage Metadata:")
    if usage_metadata.prompt_token_count:
        print(f"- {usage_metadata.prompt_token_count:>8}: Prompt (Input) Tokens")
    if usage_metadata.candidates_token_count:
        print(f"- {usage_metadata.candidates_token_count:>8}: Response (Output) Tokens")
    if usage_metadata.total_token_count:
        print(f"- {usage_metadata.total_token_count:>8}: Total Tokens")
    if usage_metadata.cached_content_token_count:
        print(f"- {usage_metadata.cached_content_token_count:>8}: Cached Content Tokens")
else:
    print("No usage metadata available.")

# Example output:
#  cached_content_token_count=None
#  candidates_token_count=311
#  prompt_token_count=6
#  total_token_count=317
