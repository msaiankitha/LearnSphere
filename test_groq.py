# test_groq_fixed.py
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("🔍 TESTING GROQ API - FIXED VERSION")
print("=" * 50)

api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    print("❌ GROQ_API_KEY not found in .env")
    exit(1)

print(f"✅ API Key found: {api_key[:8]}...")

try:
    # ❌ DON'T add base_url
    # ✅ Initialize client WITHOUT base_url
    client = Groq(api_key=api_key)
    
    print("✅ Client initialized successfully")
    print(f"✅ Using model: {os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')}")
    
    response = client.chat.completions.create(
        model=os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile'),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello from Groq API!' in exactly 4 words"}
        ],
        temperature=0,
        max_tokens=20
    )
    
    print(f"✅ Response: {response.choices[0].message.content}")
    print("✅ Groq API is WORKING!")
    print("✅ Your API key and configuration are CORRECT!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Troubleshooting:")
    print("  1. Check that GROQ_API_KEY is correct in .env")
    print("  2. Make sure no GROQ_BASE_URL is set")
    print("  3. Run: pip install --upgrade groq")
    print("  4. Verify at: https://console.groq.com/keys")

print("=" * 50)