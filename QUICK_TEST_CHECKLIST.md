# Quick Face Comparison Test Checklist

## 🎯 Before You Start
- [ ] Server running on port 8001
- [ ] Browser open to: **http://localhost:8001/test_console_v2.html**
- [ ] Auth Token: `secret-token-123`

---

## ✅ STEP 1: Store Reference (3 min)
- [ ] Click "STEP 1: Upload & Store Reference"
- [ ] Click "Upload File"
- [ ] Select face photo (clear, good lighting, full face visible)
- [ ] Click "Store Reference"
- [ ] See: ✓ `reference_20260921_HHMMSS.png` ✅

---

## ✅ STEP 2: Capture Live Face (2 min)
- [ ] Scroll to "STEP 2B: Face Comparison"
- [ ] Click "Use Camera" under "Live Capture (file2)"
- [ ] Grant camera permission
- [ ] Position camera:
  - [ ] Close to face (arm's length away)
  - [ ] Face centered in frame
  - [ ] Face straight ahead (not tilted)
  - [ ] Good lighting on face
- [ ] Click "📸 Capture"
- [ ] See preview: ✓ `camera_capture.jpg` ✅

---

## ✅ STEP 3: Compare Faces (1 min)
- [ ] Verify Reference Image shows: ✓ `reference_...`
- [ ] Verify Live Capture shows: ✓ `camera_capture.jpg`
- [ ] Threshold: Keep 70 (or adjust if needed)
- [ ] Click "Compare Faces"
- [ ] Wait for response...

---

## ✅ STEP 4: Check Result

### If SAME Person:
```
Status: ✅
face_match: true
match_score: 80-100%
liveness_passed: true
```
✅ **SUCCESS!**

### If DIFFERENT Person:
```
Status: ❌
face_match: false
match_score: 0-50%
liveness_passed: true
```
✅ **CORRECT! (Should not match)**

### If LIVENESS FAILED:
```
liveness_passed: false
liveness_reason: "move_closer_to_camera"
       or
liveness_reason: "centre_your_face"
       or
liveness_reason: "look_straight_at_camera"
```
→ **Retry STEP 2, adjust as suggested**

---

## 🔧 If Not Working

### Camera shows black?
1. Refresh page (Ctrl+R)
2. Check browser permissions (allow camera)
3. Try different browser

### "move_closer_to_camera"?
1. Move camera much closer to face
2. Face should fill ~15-20% of screen
3. Try capturing again

### "Different Persons" but same face?
1. Try with same lighting conditions
2. Same glasses (both with or both without)
3. Adjust threshold lower (70 → 60)

### Still not working?
1. Check console for errors (F12)
2. Verify token is correct
3. Check server logs (see error messages)

---

## 📱 What Good Capture Looks Like

```
✅ GOOD:
━━━━━━━━━━━━━━━━━━━━━━
┃                    ┃
┃    👤 (Large)      ┃  Face fills ~15-20%
┃  Clear & Centered  ┃  Good lighting
┃  Looking Straight  ┃  Full face visible
┃                    ┃
━━━━━━━━━━━━━━━━━━━━━━

❌ BAD:
━━━━━━━━━━━━━━━━━━━━━━
┃ Wall  │tiny👤│Room  ┃  Face too small
┃       (blurry)      ┃  Poor lighting
┃       (tilted)      ┃  Not centered
━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📊 Expected Results

| Test | Expected Result | Actual Result |
|------|-----------------|---------------|
| Same person, good lighting | Match: 85-100% | |
| Same person, glasses difference | Match: 60-80% | |
| Different person | No match: 0-40% | |
| Distant face | Rejection + error | |
| Wall/object | Rejection + error | |

---

## ✅ System Validation

All checks pass? ✅ **System is working!**

- [ ] Reference image stored to disk
- [ ] Camera capture works (not black)
- [ ] Face validation works (rejects distant/non-face)
- [ ] Same person face comparison works (matches 80%+)
- [ ] Different person comparison works (no match)
- [ ] Response JSON is valid
- [ ] Match score shown in response

---

## 🎉 Test Complete!

Once you see this:
```json
{
  "status": true,
  "face_match": true,
  "match_score": 87.5,
  "liveness_passed": true
}
```

✅ **Your Face Recognition API is working perfectly!**
