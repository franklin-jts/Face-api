# Test: Liveness Check Requires Reference Image

## 🎯 Test Objective
Verify that `/faceLiveness` endpoint now FAILS if reference image is not uploaded.

---

## 📋 Test Case 1: Liveness WITHOUT Reference (Should FAIL)

### Prerequisites:
- [ ] Server running on port 8001
- [ ] Test console accessible
- [ ] NO reference image uploaded

### Test Steps:

1. **Open Test Console:**
   - URL: `http://localhost:8001/test_console_v2.html`
   - Auth Token: `secret-token-123`

2. **Verify NO Reference Image:**
   - Don't click "Upload File" in STEP 1
   - Reference should be: NOT stored

3. **Scroll to "STEP 2A: Test Liveness Check":**
   - This is the liveness test section

4. **Capture Live Image:**
   - Click "Use Camera"
   - Capture from camera (your face)
   - Wait for preview

5. **Click "Check Liveness":**
   - Button at bottom of liveness section
   - Wait for response

### Expected Result:
```json
{
  "status": false,
  "message": "Liveness check failed: Reference image required",
  "data": {
    "liveness_passed": false,
    "liveness_score": 0.0,
    "liveness_reason": "reference_image_required",
    "spoof_detected": false,
    "face_detected": true,
    "faces_count": 1,
    "glasses_validation_reason": "reference_image_not_available"
  }
}
```

### Validation Points:
- [ ] `status: false` (failed)
- [ ] `liveness_passed: false`
- [ ] `liveness_reason: "reference_image_required"`
- [ ] HTTP Status: 400 (Bad Request)
- [ ] Error message is clear

### Actual Result:
```
Status: _____
Message: _____
Liveness Passed: _____ (should be false)
Reason: _____ (should be reference_image_required)
```

### Result: ✅ PASS or ❌ FAIL
```
Expected: ❌ FAIL (status false, reason reference_image_required)
Actual: _____ (PASS/FAIL)
```

---

## 📋 Test Case 2: Liveness WITH Reference (Should PASS)

### Prerequisites:
- [ ] Server running
- [ ] Test console accessible
- [ ] Reference image will be uploaded

### Test Steps:

1. **Open Test Console:**
   - URL: `http://localhost:8001/test_console_v2.html`

2. **Upload Reference Image (STEP 1):**
   - Click "📎 Upload File" in STEP 1
   - Select your face photo
   - Click "💾 Upload & Store Reference"
   - Wait for response: ✅ "Reference Stored"

3. **Verify Reference Stored:**
   - Check `stored_images/` folder
   - Should see: `reference_20260921_*.png`

4. **Scroll to "STEP 2A: Test Liveness Check":**
   - Find liveness test section

5. **Capture Live Image:**
   - Click "Use Camera"
   - Capture from camera
   - Wait for preview

6. **Click "Check Liveness":**
   - Wait for response

### Expected Result:
```json
{
  "status": true,
  "message": "Liveness check passed",
  "data": {
    "liveness_passed": true,
    "liveness_score": 0.93,
    "liveness_reason": "liveness_passed",
    "spoof_detected": false,
    "face_detected": true,
    "faces_count": 1,
    "glasses_match": true,
    "reference_glasses": false,
    "live_glasses": false
  }
}
```

### Validation Points:
- [ ] `status: true` (passed)
- [ ] `liveness_passed: true`
- [ ] `liveness_score` > 0 (confidence score)
- [ ] `liveness_reason: "liveness_passed"`
- [ ] `glasses_match` included (true or false)
- [ ] HTTP Status: 200 (OK)

### Actual Result:
```
Status: _____
Message: _____
Liveness Passed: _____ (should be true)
Score: _____ (0-1)
Glasses Match: _____ (true/false)
```

### Result: ✅ PASS or ❌ FAIL
```
Expected: ✅ PASS (status true, liveness_passed true)
Actual: _____ (PASS/FAIL)
```

---

## 📊 Comparison Test Results

| Scenario | Reference | Capture | Expected | Actual | Pass/Fail |
|----------|-----------|---------|----------|--------|-----------|
| Test 1 | NO | YES | ❌ FAIL | _____ | [  ] |
| Test 2 | YES | YES | ✅ PASS | _____ | [  ] |

---

## 🔍 Detailed Validation

### If Test 1 Fails (But Shouldn't):

**Problem:** Liveness passing without reference
**Cause:** Reference image requirement not working
**Check:**
- [ ] `temp/reference.jpg` doesn't exist (good)
- [ ] API still checking for it
- [ ] Error response returned (yes/no)

**Solution:** Verify app_sface.py has the fix

### If Test 2 Fails:

**Problem:** Liveness failing even with reference
**Cause:** Reference file not saved or glasses mismatch
**Check:**
- [ ] `temp/reference.jpg` exists
- [ ] File has content (> 0 bytes)
- [ ] Glasses state matches (both with or both without)

**Solution:** 
- Upload reference again
- Ensure glasses match between reference and capture
- Check browser console for errors

---

## 🎯 Extended Testing

### Test 3: Glasses Mismatch (With Reference)

**Scenario:**
- Reference image: NO glasses
- Live capture: WITH glasses

**Expected:** 
```json
{
  "liveness_passed": false,
  "liveness_reason": "glasses_mismatch"
}
```

**Result:** _____ (PASS/FAIL)

---

### Test 4: Same Reference Twice

**Scenario:**
- Reference image: Your face, no glasses
- Live capture: Your face, no glasses (same photo or fresh capture)

**Expected:**
```json
{
  "liveness_passed": true,
  "glasses_match": true,
  "reference_glasses": false,
  "live_glasses": false
}
```

**Result:** _____ (PASS/FAIL)

---

## ✅ Overall Test Results

```
Test 1 - Liveness without reference:
[ ] PASS (correctly returned error)
[ ] FAIL (incorrectly passed)

Test 2 - Liveness with reference:
[ ] PASS (correctly passed)
[ ] FAIL (incorrectly returned error)

Test 3 - Glasses mismatch:
[ ] PASS (correctly detected mismatch)
[ ] FAIL (missed mismatch)

Test 4 - Same glasses state:
[ ] PASS (correctly passed)
[ ] FAIL (incorrect mismatch error)

OVERALL: _____ TESTS PASSED / 4
```

---

## 📝 Test Report

```
LIVENESS REFERENCE REQUIREMENT TEST
Date: 2026-09-21
Tester: _____

=== TEST 1: Without Reference ===
Status: _____ (PASS/FAIL)
Error Shown: YES / NO
Error Message: _____
Reason Code: _____ (should be reference_image_required)

=== TEST 2: With Reference ===
Status: _____ (PASS/FAIL)
Liveness Passed: YES / NO
Score: _____ (0-1 range)
Glasses Validated: YES / NO

=== TEST 3: Glasses Mismatch ===
Status: _____ (PASS/FAIL)
Error Shown: YES / NO
Reason: _____

=== TEST 4: Same Glasses ===
Status: _____ (PASS/FAIL)
Liveness Passed: YES / NO

=== CONCLUSION ===
[✓] ALL PASS - Reference requirement working correctly
[ ] FAIL - Issues found (see above)

Notes:
_____________________
_____________________
```

---

## 🎬 Run These Tests Now

1. **Test 1:** Try without reference → Should FAIL ❌
2. **Test 2:** Try with reference → Should PASS ✅
3. **Test 3:** Different glasses → Should FAIL ❌
4. **Test 4:** Same glasses → Should PASS ✅

**Report results!** 📊
