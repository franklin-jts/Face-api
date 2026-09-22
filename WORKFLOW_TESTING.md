# 🎯 Advanced Testing Workflow Guide

## Two Test Console Versions

### **Simple Test Console** (Original)
**URL:** http://localhost:8001/test_console.html

- Upload images directly
- Test one-off requests
- Good for API exploration

### **Advanced Test Console** (NEW) ⭐ **USE THIS**
**URL:** http://localhost:8001/test_console_v2.html

- **Store reference image once**
- **Reuse stored image for multiple tests**
- Workflow-based testing
- **Perfect for your use case!**

---

## 🔄 Advanced Workflow (test_console_v2.html)

### **Step 1: Store Reference Image**

1. Open: http://localhost:8001/test_console_v2.html
2. Enter token: `secret-token-123`
3. **Section: "📚 Step 1: Store Reference Image"**
4. Click **"📤 Choose Reference Image"**
5. Select an image file (JPEG/PNG)
6. Click **"💾 Upload & Store Reference"**
7. ✅ You'll see: "✅ Reference image stored successfully"

```
Reference Image (Stored on Server)
[image preview shown]
✅ Reference image stored successfully and ready for testing!
```

---

### **Step 2a: Test Liveness (on Stored Image)**

Once reference is stored, test if it's a live face:

1. **Section: "👁️ Step 2a: Test Liveness"**
2. Click **"📎 Use Stored"** (uses stored reference)
3. You'll see the stored image preview
4. Click **"🔍 Check Liveness"**
5. Get liveness result:

```json
{
  "status": true/false,
  "message": "Liveness check passed/failed",
  "data": {
    "liveness_passed": true/false,
    "liveness_score": 0.85,
    "face_detected": true,
    "spoof_detected": false
  }
}
```

---

### **Step 2b: Test Face Comparison**

Compare stored reference with new images:

1. **Section: "🔄 Step 2b: Test Face Comparison"**
2. Click **"📎 Upload New"** to select comparison image
3. Or **"📷 Use Camera"** to capture from webcam
4. Set match threshold (default: 70)
5. Click **"🔍 Compare Faces"**
6. Get comparison result:

```json
{
  "status": true/false,
  "message": "Face recognition successful/not successful",
  "data": {
    "face_match": true/false,
    "match_score": 85.5,
    "liveness_passed": true,
    "challenge_passed": true
  }
}
```

---

## 📋 Testing Workflow Example

### **Use Case: Verify Same Person**

1. **Upload Reference:** Employee's official photo
   - Click "📤 Choose Reference Image"
   - Select official_photo.jpg
   - Click "💾 Upload & Store Reference"
   - ✅ Stored on server

2. **Test Liveness:** Verify official photo is not a spoof
   - Click "📎 Use Stored"
   - Click "🔍 Check Liveness"
   - Result: `liveness_passed: true/false`

3. **Test Comparison:** Compare with new capture
   - Click "📷 Use Camera"
   - Capture employee's face
   - Set threshold: 75
   - Click "🔍 Compare Faces"
   - Result: `face_match: true/false`, `match_score: 92.5`

4. **Repeat Step 3** with different poses/angles without re-uploading reference

---

## 🎥 Camera Capture Features

### **Liveness Camera Test**
- Click "📷 Use Camera"
- Frame your face
- Click "📸 Capture"
- Image is captured and preview shown
- Click "🔍 Check Liveness"

### **Comparison Camera Test**
- Click "📷 Use Camera"
- Frame your face (different angle/lighting)
- Click "📸 Capture"
- Image is captured and preview shown
- Click "🔍 Compare Faces"

---

## 📊 Expected Results

### **Liveness Test Results**

**Live Face (✅)**
```json
{
  "status": true,
  "liveness_passed": true,
  "liveness_score": 0.82,
  "spoof_detected": false,
  "face_detected": true
}
```

**Spoof/Photo (❌)**
```json
{
  "status": false,
  "liveness_passed": false,
  "liveness_score": 0.2,
  "spoof_detected": true,
  "face_detected": true
}
```

### **Comparison Test Results**

**Same Person (✅)**
```json
{
  "status": true,
  "face_match": true,
  "match_score": 87.5,
  "liveness_passed": true,
  "challenge_passed": true
}
```

**Different Person (❌)**
```json
{
  "status": false,
  "face_match": false,
  "match_score": 45.2,
  "message": "Face recognition not successful"
}
```

---

## 🔧 Advanced Features

### **Match Threshold**
- **Range:** 0-100
- **Default:** 70
- **Meaning:** Minimum similarity score to consider it a match
- **Lower (50):** More matches, more false positives
- **Higher (90):** Fewer matches, stricter matching

Example:
- Score 85 + Threshold 70 = ✅ Match
- Score 65 + Threshold 70 = ❌ No Match

### **Stored Image Persistence**
- Reference image is stored on server in `temp/reference.jpg`
- Persists between tests
- Can run multiple comparison tests without re-uploading
- Reset with: **POST** `/dev/reset-cache`

---

## 🛠️ Troubleshooting

### **"Please store a reference image first"**
- Step 1 not completed
- Upload and store reference using "💾 Upload & Store Reference"

### **Camera not working**
- Browser needs HTTPS or localhost
- Check camera permissions
- Try different browser

### **"No face detected" in liveness**
- Face too far from camera
- Poor lighting
- Face partially obscured
- Try with different image

### **Match score too low**
- Different persons
- Poor lighting in one image
- Face angles too different
- Try increasing camera distance/lighting

---

## 📈 Production Usage

### **For Your Flutter App**

Your mobile client can:

1. **First Time:**
   ```
   POST /uploadImage
   - Send employee's official photo
   - Server stores it
   ```

2. **Verification Time (repeated):**
   ```
   POST /employeeFaceCompare
   - Send: reference image (same as stored)
   - Send: live capture from camera
   - Get: match result + liveness score
   ```

3. **No need to re-upload reference!**
   - Once stored, reuse it
   - Multiple verification attempts
   - Single network trip to store

---

## ✅ Checklist

- [ ] App is running on port 8001
- [ ] Models are loaded (YuNet + SFace)
- [ ] Open test_console_v2.html
- [ ] Enter auth token
- [ ] Upload & store reference image
- [ ] Test liveness on stored image
- [ ] Test comparison with camera/upload
- [ ] Verify JSON responses
- [ ] Ready for Flutter integration!

---

## 📚 Quick Reference

| Step | Action | Result |
|------|--------|--------|
| 1 | Upload reference | ✅ Stored on server |
| 2a | Check liveness | 🟢 Live or 🔴 Spoof |
| 2b | Compare faces | 🟢 Match or 🔴 No Match |
| 3 | Repeat 2a/2b | No re-upload needed |

---

## 🎯 Next: Flutter Integration

Once testing is complete:

1. **Share test results** with your Flutter team
2. **Use same `/employeeFaceCompare` endpoint** in app
3. **Send Bearer token** in header
4. **Parse JSON responses** (same structure as tests)

---

**Status: Ready for workflow-based testing!** 🚀

Use http://localhost:8001/test_console_v2.html for the best testing experience.
