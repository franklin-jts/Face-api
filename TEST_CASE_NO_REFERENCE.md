# Test Case: Comparison Without Reference Image

## 🎯 What You're Testing

**Scenario:** User tries to compare faces without uploading reference image first
**Expected:** System rejects with clear error message
**Purpose:** Validate that comparison requires reference image

---

## 📋 Test Steps

### Test 1: Try to Compare Without Reference (Should Fail)

1. Open: **http://localhost:8001/test_console_v2.html**
2. Enter Auth Token: `secret-token-123`
3. **DO NOT upload reference image**
4. Scroll to **"STEP 2B: Face Comparison"**
5. Click **"Use Camera"** under "Live Capture (file2)"
6. Capture from camera (or upload any image)
7. Click **"🔍 Compare Faces"** button

**Expected Result - Alert Message:**
```
❌ STEP 1 Required: Please upload & store reference image first!

1. Click "Choose File"
2. Select your photo
3. Click "💾 Upload & Store Reference"
```

✅ **Test Passes** - User is instructed what to do

---

### Test 2: Compare Without Live Capture (Should Fail)

1. **Upload & Store Reference** (complete STEP 1)
2. **DO NOT capture live image** (skip STEP 2)
3. Click **"🔍 Compare Faces"** button

**Expected Result - Alert Message:**
```
❌ STEP 2 Required: Please capture or select a live image!

1. Click "Use Camera"
2. Capture your face
3. Or click "Upload File"
```

✅ **Test Passes** - User is instructed what to do

---

### Test 3: Compare With Both Images (Should Succeed)

1. **Upload & Store Reference** (complete STEP 1)
2. **Capture Live Image** (complete STEP 2)
3. Click **"🔍 Compare Faces"** button

**Expected Result - JSON Response:**
```json
{
  "status": true/false,
  "face_match": true/false,
  "match_score": 85.5,
  "liveness_passed": true
}
```

✅ **Test Passes** - Comparison performed successfully

---

## 🔧 Error Handling Validation

### Scenario 1: Missing Reference Image

**Test:** Try comparison without uploading reference

**Expected Error:**
```
Alert: "STEP 1 Required: Please upload & store reference image first!"
```

**Why:** Reference image is mandatory for face comparison

**Fix:** Upload reference image using "Store Reference" button

---

### Scenario 2: Missing Live Capture

**Test:** Try comparison without capturing live image

**Expected Error:**
```
Alert: "STEP 2 Required: Please capture or select a live image!"
```

**Why:** Live image is mandatory for face comparison

**Fix:** Capture from camera using "Use Camera" button

---

### Scenario 3: API Missing File1

**Test:** Send comparison request to API without file1 parameter

**Expected Error (from API):**
```json
{
  "detail": "❌ Reference image not provided. Please upload reference image first using 'Store Reference' button."
}
```

**Why:** /employeeFaceCompare endpoint requires file1

**Fix:** Upload reference image first

---

### Scenario 4: API Missing File2

**Test:** Send comparison request to API without file2 parameter

**Expected Error (from API):**
```json
{
  "detail": "❌ Live capture image not provided. Please capture image from camera using 'Use Camera' button."
}
```

**Why:** /employeeFaceCompare endpoint requires file2

**Fix:** Capture image from camera

---

## ✅ Validation Checklist

### Frontend Validation (Test Console):
- [ ] Alert shown if reference not uploaded
- [ ] Alert shown if live image not selected
- [ ] Clear instructions on how to fix
- [ ] No API call made if validation fails

### Backend Validation (API):
- [ ] 400 error if file1 missing
- [ ] 400 error if file2 missing
- [ ] Clear error message explaining what's required
- [ ] Error message suggests action to fix

### User Experience:
- [ ] User knows what to do
- [ ] Clear step-by-step instructions
- [ ] No confusing technical errors
- [ ] Guided toward correct workflow

---

## 📊 Test Results Template

```
TEST CASE: No Reference Image Upload

TEST 1 - Alert Without Reference:
Result: ✅ PASS
Message shown: "STEP 1 Required..."
User action clear: Yes

TEST 2 - Alert Without Live Image:
Result: ✅ PASS
Message shown: "STEP 2 Required..."
User action clear: Yes

TEST 3 - Successful Comparison:
Result: ✅ PASS
Response valid: Yes
Match score shown: Yes

OVERALL: ✅ ALL VALIDATION WORKING
```

---

## 🎯 Error Messages Reference

### Frontend Alerts (Test Console):

**Missing Reference:**
```
❌ STEP 1 Required: Please upload & store reference image first!

1. Click "Choose File"
2. Select your photo
3. Click "💾 Upload & Store Reference"
```

**Missing Live Image:**
```
❌ STEP 2 Required: Please capture or select a live image!

1. Click "Use Camera"
2. Capture your face
3. Or click "Upload File"
```

### Backend Errors (API Response):

**Missing file1:**
```
Status: 400
Message: "❌ Reference image not provided. Please upload reference image first using 'Store Reference' button."
```

**Missing file2:**
```
Status: 400
Message: "❌ Live capture image not provided. Please capture image from camera using 'Use Camera' button."
```

---

## 🎬 Run the Test

1. Open test console: **http://localhost:8001/test_console_v2.html**
2. Try to compare without uploading reference
3. See alert message ✅
4. Upload reference
5. Try to compare without capturing
6. See alert message ✅
7. Capture image
8. Compare should work ✅

**If all three scenarios work as expected: ✅ Validation is working correctly!**
