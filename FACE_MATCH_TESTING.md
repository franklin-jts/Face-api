# Face Matching - Complete Testing Guide

## ✅ What You're Testing

After uploading a reference image and capturing from camera:
1. ✅ **Liveness Check:** Is the captured face real? (not a photo)
2. ✅ **Face Match:** Does captured face match the reference image? (same person?)

---

## 📋 Complete Workflow (4 Steps)

### STEP 1: Upload & Store Reference Image
**This is the "known good" face to compare against**

1. Open: **http://localhost:8001/test_console_v2.html**
2. Enter Auth Token: `secret-token-123`
3. Find **"STEP 1: Upload & Store Reference"**
4. Click **"Upload File"**
5. Select a photo of yourself (clear face, good lighting)
6. Click **"Store Reference"**
7. ✅ You should see: `✓ reference_20260921_HHMMSS.png`

**Stored Location:** `d:\new\FaceRecognitionAPI\stored_images\reference_20260921_HHMMSS.png`

---

### STEP 2: Capture Live Face from Camera
**This is the "test" face to compare**

1. Scroll to **"STEP 2B: Face Comparison"** section
2. Under **"Live Capture (file2)"**, click **"Use Camera"**
3. Grant camera permission
4. **Position correctly:**
   - 📷 ← 12-18 inches away → 👤 (arm's length)
   - Face centered in frame
   - Face straight ahead (not tilted)
   - Good lighting on face
5. Click **"📸 Capture"**
6. ✅ You should see preview: ✓ `camera_capture.jpg`

---

### STEP 3: Compare Both Faces
**This sends both images to API for matching**

1. Make sure both files are selected:
   - ✅ Reference Image (file1): Shows preview
   - ✅ Live Capture (file2): Shows preview
2. (Optional) Adjust threshold (default 70 = 70% match required)
3. Click **"Compare Faces"** button
4. Wait for response...

---

### STEP 4: Check Response

#### ✅ MATCH (Same Person):
```json
{
  "status": true,
  "message": "Faces match",
  "data": {
    "face_match": true,
    "match_score": 87.5,
    "liveness_passed": true,
    "challenge_passed": true,
    "challenge_yaw_delta": 15.3
  }
}
```
→ **✅ SUCCESS: Same person detected!**

#### ❌ NO MATCH (Different Person):
```json
{
  "status": false,
  "message": "Faces do not match",
  "data": {
    "face_match": false,
    "match_score": 42.1,
    "liveness_passed": true,
    "challenge_passed": false,
    "challenge_yaw_delta": 5.2
  }
}
```
→ **❌ MISMATCH: Different person or poor capture**

---

## 📊 Understanding Response Fields

| Field | Meaning | Range |
|-------|---------|-------|
| `status` | Test passed? | true/false |
| `face_match` | Faces match? | true/false |
| `match_score` | Similarity score | 0-100% |
| `liveness_passed` | Face is real? | true/false |
| `challenge_passed` | Head turned enough? | true/false |
| `challenge_yaw_delta` | Head turn angle | 0-90° |

---

## ✅ Troubleshooting

### Problem: "Please store reference and select comparison image"
**Fix:**
- [ ] Did you complete STEP 1? (Store Reference)
- [ ] Did you complete STEP 2? (Capture from Camera)
- Both must be done before comparing

### Problem: Response shows "move_closer_to_camera"
**Fix:**
- Move camera significantly closer to face
- Face should fill ~15-20% of screen
- Distance: arm's length (12-18 inches)

### Problem: "Different Persons" but it's same face
**Possible Causes:**
- Different lighting (reference vs live)
- Different glasses (have glasses vs no glasses)
- Head angle different
- Face expression too different

**Solutions:**
1. Try with more similar conditions:
   - Same lighting
   - Same glasses (both with or both without)
   - Neutral expression
   
2. Lower the threshold:
   - Change from 70 → 60 or 50
   - Click "Compare Faces" again

3. Retake reference image:
   - Use current camera capture as new reference
   - Ensures matching conditions

### Problem: "whole_face_not_visible" or "centre_your_face"
**Fix:**
- Reframe camera
- Include full face (top of head to chin)
- Center face in frame (not at edges)
- Try capturing again

### Problem: Camera shows black/blank
**Fix:**
- Refresh page (Ctrl+R)
- Clear browser cache
- Try different browser (Chrome > Firefox)
- Check camera permissions in browser settings

---

## 🎯 Success Checklist

For a successful face match:

**Reference Image:**
- [ ] Clear face photo
- [ ] Good lighting
- [ ] Face fills decent portion of image
- [ ] No blur or shadows on face

**Live Capture:**
- [ ] Face passes liveness check (real, not photo)
- [ ] Face fills ~15-20% of screen
- [ ] Face centered in frame
- [ ] Good lighting
- [ ] Similar conditions to reference (glasses, lighting, angle)

**Comparison Result:**
- [ ] `"face_match": true` OR `"face_match": false`
- [ ] `"match_score"` shows % similarity
- [ ] Clear JSON response (no errors)

---

## 📈 Example: Full Test Sequence

```
STEP 1: Upload photo of yourself (glasses, good lighting)
        ↓
        ✓ reference_20260921_060844.png stored
        ↓
STEP 2: Capture from camera (same glasses, same lighting, close)
        ↓
        ✓ camera_capture.jpg ready
        ↓
STEP 3: Click "Compare Faces"
        ↓
        ✅ JSON Response:
           {
             "status": true,
             "face_match": true,
             "match_score": 89.2,
             "liveness_passed": true
           }
        ↓
RESULT: ✅ SUCCESS - Same person!
```

---

## 🔍 File Locations

**Reference images stored:**
```
d:\new\FaceRecognitionAPI\stored_images\
├── reference_20260921_060844.png
├── reference_20260921_061523.png
└── reference_20260920_141200.png
```

**View all stored images:**
- Visit: `http://localhost:8001/dev/stored-images`
- Download any image: `http://localhost:8001/dev/stored-images/reference_20260921_060844.png`

---

## 🎬 Now Test It!

1. Open: **http://localhost:8001/test_console_v2.html**
2. Follow all 4 steps above
3. Compare your face with itself (should match 80%+)
4. Try with different person (should NOT match)

Let me know the results! 📸✅
