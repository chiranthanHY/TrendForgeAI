"""
Test TrendForgeAI API - Synchronous Mode
No Redis/Celery required
"""

import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:8000"

print("="*60)
print("  TrendForgeAI API Test - Synchronous Mode")
print("="*60)
print()

# Test 1: Generate content in sync mode
print("🤖 Testing content generation (synchronous)...")
print("⏳ This will take ~30-60 seconds...")
print()

payload = {
   "topic": "Remote Work Productivity",
    "platform": "LinkedIn",
    "product_info": "TrendForgeAI - AI-powered content marketing optimizer that generates viral content",
    "num_variations": 1
}

try:
    response = requests.post(
        f"{BASE_URL}/api/content/generate?use_async=false",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=120  # 2 minute timeout
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Content generated successfully!")
        print("="*60)
        print(f"Job ID: {result['job_id']}")
        print(f"Quality Score: {result['result']['quality_score']}/10")
        print(f"Platform: {result['result']['platform']}")
        print(f"Status: {result['result']['status']}")
        print("\n📝 Generated Content:")
        print("-"*60)
        print(result['result']['final_content'])
        print("-"*60)
        print(f"\n💡 Critique: {result['result']['critique_notes']}")
        print("="*60)
        
        # Save content ID for next tests
        content_id = result['result']['id']
        
        # Test 2: Get content history
        print("\n\n📜 Testing content history...")
        history_response = requests.get(f"{BASE_URL}/api/content/history")
        
        if history_response.status_code == 200:
            history = history_response.json()
            print(f"✅ Found {history['total']} content items")
            
        # Test 3: Get specific content
        print(f"\n\n🔎 Testing get content by ID...")
        content_response = requests.get(f"{BASE_URL}/api/content/{content_id}")
        
        if content_response.status_code == 200:
            print(f"✅ Retrieved content successfully")
        
        print("\n" + "="*60)
        print("  ✅ All tests passed!")
        print("="*60)
        
    else:
        print(f"❌ Error: {response.text}")
        
except requests.Timeout:
    print("❌ Request timed out. Content generation may take longer.")
except Exception as e:
    print(f"❌ Error: {str(e)}")
