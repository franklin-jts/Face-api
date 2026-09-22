# Error Handling & Validation Testing

## ✅ What's Been Implemented

### 1. Frontend Validation (Test Console)
- ✅ Checks if reference image is uploaded before allowing comparison
- ✅ Checks if live image is selected before allowing comparison
- ✅ Shows user-friendly alert with clear instructions
- ✅ Prevents API call if validation fails

### 2. Backend Validation (API)
- ✅ Validates file1 (reference) is provided
- ✅ Validates file2 (live capture) is provided
- ✅ Returns clear error messages explaining what's missing
- ✅ Suggests action to fix (e.g., "upload reference image first")

### 3. Error Messages
- ✅ Clear, user-friendly
- ✅ Actionable (tells user what to do)
- ✅ Not technical jargon
- ✅ Prevents confusion

---

## 🎯 Test Scenarios

### Scenario 1: No Reference, With Live Image
```
USER ACTION:
- Skips STEP 1 (no reference upload)
- Completes STEP 2 (captures live image)
- Clicks "Compare Faces"

EXPECTED:
Alert Message: "STEP 1 Required: Please upload & store reference image first!"

RESULT: ✅ PASS - User knows to upload reference first
```

### Scenario 2: With Reference, No Live Image
```
USER ACTION:
- Completes STEP 1 (uploads reference)
- Skips STEP 2 (no live capture)
- Clicks "Compare Faces"

EXPECTED:
Alert Message: "STEP 2 Required: Please capture or select a live image!"

RESULT: ✅ PASS - User knows to capture live image
```

### Scenario 3: With Both Reference and Live Image
```
USER ACTION:
- Completes STEP 1 (uploads reference)
- Completes STEP 2 (captures live image)
- Clicks "Compare Faces"

EXPECTED:
JSON Response with face_match: true/false and match_score

RESULT: ✅ PASS - Comparison works normally
```

### Scenario 4: API Direct Call - Missing file1
```
API REQUEST:
POST /employeeFaceCompare
Body: { "file2": <image>, "threshold": 70 }
(No file1 parameter)

EXPECTED RESPONSE:
{
  "status_code": 400,
  "detail": "❌ Reference image not provided. Please upload reference image first using 'Store Reference' button."
}

RESULT: ✅ PASS - Clear error message
```

### Scenario 5: API Direct Call - Missing file2
```
API REQUEST:
POST /employeeFaceCompare
Body: { "file1": <image>, "threshold": 70 }
(No file2 parameter)

EXPECTED RESPONSE:
{
  "status_code": 400,
  "detail": "❌ Live capture image not provided. Please capture image from camera using 'Use Camera' button."
}

RESULT: ✅ PASS - Clear error message
```

---

## 📋 Full Test Plan

### Test 1: Try to Compare Without Anything
1. Open test console
2. Click "Compare Faces" immediately
3. **Expected:** Alert: "STEP 1 Required"
4. **Result:** ✅ PASS or ❌ FAIL

### Test 2: Upload Reference, Try to Compare Without Capture
1. Upload & store reference image
2. Skip live capture
3. Click "Compare Faces"
4. **Expected:** Alert: "STEP 2 Required"
5. **Result:** ✅ PASS or ❌ FAIL

### Test 3: Capture Without Reference, Try to Compare
1. Skip reference upload
2. Capture live image
3. Click "Compare Faces"
4. **Expected:** Alert: "STEP 1 Required"
5. **Result:** ✅ PASS or ❌ FAIL

### Test 4: Complete Both Steps
1. Upload reference
2. Capture live image
3. Click "Compare Faces"
4. **Expected:** JSON response with match_score
5. **Result:** ✅ PASS or ❌ FAIL

### Test 5: Check API Error Directly
Use curl or Postman:
```bash
curl -X POST http://localhost:8001/employeeFaceCompare \
  -H "Authorization: Bearer secret-token-123" \
  -F "file2=@capture.jpg"

# No file1 provided
```
**Expected:** 400 error with message about missing reference

---

## ✅ Success Criteria

System is working correctly when:

- [ ] Test 1: Alert shown before API call
- [ ] Test 2: Alert shown with clear instructions
- [ ] Test 3: Alert shown directing to STEP 1
- [ ] Test 4: Comparison works normally
- [ ] Test 5: API returns clear error message
- [ ] No confusing technical errors
- [ ] User knows exactly what to do next

---

## 🎬 Run This Test Now

1. Open: **http://localhost:8001/test_console_v2.html**
2. Try each scenario above
3. Verify alerts/errors match expected
4. Check that all validation works

**Once all tests pass: ✅ Error handling is complete!**
