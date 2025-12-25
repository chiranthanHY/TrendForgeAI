import requests

print("Testing basic content generation...")
response = requests.post(
    "http://localhost:8000/api/content/generate",
    json={
        "topic": "Remote Work",
        "platform": "LinkedIn",
        "product_info": "TrendForgeAI",
        "num_variations": 1
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")
