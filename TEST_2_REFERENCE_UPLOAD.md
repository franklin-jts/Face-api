# TEST 2: Upload Reference & Verify Comparison Works

## 🎯 Test Objective
Verify that when reference image IS uploaded, face comparison works correctly and returns proper match scores.

---

## 📋 Step-by-Step Test Procedure

### STEP 1: Open Test Console
```
URL: http://localhost:8001/test_console_v2.html
Auth Token: secret-token-123
```

### STEP 2: Upload Reference Image
1. **Section:** "STEP 1: Store Reference Image"
2. **Action:** Click **"📎 Upload File"** button
3. **Select:** Any clear face photo (your own face)
   - ✅ Good lighting
   - ✅ Full face visible
   - ✅ Clear eyes, nose, mouth
4. **Verify:** See filename in field: `✓ [filename]`
5. **Click:** **"💾 Upload & Store Reference"** button
6. **Wait:** For response...

### Expected Response:
```json
{
  "status": true,
  "message": "Reference image uploaded and stored successfully",
  "data": {
    "registered": true,
    "storage_filename": "reference_20260921_123456.png",
    "storage_path": "d:\\...\\stored_images\\reference_20260921_123456.png"
  }
}
```

### Validation Points:
- [ ] Response status: `"status": true`
- [ ] Message: "Reference image uploaded and stored successfully"
- [ ] Storage filename shown (with timestamp)
- [ ] Preview shows your face
- [ ] No errors in response

**Result:** ✅ PASS or ❌ FAIL
```
Expected: PASS - Reference uploaded successfully
Status: _____ (record actual)
Filename: _____ (record filename)
```

---

## 📋 STEP 3: Verify Reference Was Stored

### On Disk:
1. Open File Explorer
2. Navigate to: `d:\new\FaceRecognitionAPI\stored_images\`
3. **Look for:** `reference_20260921_*.png` (today's date with timestamp)
4. **Verify:** File exists and was created recently (check modification time)

### Validation Points:
- [ ] File exists in `stored_images/` folder
- [ ] Filename includes timestamp
- [ ] File size > 0 bytes
- [ ] File timestamp is current (just uploaded)

**Result:** ✅ PASS or ❌ FAIL
```
Expected: PASS - File exists on disk
File found: YES / NO
Filename: _____
File size: _____ bytes
```

---

## 📋 STEP 4: Capture Live Image

1. **Section:** "STEP 2B: Test Face Comparison"
2. **Find:** "Live Capture (file2)" subsection
3. **Click:** **"📷 Use Camera"** button
4. **Permission:** Grant camera access
5. **Position:** Close to your face
   - ✅ Arm's length distance (12-18 inches)
   - ✅ Face centered in frame
   - ✅ Face straight ahead
   - ✅ Good lighting
6. **Click:** **"📸 Capture"** button
7. **Verify:** Preview image appears

### Validation Points:
- [ ] Camera stream displayed (not black)
- [ ] Live video visible
- [ ] Capture button clickable
- [ ] Preview shows your face after capture
- [ ] Filename shown: `✓ camera_capture.jpg`

**Result:** ✅ PASS or ❌ FAIL
```
Expected: PASS - Live image captured
Camera worked: YES / NO
Preview visible: YES / NO
```

---

## 📋 STEP 5: Compare Faces

1. **Verify Section:** "STEP 2B: Test Face Comparison"
2. **Check Field 1:** Reference Image (file1)
   - Should show: ✓ `reference_...` with preview
   - [ ] Reference preview visible
3. **Check Field 2:** Live Capture (file2)
   - Should show: ✓ `camera_capture.jpg` with preview
   - [ ] Live preview visible
4. **Check Field 3:** Match Threshold
   - Default: 70 (keep this)
   - [ ] Value is 70
5. **Click:** **"🔍 Compare Faces"** button
6. **Wait:** For response...

### Validation Points:
- [ ] Both file previews visible
- [ ] Threshold value correct (70)
- [ ] Compare button clickable
- [ ] Response appears (not hanging)

---

## 📋 STEP 6: Check Comparison Response

### Expected Response (SAME PERSON - You vs Your Camera):
```json
{
  "status": true,
  "message": "Faces match",
  "data": {
    "face_match": true,
    "match_score": 85.5,
    "liveness_passed": true,
    "challenge_passed": true,
    "challenge_yaw_delta": 15.3
  }
}
```

### Response Analysis:

| Field | Expected | Actual | Status |
|-------|----------|--------|--------|
| `status` | `true` | _____ | ✓/✗ |
| `face_match` | `true` | _____ | ✓/✗ |
| `match_score` | 80-100 | _____ | ✓/✗ |
| `liveness_passed` | `true` | _____ | ✓/✗ |
| `challenge_passed` | `true` | _____ | ✓/✗ |

### Validation Points:
- [ ] `status: true` (success)
- [ ] `face_match: true` (same person)
- [ ] `match_score` is 0-100 number
- [ ] `match_score` is 80+ (high confidence)
- [ ] `liveness_passed: true` (real face, not photo)
- [ ] `challenge_passed: true` (head turned sufficiently)
- [ ] No error messages
- [ ] All fields present in response

**Result:** ✅ PASS or ❌ FAIL
```
Expected: PASS - Comparison successful, high match score
Match Score: _____ (0-100%)
Same Person: _____ (YES/NO)
```

---

## 📋 Troubleshooting If Test Fails

### Problem: Upload fails / "❌ Failed" message
**Solution:**
- Check token is correct: `secret-token-123`
- Verify file is image (JPEG/PNG)
- Check server logs for errors
- Try different image file

### Problem: "move_closer_to_camera" during comparison
**Solution:**
- Capture camera image again, much closer
- Face should fill ~15-20% of screen
- Try capturing again

### Problem: Match score too low (< 80%)
**Solutions:**
1. Different lighting between reference and capture
2. Reference image quality poor
3. Different glasses/hat in each image
4. Head angle different
5. Try uploading a new reference image with current lighting

**Fix:** Lower threshold from 70 → 60, try again

### Problem: "face_match: false" but same person
**Causes:**
- Poor reference image quality
- Very different lighting conditions
- Different head angles
- Glasses difference

**Solution:**
- Upload new reference with good lighting
- Capture in similar lighting
- Try lower threshold (70 → 60 or 50)

### Problem: API error "Reference image not provided"
**Cause:** Reference upload failed silently
**Solution:** Upload reference again, watch for success message

---

## ✅ SUCCESS CRITERIA - All Checks Required

For TEST 2 to PASS, ALL of these must be true:

### Upload Phase:
- [ ] Reference upload response shows `status: true`
- [ ] File appears in `stored_images/` folder
- [ ] Preview shows your face

### Capture Phase:
- [ ] Camera displays live video (not black)
- [ ] Can capture image
- [ ] Preview shows captured face

### Comparison Phase:
- [ ] Response received (not error)
- [ ] `face_match: true` (same person)
- [ ] `match_score` between 80-100%
- [ ] `liveness_passed: true`
- [ ] No error messages

### Overall:
- [ ] Full workflow works end-to-end
- [ ] Reference upload → Compare → Match Success

---

## 📊 Test Results Template

```
TEST 2: Upload Reference & Compare

Date: 2026-09-21
User: [Your Name]

=== UPLOAD REFERENCE ===
Status: PASS / FAIL
Filename: reference_20260921_HHMMSS.png
Stored to disk: YES / NO
Error: (if any) _____

=== CAPTURE LIVE IMAGE ===
Status: PASS / FAIL
Camera worked: YES / NO
Preview visible: YES / NO
Error: (if any) _____

=== COMPARISON ===
Status: PASS / FAIL
Match Score: _____ %
Face Match: YES / NO
Liveness Passed: YES / NO
Error: (if any) _____

=== OVERALL RESULT ===
[✓] PASS - All tests successful, comparison works!
[ ] FAIL - Some issues found (see errors above)

Match Score Expected: 80-100%
Match Score Actual: ____%

NOTES:
_____________________
_____________________
```

---

## 🎬 Execute This Test Now

1. Open: **http://localhost:8001/test_console_v2.html**
2. Upload reference image (your face)
3. See success response
4. Check file on disk
5. Capture from camera
6. Click Compare
7. Check match score

**Report:**
- Did it work? ✅ YES or ❌ NO
- What was the match score?
- Any errors?

---

## 🔗 Related Tests

- **TEST 1:** Compare without reference → Alert shown ✅
- **TEST 2:** Compare with reference → Works ← YOU ARE HERE
- **TEST 3:** Compare without live image → Alert shown
- **TEST 4:** API direct call missing file1 → 400 error
- **TEST 5:** API direct call missing file2 → 400 error
