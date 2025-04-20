import os
import base64
import binascii
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

response = client.models.compute_tokens(
    model="gemini-2.0-flash-001",
    contents=[{"role": "user", "parts": [{"text": prompt}]}]
)

tokens_info = response.to_json_dict()['tokens_info'][0]

print("List tokens:")
for token_id, token_b64 in zip(tokens_info['token_ids'], tokens_info['tokens']):
    try:
        # Attempt to decode as UTF-8 first
        decoded_bytes = base64.b64decode(token_b64, validate=False)
        token = decoded_bytes.decode('utf-8')
    except (binascii.Error, UnicodeDecodeError) as e:
        try:
            # If UTF-8 fails, try decoding as Latin-1 (ISO-8859-1)
            token = base64.b64decode(token_b64, validate=True).decode('latin-1')
        except (binascii.Error, UnicodeDecodeError) as e2:
            print(f"Error decoding token {token_b64}: {e} and {e2}")
            token = token_b64  # Use the original base64 string if decoding fails
    print(f"- {token_id:>8}: '{token}'")

# Example output:
# tokens_info=[TokensInfo(
#    role='user',
#    token_ids=[1841, 235303, 235256, 573, 32514, 2204, 575, 573, 4645, 5255, 235336],
#    tokens=[b'What', b"'", b's', b' the', b' longest', b' word', b' in', b' the', b' English', b' language', b'?']
#  )]
