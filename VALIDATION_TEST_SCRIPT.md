# Face Comparison Validation Test Script

## 🎯 Test Objective
Verify that Face Comparison (`/employeeFaceCompare`) properly validates:
1. ✅ Reference image is uploaded before comparison
2. ✅ Live capture image is selected before comparison
3. ✅ Both images are required for comparison to work
4. ✅ Clear error messages guide user to fix issues

---

## 📋 TEST 1: Compare Without Reference Upload

### Steps:
1. Open: `http://localhost:8001/test_console_v2.html`
2. **DO NOT upload reference image** (skip STEP 1)
3. Scroll to **"STEP 2B: Test Face Comparison"**
4. **DO upload/capture a live image** (complete STEP 2)
5. Click **"🔍 Compare Faces"** button

### Expected Behavior:
**Browser Alert Appears:**
```
❌ STEP 1 Required: Please upload & store reference image first!

1. Click "Choose File"
2. Select your photo
3. Click "💾 Upload & Store Reference"
```

### Validation Points:
- [ ] Alert appears (not API error, but frontend validation)
- [ ] Alert message is clear and actionable
- [ ] Message tells user exactly what STEP to do (STEP 1)
- [ ] Message provides step-by-step instructions
- [ ] NO API call is made (check browser Network tab - no POST to /employeeFaceCompare)

### Result: ✅ PASS or ❌ FAIL
```
Expected: PASS - Alert should show before API call
Actual: _____ (record result)
```

---

## 📋 TEST 2: Upload Reference, Then Compare

### Steps:
1. Still in same page
2. Click **"📎 Upload File"** in STEP 1
3. Select your face photo
4. Click **"💾 Upload & Store Reference"**
5. See response: ✅ "Reference Stored"
6. Scroll to STEP 2B
7. Click **"📷 Use Camera"**
8. Capture from camera
9. Click **"🔍 Compare Faces"**

### Expected Behavior:
**JSON Response with Comparison Result:**
```json
{
  "status": true,
  "message": "Faces match",
  "data": {
    "face_match": true,
    "match_score": 87.5,
    "liveness_passed": true,
    "challenge_passed": true
  }
}
```

### Validation Points:
- [ ] Comparison works (API call succeeds)
- [ ] Response includes `face_match` field
- [ ] Response includes `match_score` (0-100%)
- [ ] Response includes `liveness_passed` field
- [ ] No error messages
- [ ] Both images were processed

### Result: ✅ PASS or ❌ FAIL
```
Expected: PASS - Comparison should work with both images
Actual: _____ (record result)
Match Score: _____ (record value)
```

---

## 📋 TEST 3: Compare Without Live Image

### Steps:
1. Refresh page or open fresh console
2. Click **"📎 Upload File"** in STEP 1
3. Upload reference image
4. Click **"💾 Upload & Store Reference"**
5. **DO NOT capture live image** (skip STEP 2)
6. Scroll to STEP 2B
7. Click **"🔍 Compare Faces"** button

### Expected Behavior:
**Browser Alert Appears:**
```
❌ STEP 2 Required: Please capture or select a live image!

1. Click "Use Camera"
2. Capture your face
3. Or click "Upload File"
```

### Validation Points:
- [ ] Alert appears (frontend validation, not API error)
- [ ] Alert message is clear
- [ ] Message directs to STEP 2
- [ ] Message provides clear instructions
- [ ] NO API call is made

### Result: ✅ PASS or ❌ FAIL
```
Expected: PASS - Alert should show before API call
Actual: _____ (record result)
```

---

## 📋 TEST 4: API Direct Call - Missing file1

### Steps:
Use curl or Postman to test API directly

**Command:**
```bash
curl -X POST http://localhost:8001/employeeFaceCompare \
  -H "Authorization: Bearer secret-token-123" \
  -F "file2=@/path/to/image.jpg"

# Note: NO file1 parameter (reference image missing)
```

### Expected Response:
```json
{
  "detail": "❌ Reference image not provided. Please upload reference image first using 'Store Reference' button."
}
```

**Status Code:** `400`

### Validation Points:
- [ ] API returns 400 (Bad Request)
- [ ] Error message is clear
- [ ] Error message explains what's missing (file1)
- [ ] Error message suggests how to fix (use Store Reference)
- [ ] Not a 500 error (server error)
- [ ] Error message is user-friendly (not technical jargon)

### Result: ✅ PASS or ❌ FAIL
```
Expected: PASS - 400 error with clear message
Status Code: _____ 
Message: _____
```

---

## 📋 TEST 5: API Direct Call - Missing file2

### Steps:
Use curl or Postman to test API directly

**Command:**
```bash
curl -X POST http://localhost:8001/employeeFaceCompare \
  -H "Authorization: Bearer secret-token-123" \
  -F "file1=@/path/to/reference.jpg"

# Note: NO file2 parameter (live image missing)
```

### Expected Response:
```json
{
  "detail": "❌ Live capture image not provided. Please capture image from camera using 'Use Camera' button."
}
```

**Status Code:** `400`

### Validation Points:
- [ ] API returns 400 (Bad Request)
- [ ] Error message is clear
- [ ] Error message explains what's missing (file2)
- [ ] Error message suggests how to fix (use camera)
- [ ] Not a 500 error
- [ ] Error message is user-friendly

### Result: ✅ PASS or ❌ FAIL
```
Expected: PASS - 400 error with clear message
Status Code: _____
Message: _____
```

---

## ✅ Test Validation Checklist

### Frontend Validation (Test Console):
- [ ] Test 1: Alert shown when reference missing
- [ ] Test 1: Alert provides clear instructions
- [ ] Test 1: No API call made (check Network tab)
- [ ] Test 2: Comparison works when both images present
- [ ] Test 2: Match score returned (0-100%)
- [ ] Test 3: Alert shown when live image missing
- [ ] Test 3: Alert provides clear instructions
- [ ] Test 3: No API call made

### Backend Validation (API):
- [ ] Test 4: 400 error for missing file1
- [ ] Test 4: Error message mentions "Reference image"
- [ ] Test 4: Error message suggests "Store Reference"
- [ ] Test 5: 400 error for missing file2
- [ ] Test 5: Error message mentions "Live capture"
- [ ] Test 5: Error message suggests "Use Camera"

### User Experience:
- [ ] All error messages are clear
- [ ] All error messages are actionable
- [ ] User knows exactly what to do next
- [ ] No technical jargon or confusing errors
- [ ] System guides user through workflow

---

## 📊 Overall Test Results Summary

```
TOTAL TESTS: 5
PASSED: _____ / 5
FAILED: _____ / 5

TEST 1 (No Reference): _____ PASS/FAIL
TEST 2 (Both Images): _____ PASS/FAIL
TEST 3 (No Live Image): _____ PASS/FAIL
TEST 4 (API No file1): _____ PASS/FAIL
TEST 5 (API No file2): _____ PASS/FAIL

OVERALL RESULT: _____ PASS/FAIL

If all 5 tests PASS: ✅ Validation is working perfectly!
If any test FAILS: ❌ Need to debug and fix
```

---

## 🔍 Debug Tips

### If Test 1 Fails (Alert not showing):
- Check browser console (F12) for JavaScript errors
- Verify `storedRefFile` is initialized correctly
- Verify alert() function works
- Check if validation code is reached

### If Test 2 Fails (Comparison doesn't work):
- Check if reference was actually uploaded
- Verify file is in `stored_images/` folder
- Check server logs for errors
- Verify both images are valid

### If Test 3 Fails (Alert not showing):
- Check browser console for errors
- Verify `compareFile2` is null when expected
- Verify alert() function works

### If Test 4 Fails (API doesn't validate):
- Check server logs for error handling
- Verify API is checking for file1 parameter
- Verify error message format
- Test with Postman to ensure curl syntax is correct

### If Test 5 Fails (API doesn't validate):
- Check server logs
- Verify API is checking for file2 parameter
- Verify error message format
- Test with Postman

---

## 🎯 Manual Test Procedure

**Do this now:**

1. ✅ **Test 1:** Open console, skip reference, try compare → Should see alert
2. ✅ **Test 2:** Upload reference, capture, compare → Should show match score
3. ✅ **Test 3:** Upload reference, skip capture, try compare → Should see alert
4. ✅ **Test 4:** Use curl/Postman, no file1 → Should see 400 error
5. ✅ **Test 5:** Use curl/Postman, no file2 → Should see 400 error

**Report Results:**
- How many passed?
- Which ones failed?
- What error messages did you see?

---

## 📝 Test Report Template

```
FACE COMPARISON VALIDATION TEST
Date: 2026-09-21
Tester: [Your Name]

TEST RESULTS:
[ ] Test 1 - Alert without reference: PASS / FAIL
[ ] Test 2 - Compare with both images: PASS / FAIL  
[ ] Test 3 - Alert without live image: PASS / FAIL
[ ] Test 4 - API error missing file1: PASS / FAIL
[ ] Test 5 - API error missing file2: PASS / FAIL

TOTAL: _____ / 5 PASSED

NOTES:
- Error messages received: _____
- Any unexpected behavior: _____
- Recommendations: _____

CONCLUSION:
[ ] ✅ PASS - All validation working
[ ] ❌ FAIL - Some issues found (see notes)
```

---

## 🎬 Run This Test

Execute all 5 tests and report results!
