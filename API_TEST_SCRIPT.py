#!/usr/bin/env python3
"""
Automated API Testing Script for Face Recognition API
Tests all endpoints programmatically
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8001"
AUTH_TOKEN = "secret-token-123"
HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}

# Test results tracking
results = {
    "passed": [],
    "failed": [],
    "total": 0
}

def print_test(test_id, name, status, details=""):
    """Print test result"""
    symbol = "✅" if status == "PASS" else "❌"
    print(f"{symbol} {test_id}: {name} - {status}")
    if details:
        print(f"   {details}")

def test_health_check():
    """Test 1: Server health check"""
    try:
        response = requests.get(f"{BASE_URL}/")
        results["total"] += 1
        if response.status_code == 200:
            print_test("T-001", "Server Health Check", "PASS", f"Status: {response.status_code}")
            results["passed"].append("T-001")
            return True
        else:
            print_test("T-001", "Server Health Check", "FAIL", f"Status: {response.status_code}")
            results["failed"].append("T-001")
            return False
    except Exception as e:
        print_test("T-001", "Server Health Check", "FAIL", str(e))
        results["failed"].append("T-001")
        return False

def test_system_info():
    """Test 2: System info endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/dev/system-info", headers=HEADERS)
        results["total"] += 1
        if response.status_code == 200 and response.json().get("status"):
            data = response.json()
            print_test("T-002", "System Info", "PASS", f"API Version: {data.get('data', {}).get('api_version', 'N/A')}")
            results["passed"].append("T-002")
            return True
        else:
            print_test("T-002", "System Info", "FAIL", f"Status: {response.status_code}")
            results["failed"].append("T-002")
            return False
    except Exception as e:
        print_test("T-002", "System Info", "FAIL", str(e))
        results["failed"].append("T-002")
        return False

def test_no_reference_image():
    """Test 3: Liveness without reference image"""
    try:
        # Create dummy image (1x1 pixel)
        from PIL import Image
        import io
        
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        files = {"capture": ("test.jpg", img_bytes, "image/jpeg")}
        response = requests.post(f"{BASE_URL}/faceLiveness", headers=HEADERS, files=files)
        results["total"] += 1
        
        if response.status_code == 400:
            data = response.json()
            if "reference_image_required" in str(data):
                print_test("T-003", "Liveness Without Reference", "PASS", "Correctly rejected")
                results["passed"].append("T-003")
                return True
        
        print_test("T-003", "Liveness Without Reference", "FAIL", f"Status: {response.status_code}")
        results["failed"].append("T-003")
        return False
    except Exception as e:
        print_test("T-003", "Liveness Without Reference", "FAIL", str(e))
        results["failed"].append("T-003")
        return False

def test_invalid_auth_token():
    """Test 4: Invalid authentication token"""
    try:
        bad_headers = {"Authorization": "Bearer invalid-token"}
        response = requests.get(f"{BASE_URL}/dev/system-info", headers=bad_headers)
        results["total"] += 1
        
        if response.status_code == 403:
            print_test("T-004", "Invalid Auth Token", "PASS", "Correctly rejected")
            results["passed"].append("T-004")
            return True
        else:
            print_test("T-004", "Invalid Auth Token", "FAIL", f"Status: {response.status_code}")
            results["failed"].append("T-004")
            return False
    except Exception as e:
        print_test("T-004", "Invalid Auth Token", "FAIL", str(e))
        results["failed"].append("T-004")
        return False

def test_missing_auth_token():
    """Test 5: Missing authentication token"""
    try:
        response = requests.get(f"{BASE_URL}/dev/system-info")
        results["total"] += 1
        
        if response.status_code == 403:
            print_test("T-005", "Missing Auth Token", "PASS", "Correctly rejected")
            results["passed"].append("T-005")
            return True
        else:
            print_test("T-005", "Missing Auth Token", "FAIL", f"Status: {response.status_code}")
            results["failed"].append("T-005")
            return False
    except Exception as e:
        print_test("T-005", "Missing Auth Token", "FAIL", str(e))
        results["failed"].append("T-005")
        return False

def test_invalid_file_upload():
    """Test 6: Invalid file upload (not image)"""
    try:
        files = {"reference": ("test.txt", b"not an image", "text/plain")}
        response = requests.post(f"{BASE_URL}/uploadImage", headers=HEADERS, files=files)
        results["total"] += 1
        
        if response.status_code == 400:
            print_test("T-006", "Invalid File Upload", "PASS", "Correctly rejected")
            results["passed"].append("T-006")
            return True
        else:
            print_test("T-006", "Invalid File Upload", "FAIL", f"Status: {response.status_code}")
            results["failed"].append("T-006")
            return False
    except Exception as e:
        print_test("T-006", "Invalid File Upload", "FAIL", str(e))
        results["failed"].append("T-006")
        return False

def test_compare_without_files():
    """Test 7: Face comparison without files"""
    try:
        response = requests.post(f"{BASE_URL}/employeeFaceCompare", headers=HEADERS)
        results["total"] += 1
        
        if response.status_code == 400:
            print_test("T-007", "Compare Without Files", "PASS", "Correctly rejected")
            results["passed"].append("T-007")
            return True
        else:
            print_test("T-007", "Compare Without Files", "FAIL", f"Status: {response.status_code}")
            results["failed"].append("T-007")
            return False
    except Exception as e:
        print_test("T-007", "Compare Without Files", "FAIL", str(e))
        results["failed"].append("T-007")
        return False

def test_stored_images_list():
    """Test 8: List stored images"""
    try:
        response = requests.get(f"{BASE_URL}/dev/stored-images", headers=HEADERS)
        results["total"] += 1
        
        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                print_test("T-008", "List Stored Images", "PASS", f"Found images: {len(data.get('data', []))}")
                results["passed"].append("T-008")
                return True
        
        print_test("T-008", "List Stored Images", "FAIL", f"Status: {response.status_code}")
        results["failed"].append("T-008")
        return False
    except Exception as e:
        print_test("T-008", "List Stored Images", "FAIL", str(e))
        results["failed"].append("T-008")
        return False

def test_api_response_format():
    """Test 9: API response format"""
    try:
        response = requests.get(f"{BASE_URL}/dev/system-info", headers=HEADERS)
        results["total"] += 1
        
        if response.status_code == 200:
            data = response.json()
            required_fields = ["status", "message", "data"]
            if all(field in data for field in required_fields):
                print_test("T-009", "API Response Format", "PASS", "All required fields present")
                results["passed"].append("T-009")
                return True
        
        print_test("T-009", "API Response Format", "FAIL", "Missing required fields")
        results["failed"].append("T-009")
        return False
    except Exception as e:
        print_test("T-009", "API Response Format", "FAIL", str(e))
        results["failed"].append("T-009")
        return False

def test_timeout_handling():
    """Test 10: API timeout handling"""
    try:
        results["total"] += 1
        # This would require a timeout, skipping for now
        print_test("T-010", "Timeout Handling", "SKIP", "Manual test required")
        return True
    except Exception as e:
        print_test("T-010", "Timeout Handling", "FAIL", str(e))
        results["failed"].append("T-010")
        return False

def test_concurrent_requests():
    """Test 11: Concurrent requests"""
    try:
        import concurrent.futures
        results["total"] += 1
        
        def make_request():
            return requests.get(f"{BASE_URL}/dev/system-info", headers=HEADERS)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            responses = [f.result() for f in futures]
        
        if all(r.status_code == 200 for r in responses):
            print_test("T-011", "Concurrent Requests", "PASS", "All 5 requests succeeded")
            results["passed"].append("T-011")
            return True
        else:
            print_test("T-011", "Concurrent Requests", "FAIL", "Some requests failed")
            results["failed"].append("T-011")
            return False
    except Exception as e:
        print_test("T-011", "Concurrent Requests", "FAIL", str(e))
        results["failed"].append("T-011")
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("🧪 Face Recognition API - Automated Test Suite")
    print("=" * 70)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Base URL: {BASE_URL}")
    print("=" * 70)
    print()
    
    # Run tests
    test_health_check()
    test_system_info()
    test_no_reference_image()
    test_invalid_auth_token()
    test_missing_auth_token()
    test_invalid_file_upload()
    test_compare_without_files()
    test_stored_images_list()
    test_api_response_format()
    test_timeout_handling()
    test_concurrent_requests()
    
    # Print summary
    print()
    print("=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {len(results['passed'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"Pass Rate: {(len(results['passed']) / results['total'] * 100):.1f}%")
    print("=" * 70)
    
    if results['failed']:
        print("\nFailed Tests:")
        for test_id in results['failed']:
            print(f"  - {test_id}")
    
    print()
    print("=" * 70)
    if len(results['passed']) == results['total']:
        print("✅ ALL TESTS PASSED - API IS WORKING!")
    else:
        print("⚠️ SOME TESTS FAILED - CHECK RESULTS ABOVE")
    print("=" * 70)

if __name__ == "__main__":
    main()
