# Face Validation - STRICTER Requirements

## ✅ What Changed

The API now has **STRICTER face validation** to reject:
- ❌ Wall, ceiling, objects
- ❌ Body parts (hands, shoulders, back of head)
- ❌ Distant/small faces
- ❌ Faces at angles
- ❌ Low confidence detections

---

## 📋 New Validation Requirements

| Requirement | Old | New | Purpose |
|------------|-----|-----|---------|
| **Face Size** | 3.5% of image | **15% of image** | Reject distant faces |
| **Minimum Pixels** | 100x100 | **200x200** | Only clear, close faces |
| **Centered** | ±28% from center | **±25% from center** | Face must be framed properly |
| **Straight Facing** | ±12° eye tilt | **±10° eye tilt** | Stricter head alignment |
| **Nose Alignment** | ±0.22 offset | **±0.18 offset** | More precise centering |
| **Confidence** | > 70% | **> 75%** | Higher detection certainty |

---

## ✅ What Will PASS (Accept)

✅ Your face, **close to camera** (arm's length)
✅ Face **centered in frame**
✅ Face **looks straight at camera**
✅ **Good lighting** on face
✅ **Only face visible** (no background dominance)

### Example - GOOD:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━
┃        Your Face         ┃
┃    👤 (large, centered)   ┃
┃    Clear & well-lit       ┃
━━━━━━━━━━━━━━━━━━━━━━━━━━
→ ✅ ACCEPTED
```

---

## ❌ What Will FAIL (Reject)

❌ Wall, ceiling, objects
❌ Distant face (too small)
❌ Face at edge of frame
❌ Head turned to side
❌ Poor lighting
❌ Only half of face visible

### Example - BAD:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━
┃  Wall  | tiny 👤 | Room   ┃
┃        (too small)        ┃
━━━━━━━━━━━━━━━━━━━━━━━━━━
→ ❌ REJECTED
```

---

## 🎯 How to Capture Correctly

**Step 1: Position Camera**
```
Distance: Arm's length away (12-18 inches / 30-45 cm)
Height: Eye level or slightly above
Angle: Straight on (don't tilt device)
```

**Step 2: Frame Your Face**
```
Head Position:
  • Top of head: ~1-2 inches from top of frame
  • Bottom of face: ~2-3 inches from bottom
  • Eyes: Center vertically
  • Left/Right: Centered horizontally
```

**Step 3: Lighting**
```
✅ Good: Front-facing light (window, lamp)
✅ Good: Even lighting across face
❌ Bad: Backlighting (light behind you)
❌ Bad: Dark/shadowy areas
❌ Bad: Direct sun glare
```

**Step 4: Capture**
```
Look straight at camera
No tilt/angle (face forward)
Don't smile excessively (neutral better)
Don't move (stay still)
Click "📸 Capture"
```

---

## 📊 Response Messages

If validation fails, you'll see one of these reasons:

| Message | Meaning | Fix |
|---------|---------|-----|
| `"move_closer_to_camera"` | Face too small | Move closer (arm's length) |
| `"whole_face_not_visible"` | Part cut off | Center face, include whole head |
| `"centre_your_face"` | Face at edge | Reframe to center |
| `"look_straight_at_camera"` | Head tilted/angled | Face straight forward |
| `"low_face_detection_confidence"` | Poor quality | Better lighting, clearer image |

---

## ✅ Test Checklist

Before capturing, verify:
- [ ] Face fills ~15% of frame (noticeably large)
- [ ] Face is centered (not at edges)
- [ ] Face is straight (not tilted/angled)
- [ ] Good lighting on face
- [ ] Whole face visible (no cropping)
- [ ] Still/not moving
- [ ] Only ONE face in frame

If all checked: ✅ **Should pass validation!**

---

## 🔧 If Still Failing

**Problem: "move_closer_to_camera"**
- Solution: Move camera significantly closer (reduce distance by half)
- Target: Face should be ~1/3 of screen height

**Problem: "whole_face_not_visible"**
- Solution: Reframe so top of head visible, chin visible
- Adjust: Move camera back slightly if too close

**Problem: "look_straight_at_camera"**
- Solution: Face directly forward, no tilting
- Check: Eyes level, both eyes clearly visible

**Problem: Still rejecting valid faces?**
- Try: Better lighting conditions
- Try: Move closer (faces < 15% of image fail)
- Try: Restart browser (clear cache)

---

## 🎥 Why These Rules?

The stricter validation ensures:

1. **Quality Recognition:** Large, clear faces = accurate comparison
2. **Anti-Spoofing:** Close, frontal faces harder to spoof with photos
3. **Consistency:** Same rules applied to reference + live capture
4. **User Experience:** Clear feedback on what to do

When both reference image and live capture meet these rules:
→ ✅ High accuracy face comparison (85%+ match score)
