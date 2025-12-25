"""
Test script for TrendForgeAI API
"""

import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    pprint(response.json())
    print()

def test_generate_content():
    """Test content generation"""
    print("🤖 Testing content generation...")
    
    payload = {
        "topic": "AI in Healthcare 2025",
        "platform": "LinkedIn",
        "product_info": "TrendForgeAI - An AI tool that predicts marketing trends and auto-generates viral content.",
        "num_variations": 1
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/api/content/generate",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Content generated successfully!")
        print(f"Job ID: {result['job_id']}")
        print(f"Quality Score: {result['result']['quality_score']}/10")
        print(f"\nGenerated Content:\n{'-'*50}")
        print(result['result']['final_content'])
        print('-'*50)
        return result['result']['id']
    else:
        print(f"❌ Error: {response.text}")
        return None

def test_get_history():
    """Test getting content history"""
    print("\n📜 Testing content history...")
    response = requests.get(f"{BASE_URL}/api/content/history?page=1&page_size=5")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Found {result['total']} content items")
        print(f"Showing page {result['page']} ({len(result['items'])} items)")
        for item in result['items']:
            print(f"\n  - {item['topic']} ({item['platform']})")
            print(f"    Score: {item['quality_score']}/10, Status: {item['status']}")
    else:
        print(f"❌ Error: {response.text}")

def test_get_content(content_id):
    """Test getting specific content"""
    if not content_id:
        return
    
    print(f"\n🔎 Testing get content by ID...")
    response = requests.get(f"{BASE_URL}/api/content/{content_id}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Retrieved content: {result['topic']}")
        print(f"Quality Score: {result['quality_score']}/10")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    print("="*60)
    print("  TrendForgeAI API Test Suite")
    print("="*60)
    print()
    
    # Run tests
    test_health()
    content_id = test_generate_content()
    test_get_history()
    test_get_content(content_id)
    
    print("\n" + "="*60)
    print("  ✅ All tests completed!")
    print("="*60)
