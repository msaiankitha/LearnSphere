# test_import.py
import os
import sys

print("=" * 50)
print("🔍 TESTING IMPORTS")
print("=" * 50)

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test Dummy import first (simplest)
    print("Testing Dummy import...")
    from utils.dummy_utils import DummyGemini, extract_code
    print("✅ SUCCESS! Dummy import working!")
    print(f"✅ DummyGemini: {DummyGemini}")
    print(f"✅ extract_code: {extract_code}")
    
    # Test OpenAI import
    print("\nTesting OpenAI import...")
    try:
        from utils.openai_utils import OpenAIUtils
        print("✅ OpenAI import successful!")
    except ImportError as e:
        print(f"⚠️ OpenAI not available: {e}")
        
except ImportError as e:
    print(f"❌ FAILED: {e}")
    
    # Debug: Show what's in the utils folder
    print("\n🔍 Debug Info:")
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in current dir: {os.listdir('.')}")
    
    if os.path.exists('utils'):
        print(f"Files in utils folder: {os.listdir('utils')}")
    else:
        print("❌ utils folder not found!")
        
    print(f"\nPython path: {sys.path}")

print("=" * 50)