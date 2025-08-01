#!/usr/bin/env python3
"""
Debug script for Perplexity API
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_perplexity_api():
    """Test the Perplexity API with different models"""
    
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test different models
    models = [
        "llama-3-sonar-large-32k",
        "llama-3-sonar-large-32k-online", 
        "llama-3-sonar-large-32k-chat",
        "llama-3-sonar-medium-32k",
        "llama-3-sonar-small-32k"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for model in models:
        print(f"\n🔍 Testing model: {model}")
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Hello, how are you?"}
            ],
            "max_tokens": 100,
            "temperature": 0.2
        }
        
        try:
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                print(f"✅ {model} - SUCCESS!")
                data = response.json()
                print(f"   Response: {data['choices'][0]['message']['content'][:50]}...")
                return model  # Found working model
            else:
                print(f"❌ {model} - Status: {response.status_code}")
                print(f"   Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ {model} - Exception: {e}")
    
    return None

if __name__ == "__main__":
    working_model = test_perplexity_api()
    if working_model:
        print(f"\n🎉 Working model found: {working_model}")
    else:
        print("\n❌ No working model found") 