#!/usr/bin/env python
"""
Test script to verify if the Gemini API key is working
"""

import os
from dotenv import load_dotenv
import requests

def test_gemini_api_key():
    """Test if the Gemini API key is valid and working"""
    
    print("🔍 Testing Gemini API Key...")
    print("-" * 50)
    
    # Load environment variables
    load_dotenv()
    load_dotenv(dotenv_path='.env')
    load_dotenv(dotenv_path='../.env')
    
    # Get API key
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ No API key found in environment variables")
        return False
    
    if api_key == 'YOUR_GEMINI_API_KEY_HERE':
        print("❌ API key is still the placeholder value")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Test the API key with a simple request
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Hello, this is a test. Please respond with 'API key is working!'"
                }]
            }]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        print("🔄 Testing API key with Gemini...")
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ API key is valid and working!")
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"📝 Response: {text}")
            return True
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_api_key()
    
    if not success:
        print("\n" + "="*60)
        print("🔧 HOW TO FIX:")
        print("="*60)
        print("1. Go to: https://makersuite.google.com/app/apikey")
        print("2. Create a NEW API key (the current one might be invalid)")
        print("3. Copy the new key")
        print("4. Replace the key in your .env file")
        print("5. Run this test again")
        print("="*60)