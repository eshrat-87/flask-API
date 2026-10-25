#!/usr/bin/env python3
"""
Test script for Task 3: Authentication & Authorization
"""

import requests
import json
from requests.auth import HTTPBasicAuth

API_URL = "http://localhost:5002"

# Demo credentials
EMPLOYEE_USERNAME = "employee"
EMPLOYEE_PASSWORD = "password123"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
INVALID_USERNAME = "wronguser"
INVALID_PASSWORD = "wrongpass"

def test_login(username, password, test_num):
    """Test login endpoint."""
    
    print(f"\nTest {test_num}: Testing login for {username}...")
    
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(f"{API_URL}/login", json=data)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success - Role: {result['role']}")
            return True, result.get('role')
        elif response.status_code == 401:
            print(f"   ❌ Unauthorized - {response.json().get('error')}")
            return False, None
        else:
            print(f"   ❌ Unexpected response: {response.json()}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to Flask API at {API_URL}")
        return False, None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

def test_employee_access(username, password, auth_type="basic", test_num=""):
    """Test employee access (should only view)."""
    
    print(f"\nTest {test_num}: Testing employee access...")
    
    try:
        # First, get all employees
        if auth_type == "basic":
            response = requests.get(f"{API_URL}/employees", 
                                  auth=HTTPBasicAuth(username, password))
        elif auth_type == "login":
            # Login first, then get employees
            login_data = {"username": username, "password": password}
            login_response = requests.post(f"{API_URL}/login", json=login_data)
            if login_response.status_code != 200:
                print(f"   ❌ Login failed")
                return False
            
            # For this example, we'll use Basic Auth for the actual request
            response = requests.get(f"{API_URL}/employees", 
                                  auth=HTTPBasicAuth(username, password))
        
        print(f"   GET /employees - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Can view {len(data['employees'])} employees")
            
            # Try to delete (should fail)
            delete_response = requests.delete(f"{API_URL}/employees/1", 
                                            auth=HTTPBasicAuth(username, password))
            print(f"   DELETE /employees/1 - Status: {delete_response.status_code}")
            
            if delete_response.status_code == 403:
                print(f"   ✅ Employee cannot delete (as expected)")
                return True
            else:
                print(f"   ❌ Unexpected - Employee could delete")
                return False
        elif response.status_code == 401:
            print(f"   ❌ Unauthorized")
            return False
        else:
            print(f"   ❌ Unexpected response: {response.json()}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to Flask API")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_admin_access(username, password, test_num=""):
    """Test admin access (should do everything)."""
    
    print(f"\nTest {test_num}: Testing admin access...")
    
    try:
        # 1. Get all employees
        response = requests.get(f"{API_URL}/employees", 
                              auth=HTTPBasicAuth(username, password))
        print(f"   GET /employees - Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Cannot view employees")
            return False
        
        data = response.json()
        initial_count = len(data['employees'])
        print(f"   ✅ Can view {initial_count} employees")
        
        # 2. Add a new employee
        new_employee = {
            "name": "Test Employee",
            "position": "Tester"
        }
        post_response = requests.post(f"{API_URL}/employees", 
                                    auth=HTTPBasicAuth(username, password),
                                    json=new_employee)
        print(f"   POST /employees - Status: {post_response.status_code}")
        
        if post_response.status_code != 201:
            print(f"   ❌ Cannot add employee")
            return False
        
        new_employee_id = post_response.json()['id']
        print(f"   ✅ Added employee ID: {new_employee_id}")
        
        # 3. Update the new employee
        update_data = {
            "position": "Senior Tester"
        }
        update_response = requests.put(f"{API_URL}/employees/{new_employee_id}", 
                                     auth=HTTPBasicAuth(username, password),
                                     json=update_data)
        print(f"   PUT /employees/{new_employee_id} - Status: {update_response.status_code}")
        
        if update_response.status_code != 200:
            print(f"   ❌ Cannot update employee")
            return False
        
        print(f"   ✅ Updated employee")
        
        # 4. Delete the new employee
        delete_response = requests.delete(f"{API_URL}/employees/{new_employee_id}", 
                                        auth=HTTPBasicAuth(username, password))
        print(f"   DELETE /employees/{new_employee_id} - Status: {delete_response.status_code}")
        
        if delete_response.status_code != 200:
            print(f"   ❌ Cannot delete employee")
            return False
        
        print(f"   ✅ Deleted employee")
        
        return True
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to Flask API")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_missing_credentials(test_num=""):
    """Test without credentials."""
    
    print(f"\nTest {test_num}: Testing without credentials...")
    
    try:
        response = requests.get(f"{API_URL}/employees")
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Expected - Missing credentials should return 401")
            return True
        else:
            print(f"   ❌ Unexpected response")
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
    print("Testing Task 3: Authentication & Authorization")
    print("=" * 60)
    print(f"\nDemo Users:")
    print(f"  Employee: username='{EMPLOYEE_USERNAME}', password='{EMPLOYEE_PASSWORD}'")
    print(f"  Admin:    username='{ADMIN_USERNAME}', password='{ADMIN_PASSWORD}'")
    print("=" * 60)
    
    results = []
    
    # Test 1: Login with valid employee
    success, role = test_login(EMPLOYEE_USERNAME, EMPLOYEE_PASSWORD, 1)
    results.append(success)
    
    # Test 2: Login with valid admin
    success, role = test_login(ADMIN_USERNAME, ADMIN_PASSWORD, 2)
    results.append(success)
    
    # Test 3: Login with invalid credentials
    success, role = test_login(INVALID_USERNAME, INVALID_PASSWORD, 3)
    results.append(not success)  # Should fail
    
    # Test 4: Employee role - view only (Basic Auth)
    success = test_employee_access(EMPLOYEE_USERNAME, EMPLOYEE_PASSWORD, "basic", 4)
    results.append(success)
    
    # Test 5: Admin role - full access (Basic Auth)
    success = test_admin_access(ADMIN_USERNAME, ADMIN_PASSWORD, 5)
    results.append(success)
    
    # Test 6: Missing credentials
    success = test_missing_credentials(6)
    results.append(success)
    
    # Test 7: Employee trying to delete (should fail)
    try:
        print(f"\nTest 7: Employee trying to delete employee...")
        response = requests.delete(f"{API_URL}/employees/2", 
                                 auth=HTTPBasicAuth(EMPLOYEE_USERNAME, EMPLOYEE_PASSWORD))
        print(f"   DELETE /employees/2 - Status: {response.status_code}")
        
        if response.status_code == 403:
            print(f"   ✅ Employee cannot delete (403 Forbidden)")
            results.append(True)
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            results.append(False)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results.append(False)
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r)
    total_tests = len(results)
    
    print(f"Passed: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("✅ All tests passed! Role-based access control is working correctly.")
    else:
        print(f"⚠️  {total_tests - success_count} tests failed")
    
    print("=" * 60)
    print("\nRole-based Access Matrix:")
    print("=" * 60)
    print("| Action           | Employee | Administrator |")
    print("|------------------|----------|---------------|")
    print("| View employees   |    ✅    |      ✅       |")
    print("| Add employee     |    ❌    |      ✅       |")
    print("| Update employee  |    ❌    |      ✅       |")
    print("| Delete employee  |    ❌    |      ✅       |")
    print("=" * 60)

if __name__ == "__main__":
    main()