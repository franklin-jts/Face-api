# Face Comparison Testing Guide

## ✅ System is Working
- ✅ Camera is now fixed (showing live video, not black blocks)
- ✅ Images are being stored locally in `stored_images/`
- ✅ Both `/uploadImage` and `/employeeFaceCompare` endpoints are working

## 📋 How to Test Face Comparison

### Step 1: Store Reference Image
1. Open **http://localhost:8001/test_console_v2.html**
2. Enter Auth Token: `secret-token-123`
3. Scroll to **"STEP 1: Upload & Store Reference"**
4. Click **"Upload File"** 
5. Select your face photo from computer
6. Click **"Store Reference"**
7. ✅ Confirm you see: `✓ reference_20260921_HHMMSS.png` saved

**Image is now stored in:** `d:\new\FaceRecognitionAPI\stored_images\reference_20260921_HHMMSS.png`

---

### Step 2: Capture Live Face for Comparison
1. Still in same console page
2. Scroll to **"STEP 2B: Face Comparison"** 
3. Under **"Live Capture (file2)"**, click **"Use Camera"**
4. Grant camera permission
5. Frame your face in video
6. Click **"📸 Capture"** button
7. ✅ Confirm preview image appears below button

**Captured image is temporary** (not stored until comparison)

---

### Step 3: Compare Faces
1. Make sure both images are selected:
   - ✅ Reference Image: `✓ reference_...` (from Step 1)
   - ✅ Live Capture: ✓ `camera_capture.jpg` (from Step 2)

2. (Optional) Adjust threshold (default 70 = 70% match required)

3. Click **"Compare Faces"** button

4. ✅ See response:

**MATCH (Same Person):**
```json
{
  "status": true,
  "face_match": true,
  "match_score": 85.5,
  "liveness_passed": true,
  "challenge_passed": true,
  "challenge_yaw_delta": 12.5
}
```

**NO MATCH (Different Person):**
```json
{
  "status": false,
  "face_match": false,
  "match_score": 35.2,
  "liveness_passed": true,
  "challenge_passed": false,
  "challenge_yaw_delta": 5.0
}
```

---

## 📊 Understanding the Response

| Field | Meaning |
|-------|---------|
| `status` | True = same person, False = different person |
| `face_match` | True if match_score > threshold |
| `match_score` | 0-100 similarity percentage |
| `liveness_passed` | True if face is real (not photo/video) |
| `challenge_passed` | True if head turned enough (anti-spoof) |
| `challenge_yaw_delta` | Head turn angle (degrees) |

---

## 🔍 Troubleshooting

### Problem: "❌ Please store reference and select comparison image"
**Fix:** Make sure you completed Step 1 AND Step 2. Both must have images selected.

### Problem: "❌ Different Persons" but it's the same face
**Solution:** 
- Try adjusting threshold LOWER (e.g., 60 instead of 70)
- Make sure lighting is similar in both photos
- Avoid sunglasses/hats if possible

### Problem: "face_detected": false
**Fix:** 
- Move closer to camera
- Ensure good lighting on your face
- Try the Liveness test first to verify face detection works

### Problem: Camera shows black block
**Fix:** (Already fixed in latest version)
- Refresh page (Ctrl+R)
- Clear browser cache
- Try different browser (Chrome > Firefox)

---

## 🗂️ File Storage Location

All comparison images are stored here:
```
d:\new\FaceRecognitionAPI\stored_images\
├── reference_20260921_060844.png    ← Stored reference images
├── reference_20260920_141523.png
├── liveness_20260919_094340.jpg     ← Liveness test captures
├── liveness_20260919_094355.jpg
└── ... (more images)
```

**Check stored images:** Visit `http://localhost:8001/dev/stored-images`

---

## 🎯 Full Workflow Summary

```
REFERENCE IMAGE (stored)     +     LIVE CAPTURE (camera)
        ↓                                    ↓
   Extract face embedding            Extract face embedding
        ↓                                    ↓
        └──────────→ Compare Cosine Similarity ←──────┘
                            ↓
                      Match Score (0-100)
                            ↓
                   Compare with Threshold
                            ↓
                    ✅ MATCH or ❌ NO MATCH
```

---

## ✅ Test Verification Checklist

- [ ] Camera is displaying live video (not black)
- [ ] Reference image stored to `stored_images/reference_*.png`
- [ ] Can capture from camera without errors
- [ ] Comparison returns JSON response with `face_match` field
- [ ] Getting same person match when comparing own face with own camera capture
- [ ] Getting different person when comparing with different person's photo

If all checks pass: ✅ **System is working correctly!**
