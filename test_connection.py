import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

print("Testing Gemini API connection...")

try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(
        "Say hello in one word",
        request_options={'timeout': 30}
    )
    print(f"✅ Success! Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying alternative model...")
    try:
        model = genai.GenerativeModel('gemini-pro-latest')
        response = model.generate_content("Say hello in one word")
        print(f"✅ Success with alternative! Response: {response.text}")
    except Exception as e2:
        print(f"❌ Alternative also failed: {e2}")
