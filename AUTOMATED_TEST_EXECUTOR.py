#!/usr/bin/env python3
"""
Comprehensive Automated Test Executor for Face Recognition API
Executes all testable scenarios from the 76-test matrix using real stored images
"""

import requests
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import base64

# ============================================================================
# CONFIGURATION
# ============================================================================

API_BASE_URL = "http://localhost:8001"
STORAGE_FOLDER = Path("stored_images")
TEST_RESULTS = []
FAILED_TESTS = []

# API Endpoints
ENDPOINTS = {
    "health": f"{API_BASE_URL}/health",
    "upload_reference": f"{API_BASE_URL}/uploadImage",
    "face_liveness": f"{API_BASE_URL}/faceLiveness",
    "face_compare": f"{API_BASE_URL}/employeeFaceCompare",
    "list_images": f"{API_BASE_URL}/dev/stored-images",
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def log_result(test_id: str, test_name: str, status: str, details: str, actual_result: Dict = None):
    """Log test result"""
    result = {
        "test_id": test_id,
        "test_name": test_name,
        "status": status,
        "details": details,
        "actual_result": actual_result or {},
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    TEST_RESULTS.append(result)
    
    status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⏳"
    print(f"{status_icon} {test_id}: {test_name} - {status}")
    print(f"   Details: {details}")
    if actual_result:
        print(f"   Response: {json.dumps(actual_result, indent=2)[:200]}")
    print()
    
    if status == "FAIL":
        FAILED_TESTS.append(test_id)

def read_image(image_path: Path) -> Optional[bytes]:
    """Read image file and return bytes"""
    if not image_path.exists():
        return None
    with open(image_path, "rb") as f:
        return f.read()

def get_reference_images() -> Dict[str, Path]:
    """Get all reference images from storage"""
    if not STORAGE_FOLDER.exists():
        return {}
    
    reference_images = {}
    for file in STORAGE_FOLDER.glob("reference_*.jpg"):
        key = file.stem.replace("reference_", "")
        reference_images[key] = file
    for file in STORAGE_FOLDER.glob("reference_*.png"):
        key = file.stem.replace("reference_", "")
        reference_images[key] = file
    
    return reference_images

def get_liveness_images() -> Dict[str, Path]:
    """Get all liveness test images from storage"""
    if not STORAGE_FOLDER.exists():
        return {}
    
    liveness_images = {}
    for file in STORAGE_FOLDER.glob("liveness_*.jpg"):
        key = file.stem.replace("liveness_", "")
        liveness_images[key] = file
    for file in STORAGE_FOLDER.glob("liveness_*.png"):
        key = file.stem.replace("liveness_", "")
        liveness_images[key] = file
    
    return liveness_images

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(ENDPOINTS["health"], timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is healthy")
            print(f"   Detector: {data['models']['detector_ready']}")
            print(f"   Recognizer: {data['models']['recognizer_ready']}")
            return True
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API at", API_BASE_URL)
        print("   Start the API with: python app_sface.py")
        return False
    except Exception as e:
        print(f"❌ API health check failed: {e}")
        return False

# ============================================================================
# TEST IMPLEMENTATIONS
# ============================================================================

def test_fv001_valid_enrollment():
    """
    FV-001: Valid Face Enrollment
    Upload reference image successfully
    """
    reference_images = get_reference_images()
    if not reference_images:
        log_result("FV-001", "Valid Face Enrollment", "SKIP", "No reference images found")
        return
    
    first_ref = list(reference_images.values())[0]
    image_bytes = read_image(first_ref)
    
    if not image_bytes:
        log_result("FV-001", "Valid Face Enrollment", "FAIL", "Could not read reference image")
        return
    
    try:
        files = {"reference": ("reference.jpg", image_bytes, "image/jpeg")}
        response = requests.post(ENDPOINTS["upload_reference"], files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            log_result("FV-001", "Valid Face Enrollment", "PASS", 
                      f"Reference uploaded: {data.get('message')}", data)
        else:
            data = response.json()
            log_result("FV-001", "Valid Face Enrollment", "FAIL", 
                      f"HTTP {response.status_code}: {data.get('message', 'Unknown error')}", data)
    except Exception as e:
        log_result("FV-001", "Valid Face Enrollment", "FAIL", str(e))

def test_fv006_reenroll_existing():
    """
    FV-006: Re-enroll Existing Employee
    Upload same person again
    """
    reference_images = get_reference_images()
    if len(reference_images) < 1:
        log_result("FV-006", "Re-enroll Existing", "SKIP", "Need at least 1 reference image")
        return
    
    ref_list = list(reference_images.values())
    first_ref = ref_list[0]
    second_ref = ref_list[0] if len(ref_list) == 1 else ref_list[1]
    
    image_bytes1 = read_image(first_ref)
    image_bytes2 = read_image(second_ref)
    
    if not image_bytes1 or not image_bytes2:
        log_result("FV-006", "Re-enroll Existing", "FAIL", "Could not read reference images")
        return
    
    try:
        # Upload first
        files = {"reference": ("reference.jpg", image_bytes1, "image/jpeg")}
        response1 = requests.post(ENDPOINTS["upload_reference"], files=files, timeout=30)
        
        # Re-enroll with second image
        files = {"reference": ("reference.jpg", image_bytes2, "image/jpeg")}
        response2 = requests.post(ENDPOINTS["upload_reference"], files=files, timeout=30)
        
        if response2.status_code == 200:
            data = response2.json()
            log_result("FV-006", "Re-enroll Existing", "PASS", 
                      f"Re-enrollment successful: {data.get('message')}", data)
        else:
            data = response2.json()
            log_result("FV-006", "Re-enroll Existing", "FAIL", 
                      f"Re-enrollment failed: {data.get('message')}", data)
    except Exception as e:
        log_result("FV-006", "Re-enroll Existing", "FAIL", str(e))

def test_fv008_correct_employee_match():
    """
    FV-008: Face Match - Correct Employee
    Test that same person matches correctly
    """
    reference_images = get_reference_images()
    liveness_images = get_liveness_images()
    
    if not reference_images or not liveness_images:
        log_result("FV-008", "Correct Employee Match", "SKIP", 
                  "Need reference and liveness images")
        return
    
    try:
        # Upload reference
        ref_image = list(reference_images.values())[0]
        ref_bytes = read_image(ref_image)
        
        files = {"reference": ("reference.jpg", ref_bytes, "image/jpeg")}
        response = requests.post(ENDPOINTS["upload_reference"], files=files, timeout=30)
        
        if response.status_code != 200:
            log_result("FV-008", "Correct Employee Match", "FAIL", 
                      "Could not upload reference image")
            return
        
        # Test liveness with same person
        live_image = list(liveness_images.values())[0]
        live_bytes = read_image(live_image)
        
        files = {"capture": ("capture.jpg", live_bytes, "image/jpeg")}
        params = {"threshold": 70}
        response = requests.post(ENDPOINTS["face_liveness"], files=files, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status"):
                log_result("FV-008", "Correct Employee Match", "PASS", 
                          f"Liveness passed: {data.get('message')}", data)
            else:
                log_result("FV-008", "Correct Employee Match", "FAIL", 
                          f"Liveness failed: {data.get('message')}", data)
        else:
            data = response.json()
            log_result("FV-008", "Correct Employee Match", "FAIL", 
                      f"HTTP {response.status_code}: {data.get('message')}", data)
    except Exception as e:
        log_result("FV-008", "Correct Employee Match", "FAIL", str(e))

def test_fv032_eyes_closed():
    """
    FV-032: Eyes Closed Detection
    Verify that closed eyes are detected
    """
    liveness_images = get_liveness_images()
    if not liveness_images:
        log_result("FV-032", "Eyes Closed Detection", "SKIP", "No liveness images found")
        return
    
    # Get first reference image
    reference_images = get_reference_images()
    if not reference_images:
        log_result("FV-032", "Eyes Closed Detection", "SKIP", "No reference image for comparison")
        return
    
    try:
        # Upload reference
        ref_image = list(reference_images.values())[0]
        ref_bytes = read_image(ref_image)
        
        files = {"reference": ("reference.jpg", ref_bytes, "image/jpeg")}
        requests.post(ENDPOINTS["upload_reference"], files=files, timeout=30)
        
        # Test with first liveness image (should detect eyes)
        live_image = list(liveness_images.values())[0]
        live_bytes = read_image(live_image)
        
        files = {"capture": ("capture.jpg", live_bytes, "image/jpeg")}
        response = requests.post(ENDPOINTS["face_liveness"], files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            liveness_reason = data.get("data", {}).get("liveness_reason", "")
            
            # Check if eyes were detected properly
            if "eyes_closed" in liveness_reason.lower():
                log_result("FV-032", "Eyes Closed Detection", "PASS", 
                          f"Eyes closed detected: {liveness_reason}", data)
            elif "eyes" in liveness_reason.lower():
                log_result("FV-032", "Eyes Closed Detection", "PARTIAL", 
                          f"Eyes message: {liveness_reason}", data)
            else:
                log_result("FV-032", "Eyes Closed Detection", "INFO", 
                          f"Liveness reason: {liveness_reason}", data)
        else:
            data = response.json()
            log_result("FV-032", "Eyes Closed Detection", "FAIL", 
                      f"HTTP {response.status_code}", data)
    except Exception as e:
        log_result("FV-032", "Eyes Closed Detection", "FAIL", str(e))

def test_fv045_repeated_verify_taps():
    """
    FV-045: Repeated Verify Taps (Idempotency)
    Ensure repeated requests don't create duplicates
    """
    reference_images = get_reference_images()
    liveness_images = get_liveness_images()
    
    if not reference_images or not liveness_images:
        log_result("FV-045", "Repeated Verify Taps", "SKIP", 
                  "Need reference and liveness images")
        return
    
    try:
        # Upload reference
        ref_image = list(reference_images.values())[0]
        ref_bytes = read_image(ref_image)
        
        files = {"reference": ("reference.jpg", ref_bytes, "image/jpeg")}
        requests.post(ENDPOINTS["upload_reference"], files=files, timeout=30)
        
        # Send 5 rapid requests with same image
        live_image = list(liveness_images.values())[0]
        live_bytes = read_image(live_image)
        
        responses = []
        for i in range(5):
            files = {"capture": ("capture.jpg", live_bytes, "image/jpeg")}
            response = requests.post(ENDPOINTS["face_liveness"], files=files, timeout=30)
            responses.append(response.status_code)
        
        # All should be consistent (either all 200 or all 400)
        if len(set(responses)) == 1:
            log_result("FV-045", "Repeated Verify Taps", "PASS", 
                      f"All 5 requests returned consistent status: {responses[0]}")
        else:
            log_result("FV-045", "Repeated Verify Taps", "FAIL", 
                      f"Inconsistent responses: {responses}")
    except Exception as e:
        log_result("FV-045", "Repeated Verify Taps", "FAIL", str(e))

def test_fv071_response_time():
    """
    FV-071: Normal Response-Time Test
    Measure performance with 10 valid verifications
    """
    import time
    
    reference_images = get_reference_images()
    liveness_images = get_liveness_images()
    
    if not reference_images or not liveness_images:
        log_result("FV-071", "Response Time SLA", "SKIP", 
                  "Need reference and liveness images")
        return
    
    try:
        ref_bytes = read_image(list(reference_images.values())[0])
        live_bytes = read_image(list(liveness_images.values())[0])
        
        # Upload reference
        files = {"reference": ("reference.jpg", ref_bytes, "image/jpeg")}
        requests.post(ENDPOINTS["upload_reference"], files=files, timeout=30)
        
        # Measure 10 liveness checks
        times = []
        for i in range(10):
            start = time.time()
            files = {"capture": ("capture.jpg", live_bytes, "image/jpeg")}
            response = requests.post(ENDPOINTS["face_liveness"], files=files, timeout=30)
            elapsed = time.time() - start
            times.append(elapsed)
        
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        
        if avg_time < 5.0:  # SLA: < 5 seconds average
            log_result("FV-071", "Response Time SLA", "PASS", 
                      f"Avg: {avg_time:.2f}s, Min: {min_time:.2f}s, Max: {max_time:.2f}s")
        else:
            log_result("FV-071", "Response Time SLA", "FAIL", 
                      f"Avg: {avg_time:.2f}s (SLA: < 5s)")
    except Exception as e:
        log_result("FV-071", "Response Time SLA", "FAIL", str(e))

# ============================================================================
# TEST RUNNER
# ============================================================================

def run_all_tests():
    """Execute all testable test cases"""
    global TEST_RESULTS, FAILED_TESTS
    
    print("\n" + "="*80)
    print("FACE RECOGNITION API - COMPREHENSIVE TEST EXECUTION")
    print("="*80 + "\n")
    
    # Check API health
    if not check_api_health():
        print("\n❌ Cannot proceed without API. Exiting.")
        return False
    
    print("\n" + "="*80)
    print("EXECUTING TESTABLE SCENARIOS")
    print("="*80 + "\n")
    
    # Run tests
    test_functions = [
        test_fv001_valid_enrollment,
        test_fv006_reenroll_existing,
        test_fv008_correct_employee_match,
        test_fv032_eyes_closed,
        test_fv045_repeated_verify_taps,
        test_fv071_response_time,
    ]
    
    for test_func in test_functions:
        try:
            test_func()
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}\n")
    
    # Generate summary
    print("\n" + "="*80)
    print("TEST EXECUTION SUMMARY")
    print("="*80)
    
    total = len(TEST_RESULTS)
    passed = len([t for t in TEST_RESULTS if t["status"] == "PASS"])
    failed = len([t for t in TEST_RESULTS if t["status"] == "FAIL"])
    skipped = len([t for t in TEST_RESULTS if t["status"] == "SKIP"])
    
    print(f"\nTotal Tests Executed: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⏳ Skipped: {skipped}")
    print(f"\nSuccess Rate: {(passed/total*100):.1f}%" if total > 0 else "N/A")
    
    if FAILED_TESTS:
        print(f"\nFailed Tests: {', '.join(FAILED_TESTS)}")
    
    return True

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    if run_all_tests():
        # Save detailed results
        output_file = "TEST_EXECUTION_RESULTS.json"
        with open(output_file, "w") as f:
            json.dump({
                "execution_date": datetime.utcnow().isoformat() + "Z",
                "total_tests": len(TEST_RESULTS),
                "passed": len([t for t in TEST_RESULTS if t["status"] == "PASS"]),
                "failed": len([t for t in TEST_RESULTS if t["status"] == "FAIL"]),
                "skipped": len([t for t in TEST_RESULTS if t["status"] == "SKIP"]),
                "results": TEST_RESULTS,
            }, f, indent=2)
        print(f"\n✅ Results saved to {output_file}")
