import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found. Check your .env file.")
    raise SystemExit(1)

print(f"Using model: {model_name}")
print("Sending a test prompt to Gemini...")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model=model_name,
    contents="In one sentence, explain what a capstone project is.",
)

print("\n--- Gemini's response ---")
print(response.text)
print("--------------------------")
print("\nSuccess! Your API key and SDK setup are working.")