#!/usr/bin/env python3
"""
Test script for Task 2: API Key Authentication
Note: You need to replace the API_KEY variables with actual keys from console output.
"""

import requests
import json

API_URL = "http://localhost:5001"

# NOTE: These are example keys. Replace with actual keys from console when running app.py
API_KEY_1 = "REPLACE_WITH_KEY1_FROM_CONSOLE"
API_KEY_2 = "REPLACE_WITH_KEY2_FROM_CONSOLE"
API_KEY_3 = "REPLACE_WITH_KEY3_FROM_CONSOLE"
INVALID_KEY = "invalid-key-12345"

def test_with_key(api_key, test_num):
    """Test API with a specific key."""
    
    print(f"\nTest {test_num}: Testing with API key...")
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    
    data = {
        "text": "hello world from test"
    }
    
    try:
        response = requests.post(f"{API_URL}/process", headers=headers, json=data)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Success - Valid key")
            return True
        elif response.status_code == 401:
            print("   ❌ Unauthorized - Invalid key")
            return False
        else:
            print(f"   ❌ Unexpected response")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to Flask API at {API_URL}")
        print("   Make sure Task 2 Flask app is running:")
        print("     cd Task2")
        print("     python app.py")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_missing_key():
    """Test API without any API key."""
    
    print("\nTest 4: Testing without API key...")
    
    headers = {
        "Content-Type": "application/json"
        # No X-API-Key header
    }
    
    data = {
        "text": "hello world"
    }
    
    try:
        response = requests.post(f"{API_URL}/process", headers=headers, json=data)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 401:
            print("   ✅ Expected - Missing key should return 401")
            return True
        else:
            print("   ❌ Unexpected response for missing key")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to Flask API")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_invalid_payload():
    """Test API with invalid payload."""
    
    print("\nTest 5: Testing with invalid payload (no text field)...")
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY_1
    }
    
    data = {
        "wrong_field": "hello world"
    }
    
    try:
        response = requests.post(f"{API_URL}/process", headers=headers, json=data)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 400:
            print("   ✅ Expected - Missing required field")
            return True
        else:
            print("   ❌ Unexpected response for invalid payload")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to Flask API")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_health_endpoint():
    """Test health endpoint."""
    
    print("\nTest 6: Testing health endpoint...")
    
    try:
        response = requests.get(f"{API_URL}/health")
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Health check passed")
            return True
        else:
            print("   ❌ Health check failed")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to Flask API")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Main test function."""
    
    print("=" * 60)
    print("Testing Task 2: API Key Authentication")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: Run Task 2 Flask app first (python app.py)")
    print("   and replace API_KEY variables in this script with actual keys")
    print("   from the console output.")
    print("=" * 60)
    
    if API_KEY_1.startswith("REPLACE"):
        print("\n❌ ERROR: Please replace API_KEY variables with actual keys!")
        print("1. Start Task 2 app: cd Task2 && python app.py")
        print("2. Copy the 3 API keys from console output")
        print("3. Update API_KEY_1, API_KEY_2, API_KEY_3 in this script")
        return
    
    print(f"\nTesting with:")
    print(f"  API Key 1: {API_KEY_1[:20]}...")
    print(f"  API Key 2: {API_KEY_2[:20]}...")
    print(f"  API Key 3: {API_KEY_3[:20]}...")
    print(f"  Invalid Key: {INVALID_KEY}")
    
    results = []
    
    # Test 1-3: Valid keys
    results.append(test_with_key(API_KEY_1, 1))
    results.append(test_with_key(API_KEY_2, 2))
    results.append(test_with_key(API_KEY_3, 3))
    
    # Test 4: Invalid key
    results.append(test_with_key(INVALID_KEY, "4 (Invalid)"))
    
    # Test 5: Missing key
    results.append(test_missing_key())
    
    # Test 6: Invalid payload
    results.append(test_invalid_payload())
    
    # Test 7: Health endpoint
    results.append(test_health_endpoint())
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r)
    total_tests = len(results)
    
    print(f"Passed: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("✅ All tests passed!")
    else:
        print(f"⚠️  {total_tests - success_count} tests failed")
    
    print("=" * 60)

if __name__ == "__main__":
    main()