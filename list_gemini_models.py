import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

USE_VERTEX = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "0") == "1"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not USE_VERTEX:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    genai.configure()

print("Listing available Gemini/Generative AI models...")
for model in genai.list_models():
    print(f"Model name: {model.name}")
    print(f"  Supported methods: {getattr(model, 'supported_methods', [])}")
    print()
