import requests
import json

BASE_URL = "http://localhost:5000"

def test_create_string():
    print("\n=== Testing POST /strings ===")
    
    # Test successful creation
    data = {"value": "racecar"}
    response = requests.post(f"{BASE_URL}/strings", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test duplicate (should get 409)
    response = requests.post(f"{BASE_URL}/strings", json=data)
    print(f"\nDuplicate Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test missing value field (should get 400)
    response = requests.post(f"{BASE_URL}/strings", json={})
    print(f"\nMissing field Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test invalid type (should get 422)
    response = requests.post(f"{BASE_URL}/strings", json={"value": 123})
    print(f"\nInvalid type Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_get_string():
    print("\n=== Testing GET /strings/{string_value} ===")
    
    # Create a string first
    requests.post(f"{BASE_URL}/strings", json={"value": "hello world"})
    
    # Get the string
    response = requests.get(f"{BASE_URL}/strings/hello world")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test non-existent string (should get 404)
    response = requests.get(f"{BASE_URL}/strings/nonexistent")
    print(f"\nNon-existent Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_get_all_with_filters():
    print("\n=== Testing GET /strings with filters ===")
    
    # Create some test strings
    test_strings = [
        "racecar",
        "hello world",
        "A man a plan a canal Panama",
        "test",
        "python"
    ]
    
    for s in test_strings:
        try:
            requests.post(f"{BASE_URL}/strings", json={"value": s})
        except:
            pass
    
    # Test palindrome filter
    response = requests.get(f"{BASE_URL}/strings?is_palindrome=true")
    print(f"Palindromes Status: {response.status_code}")
    print(f"Count: {response.json()['count']}")
    
    # Test length filter
    response = requests.get(f"{BASE_URL}/strings?min_length=10")
    print(f"\nMin length 10 Status: {response.status_code}")
    print(f"Count: {response.json()['count']}")
    
    # Test word count filter
    response = requests.get(f"{BASE_URL}/strings?word_count=2")
    print(f"\nWord count 2 Status: {response.status_code}")
    print(f"Count: {response.json()['count']}")
    
    # Test contains character
    response = requests.get(f"{BASE_URL}/strings?contains_character=a")
    print(f"\nContains 'a' Status: {response.status_code}")
    print(f"Count: {response.json()['count']}")

def test_natural_language():
    print("\n=== Testing GET /strings/filter-by-natural-language ===")
    
    # Test single word palindromes
    response = requests.get(
        f"{BASE_URL}/strings/filter-by-natural-language",
        params={"query": "all single word palindromic strings"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test longer than query
    response = requests.get(
        f"{BASE_URL}/strings/filter-by-natural-language",
        params={"query": "strings longer than 10 characters"}
    )
    print(f"\nLonger than 10 Status: {response.status_code}")
    print(f"Count: {response.json()['count']}")
    
    # Test contains letter
    response = requests.get(
        f"{BASE_URL}/strings/filter-by-natural-language",
        params={"query": "strings containing the letter z"}
    )
    print(f"\nContains 'z' Status: {response.status_code}")
    print(f"Count: {response.json()['count']}")

def test_delete_string():
    print("\n=== Testing DELETE /strings/{string_value} ===")
    
    # Create a string
    requests.post(f"{BASE_URL}/strings", json={"value": "delete me"})
    
    # Delete it
    response = requests.delete(f"{BASE_URL}/strings/delete me")
    print(f"Status: {response.status_code}")
    print(f"Response: Empty (204)")
    
    # Try to delete again (should get 404)
    response = requests.delete(f"{BASE_URL}/strings/delete me")
    print(f"\nAlready deleted Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("Starting API Tests...")
    print("Make sure the API server is running on http://localhost:5000")
    
    try:
        test_create_string()
        test_get_string()
        test_get_all_with_filters()
        test_natural_language()
        test_delete_string()
        
        print("\n=== All tests completed! ===")
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API. Make sure it's running!")
    except Exception as e:
        print(f"\nError during testing: {e}")