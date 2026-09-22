# 📋 Threshold Testing Results

## Test Summary
**Date**: September 21, 2026  
**Tester**: [Your Name]  
**API Version**: YuNet + SFace  
**Default Threshold**: 70

---

## Test Results

### Test 1: Same Person - Close Distance (30cm)

| # | Threshold | Match Score | Result | Status |
|---|---|---|---|---|
| 1 | 50 | ? | ? | ⏳ |
| 2 | 60 | ? | ? | ⏳ |
| 3 | 70 | ? | ? | ⏳ |
| 4 | 80 | ? | ? | ⏳ |
| 5 | 90 | ? | ? | ⏳ |

**Instructions**:
1. Upload reference image at ~30cm distance
2. Capture test image at same distance, same angle
3. For each threshold row:
   - Set threshold value in console
   - Click "🔍 Compare Faces"
   - Copy the `match_score` from response
   - Record result (true/false)

**Expected**: Scores should be 85-95

---

### Test 2: Same Person - Medium Distance (60cm)

| # | Threshold | Match Score | Result | Status |
|---|---|---|---|---|
| 1 | 50 | ? | ? | ⏳ |
| 2 | 60 | ? | ? | ⏳ |
| 3 | 70 | ? | ? | ⏳ |
| 4 | 80 | ? | ? | ⏳ |
| 5 | 90 | ? | ? | ⏳ |

**Instructions**:
1. Use same reference image
2. Capture test image at ~60cm distance (twice as far)
3. Record match scores and results

**Expected**: Scores should drop to 75-85

---

### Test 3: Same Person - Far Distance (100cm+)

| # | Threshold | Match Score | Result | Status |
|---|---|---|---|---|
| 1 | 50 | ? | ? | ⏳ |
| 2 | 60 | ? | ? | ⏳ |
| 3 | 70 | ? | ? | ⏳ |
| 4 | 80 | ? | ? | ⏳ |
| 5 | 90 | ? | ? | ⏳ |

**Instructions**:
1. Use same reference image
2. Capture test image at ~100cm+ distance (very far)
3. Record match scores and results

**Expected**: Scores should drop to 65-75

---

### Test 4: Same Person - Different Angle (Head Turn 30°)

| # | Threshold | Match Score | Result | Status |
|---|---|---|---|---|
| 1 | 50 | ? | ? | ⏳ |
| 2 | 60 | ? | ? | ⏳ |
| 3 | 70 | ? | ? | ⏳ |
| 4 | 80 | ? | ? | ⏳ |
| 5 | 90 | ? | ? | ⏳ |

**Instructions**:
1. Use same reference image (face straight)
2. Capture test image with head turned ~30° to side
3. Record match scores and results

**Expected**: Scores should be 70-85

---

### Test 5: Different Person

| # | Threshold | Match Score | Result | Status |
|---|---|---|---|---|
| 1 | 50 | ? | ? | ⏳ |
| 2 | 60 | ? | ? | ⏳ |
| 3 | 70 | ? | ? | ⏳ |
| 4 | 80 | ? | ? | ⏳ |
| 5 | 90 | ? | ? | ⏳ |

**Instructions**:
1. Keep same reference image
2. Capture test image with **completely different person**
3. Record match scores and results

**Expected**: Scores should be 20-60 (all false)

---

## 📊 Score Distribution Analysis

After completing all tests, fill in this table:

### Scores for SAME PERSON:
- Closest distance (30cm): _____ 
- Medium distance (60cm): _____ 
- Far distance (100cm+): _____ 
- Different angle: _____ 
- **Minimum score**: _____ 
- **Maximum score**: _____ 

### Scores for DIFFERENT PERSON:
- Capture 1: _____ 
- Capture 2: _____ 
- Capture 3: _____ 
- **Maximum score**: _____ 

---

## 🎯 Optimal Threshold Calculation

```
Same Person Minimum Score:  _____ (e.g., 72)
Different Person Maximum Score: _____ (e.g., 68)
Optimal Threshold: _____ (should be between min and max)
```

**Recommendation**: Set threshold to **_____**

---

## 📋 Distance Impact Analysis

How much does distance affect matching?

```
Close (30cm):      _____ → Easy to match ✅
Medium (60cm):     _____ → Moderate difficulty 
Far (100cm+):      _____ → Hard to match ⚠️
Different angle:   _____ → ⚠️ Angle affects match
```

---

## ✅ Verification Checklist

- [ ] Tested same person at 3 different distances
- [ ] Tested same person at different angle
- [ ] Tested completely different person
- [ ] Recorded all match scores
- [ ] Identified minimum score for same person
- [ ] Identified maximum score for different person
- [ ] Calculated optimal threshold
- [ ] Verified threshold works correctly
- [ ] Documented all findings

---

## 🔍 Quality Assessment

### Lighting Conditions
- [ ] Good lighting (bright, no shadows)
- [ ] Normal lighting (indoor, moderate)
- [ ] Low lighting (dim, challenging)
- [ ] Varied - test all three

**Lighting Impact**: _______________

### Face Quality
- [ ] Clear, no blur
- [ ] Good contrast
- [ ] Full face visible
- [ ] No glasses/obstructions

**Quality Issues**: _______________

### Image Consistency
- [ ] Reference image quality: _____ / 10
- [ ] Test image quality: _____ / 10
- [ ] Consistency between tests: _____ / 10

---

## 📝 Key Findings

**1. Distance Effect**
Distance from camera affects match score? **Yes / No**
- How much: _____ points per 30cm

**2. Angle Effect**
Head angle affects match score? **Yes / No**
- How much: _____ points per 15° turn

**3. Lighting Effect**
Lighting affects match score? **Yes / No**
- How much: _____ points per lighting level

---

## 💡 Recommendations

**Recommended Threshold**: _____

**Why**: 
- Same person minimum: _____
- Different person maximum: _____
- Safe margin: _____

**Expected Performance**:
- False Negative Rate (same person rejected): _____ %
- False Positive Rate (different person accepted): _____ %

---

## 🚀 Next Steps

1. [ ] Set threshold to recommended value
2. [ ] Deploy to production
3. [ ] Monitor false positives/negatives
4. [ ] Re-test with real users
5. [ ] Adjust if needed

---

## Notes

```
Add any additional observations, issues, or recommendations here:

_________________________________________________________________

_________________________________________________________________

_________________________________________________________________
```

---

**Report Generated**: _______________  
**Tested By**: _______________  
**Approved By**: _______________
