#!/usr/bin/env python3
"""
Test script for Task 1: Student Management System
"""

import requests
import json

API_URL = "http://localhost:5000"

def test_endpoints():
    """Test all Task 1 endpoints."""
    
    print("=" * 60)
    print("Testing Task 1: Student Management System")
    print("=" * 60)
    
    # Test 1: Get all students (initial)
    print("\n1. Getting all students...")
    response = requests.get(f"{API_URL}/students")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Students: {len(response.json())}")
        for student in response.json():
            print(f"     - {student['name']} ({student['email']})")
    
    # Test 2: Add a new student
    print("\n2. Adding a new student...")
    new_student = {
        "name": "Ali Khan",
        "department": "Computer Science",
        "email": "ali.khan@example.com"
    }
    response = requests.post(f"{API_URL}/students", json=new_student)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        student_id = response.json()['id']
        print(f"   New student ID: {student_id}")
    
    # Test 3: Get the new student
    print("\n3. Getting the new student...")
    response = requests.get(f"{API_URL}/students/{student_id}")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        student = response.json()
        print(f"   Student data: {student}")
    
    # Test 4: Update the student
    print("\n4. Updating the student...")
    update_data = {
        "department": "Software Engineering",
        "email": "ali.khan.updated@example.com"
    }
    response = requests.put(f"{API_URL}/students/{student_id}", json=update_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Message: {response.json()['message']}")
    
    # Test 5: Get all students again
    print("\n5. Getting all students again...")
    response = requests.get(f"{API_URL}/students")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Total students: {len(response.json())}")
    
    # Test 6: Delete the student
    print("\n6. Deleting the student...")
    response = requests.delete(f"{API_URL}/students/{student_id}")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Message: {response.json()['message']}")
    
    # Test 7: Try to get deleted student
    print("\n7. Trying to get deleted student...")
    response = requests.get(f"{API_URL}/students/{student_id}")
    print(f"   Status: {response.status_code}")
    if response.status_code == 404:
        print("   Student not found (as expected)")
    
    print("\n" + "=" * 60)
    print("Task 1 Testing Complete! ✓")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_endpoints()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Flask API at http://localhost:5000")
        print("Make sure Task 1 Flask app is running:")
        print("   cd Task1")
        print("   python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")