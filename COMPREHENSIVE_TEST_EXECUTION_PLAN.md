# 📋 Comprehensive Test Execution Plan - Face Recognition API

**Total Test Cases**: 76  
**Categories**: 14  
**Priority Distribution**:
- P0 (Critical): 28 tests
- P1 (Major): 40 tests
- P2 (Minor): 8 tests

---

## 🎯 Test Execution Strategy

### Phase 1: Critical Tests (P0) - Day 1
**28 Tests** - Must Pass Before Other Tests  
**Estimated Time**: 4-5 hours

### Phase 2: Major Tests (P1) - Day 2-3
**40 Tests** - Core Functionality Validation  
**Estimated Time**: 6-8 hours

### Phase 3: Minor Tests (P2) - Day 4
**8 Tests** - Edge Cases & UX Polish  
**Estimated Time**: 2-3 hours

---

## 📊 Test Cases by Category

### 1️⃣ ENROLLMENT (8 Tests)

#### FV-001: Valid Face Enrollment ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Active employee; camera allowed  
**Steps**:
1. Open enrollment screen
2. Center face in frame
3. Complete liveness check
4. Submit enrollment
5. Verify success message

**Expected Result**: Enrollment succeeds and template is linked to correct employee  
**Test Data**: Real single face, normal lighting  
**Status**: ⏳ Not Run  

---

#### FV-002: No Face During Enrollment ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Enrollment screen open  
**Steps**:
1. Point camera away
2. Attempt capture with no face
3. Check error message

**Expected Result**: Block submission and request a face  
**Test Data**: No face  
**Status**: ⏳ Not Run  

---

#### FV-003: Multiple Faces During Enrollment ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Enrollment screen open  
**Steps**:
1. Place 2+ people in frame
2. Attempt enrollment submission
3. Verify rejection

**Expected Result**: Block enrollment; require exactly one face  
**Test Data**: Multiple faces  
**Status**: ⏳ Not Run  

---

#### FV-004: Low-Light Enrollment ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Camera available  
**Steps**:
1. Dim lighting to minimal
2. Attempt enrollment
3. Check quality feedback

**Expected Result**: Reject poor-quality capture and guide lighting  
**Test Data**: Low illumination  
**Status**: ⏳ Not Run  

---

#### FV-005: Strong Backlight Enrollment ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Camera available  
**Steps**:
1. Stand against bright window
2. Attempt enrollment submission
3. Check repositioning request

**Expected Result**: Request repositioning until face quality is sufficient  
**Test Data**: Backlit face  
**Status**: ⏳ Not Run  

---

#### FV-006: Re-enroll Existing Employee ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Employee already enrolled  
**Steps**:
1. Attempt replacement enrollment
2. Verify authorized re-enrollment flow
3. Check audit trail

**Expected Result**: Apply authorized re-enrollment flow; audit replacement  
**Test Data**: Existing template  
**Status**: ⏳ Not Run  

---

#### FV-007: Enrollment Interrupted ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Enrollment started  
**Steps**:
1. Close/background app before completion
2. Reopen app
3. Check enrollment status

**Expected Result**: Incomplete enrollment must not become active  
**Test Data**: Interrupted flow  
**Status**: ⏳ Not Run  

---

#### FV-008: Face Match - Correct Employee ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Employee enrolled  
**Steps**:
1. Start verification
2. Complete liveness check
3. Submit for matching
4. Check result

**Expected Result**: Liveness and identity match pass  
**Test Data**: Genuine enrolled employee  
**Status**: ⏳ Not Run  

---

### 2️⃣ FACE MATCHING (7 Tests)

#### FV-009: Different Employee Verification ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: A logged in; B on camera  
**Steps**:
1. Employee A logs in
2. Employee B attempts verification with their face
3. Check rejection

**Expected Result**: Reject match and create no attendance  
**Test Data**: Wrong genuine person  
**Status**: ⏳ Not Run  

---

#### FV-010: Slight Head Angle ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled  
**Steps**:
1. Verify with slight left/right angle (±10°)
2. Check match result

**Expected Result**: Verify within supported tolerance  
**Test Data**: Moderate pose  
**Status**: ⏳ Not Run  

---

#### FV-011: Glasses Variation ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled without glasses  
**Steps**:
1. Wear normal glasses
2. Attempt verification
3. Check match result

**Expected Result**: Genuine employee handled within supported tolerance  
**Test Data**: Eyeglasses  
**Status**: ⏳ Not Run  

---

#### FV-012: Beard/Hair Appearance Change ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled  
**Steps**:
1. Verify after normal appearance change (beard, hair)
2. Check match result

**Expected Result**: Verify genuine user or give controlled re-enrollment guidance  
**Test Data**: Changed facial hair/hair  
**Status**: ⏳ Not Run  

---

#### FV-013: Mask/Covered Face ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled  
**Steps**:
1. Cover significant lower face with mask
2. Attempt verification
3. Check response

**Expected Result**: Request unobstructed face when evidence is insufficient  
**Test Data**: Face mask  
**Status**: ⏳ Not Run  

---

#### FV-014: Partial Face Outside Frame ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled  
**Steps**:
1. Move face partly outside guide/frame
2. Check quality feedback

**Expected Result**: Block/quality-fail and guide user to center face  
**Test Data**: Partial face  
**Status**: ⏳ Not Run  

---

#### FV-015: Genuine Live Face ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Liveness enabled  
**Steps**:
1. Complete live challenge naturally (blink, move)
2. Check liveness result
3. Verify continuation to match

**Expected Result**: Pass liveness and continue to match  
**Test Data**: Real person  
**Status**: ⏳ Not Run  

---

### 3️⃣ LIVENESS DETECTION (9 Tests)

#### FV-016: Printed Photograph Spoof ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Authorized QA spoof media  
**Steps**:
1. Present printed employee photo to camera
2. Attempt verification
3. Check rejection

**Expected Result**: Reject spoof; no attendance  
**Test Data**: Printed photo  
**Status**: ⏳ Not Run  

---

#### FV-017: Photo on Another Phone ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Authorized QA spoof media  
**Steps**:
1. Display static photo on phone screen
2. Point to camera
3. Check rejection

**Expected Result**: Reject spoof  
**Test Data**: Digital photo  
**Status**: ⏳ Not Run  

---

#### FV-018: Prerecorded Video on Phone ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Authorized QA replay media  
**Steps**:
1. Play employee video on phone to camera
2. Check replay detection
3. Verify rejection

**Expected Result**: Reject replay attack  
**Test Data**: Replay video  
**Status**: ⏳ Not Run  

---

#### FV-019: Prerecorded Video on Laptop/Tablet ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Authorized QA replay media  
**Steps**:
1. Play employee video on larger screen
2. Point camera to display
3. Check rejection

**Expected Result**: Reject replay attack  
**Test Data**: Replay video on large display  
**Status**: ⏳ Not Run  

---

#### FV-020: Screenshot Attack ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Authorized QA image  
**Steps**:
1. Display previous screenshot
2. Point camera
3. Check static image rejection

**Expected Result**: Reject static replay  
**Test Data**: Screenshot  
**Status**: ⏳ Not Run  

---

#### FV-021: Blink Challenge Not Completed ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Challenge liveness enabled  
**Steps**:
1. When blink requested, do NOT blink
2. Wait for timeout
3. Check failure

**Expected Result**: Fail/timeout challenge  
**Test Data**: No response to blink  
**Status**: ⏳ Not Run  

---

#### FV-022: Wrong Head-Turn Challenge ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Challenge liveness enabled  
**Steps**:
1. When asked to turn left, turn right
2. Check challenge result
3. Verify failure

**Expected Result**: Do not mark challenge successful  
**Test Data**: Wrong movement  
**Status**: ⏳ Not Run  

---

#### FV-023: Repeated Failed Attempts ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Retry policy configured  
**Steps**:
1. Fail liveness repeatedly (5-10 times)
2. Check rate limit enforcement
3. Verify lock/throttle activation

**Expected Result**: Enforce configured rate-limit/lock/retry policy  
**Test Data**: Repeated failures  
**Status**: ⏳ Not Run  

---

### 4️⃣ ENVIRONMENT (6 Tests)

#### FV-024: Normal Indoor Lighting ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled  
**Steps**:
1. Verify in office lighting
2. Check verification success rate

**Expected Result**: Reliable verification  
**Test Data**: Normal light  
**Status**: ⏳ Not Run  

---

#### FV-025: Dark Environment ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled  
**Steps**:
1. Dim lighting to near darkness
2. Attempt verification
3. Check guidance/failure

**Expected Result**: Prompt for better light; no unsafe acceptance  
**Test Data**: Dark  
**Status**: ⏳ Not Run  

---

#### FV-026: Direct Bright Sunlight ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled  
**Steps**:
1. Verify in harsh sunlight
2. Check handling

**Expected Result**: Handle or request repositioning  
**Test Data**: Bright light  
**Status**: ⏳ Not Run  

---

#### FV-027: Shadow Across Face ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled  
**Steps**:
1. Create uneven facial shadow
2. Attempt verification
3. Check quality handling

**Expected Result**: Quality control requests correction if required  
**Test Data**: Uneven light/shadow  
**Status**: ⏳ Not Run  

---

#### FV-028: Moving Outdoor Background ✅
**Priority**: P2 | **Severity**: Minor  
**Preconditions**: Employee enrolled  
**Steps**:
1. Verify outdoors with moving background
2. Check robustness

**Expected Result**: Background must not bypass liveness/identity checks  
**Test Data**: Moving background  
**Status**: ⏳ Not Run  

---

### 5️⃣ POSITION (10 Tests)

#### FV-029: Face Too Close ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled  
**Steps**:
1. Move face extremely close to camera
2. Check feedback

**Expected Result**: Ask user to move back  
**Test Data**: Cropped face  
**Status**: ⏳ Not Run  

---

#### FV-030: Face Too Far ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled  
**Steps**:
1. Stand too far from camera
2. Check guidance

**Expected Result**: Ask user to move closer  
**Test Data**: Small face  
**Status**: ⏳ Not Run  

---

#### FV-031: Extreme Side Profile ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled  
**Steps**:
1. Turn to near-profile (~70°)
2. Check quality/angle response

**Expected Result**: Request front-facing pose/fail quality  
**Test Data**: Extreme pose  
**Status**: ⏳ Not Run  

---

#### FV-032: Eyes Closed ✅
**Priority**: P2 | **Severity**: Minor  
**Preconditions**: Employee enrolled  
**Steps**:
1. Keep eyes closed during capture
2. Check liveness/quality handling

**Expected Result**: Follow liveness/quality policy; request valid live capture  
**Test Data**: Eyes closed  
**Status**: ⏳ Not Run  

---

#### FV-033: Motion Blur ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Employee enrolled  
**Steps**:
1. Move rapidly during capture
2. Check frame rejection

**Expected Result**: Reject unusable frame  
**Test Data**: Blur  
**Status**: ⏳ Not Run  

---

#### FV-034: First-Time Permission Allowed ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Fresh install  
**Steps**:
1. Start verification
2. Allow camera permission when prompted
3. Check camera opens

**Expected Result**: Camera opens and flow continues  
**Test Data**: Permission Allow  
**Status**: ⏳ Not Run  

---

#### FV-035: Camera Permission Denied ✅
**Priority**: P0 | **Severity**: Major  
**Preconditions**: Permission undecided  
**Steps**:
1. Start verify
2. Deny permission
3. Check error handling

**Expected Result**: Explain requirement; no crash  
**Test Data**: Permission Deny  
**Status**: ⏳ Not Run  

---

#### FV-036: Permission Permanently Denied ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Previously permanently denied  
**Steps**:
1. Start verification
2. Check error message
3. Verify guidance to OS settings

**Expected Result**: Guide to OS settings  
**Test Data**: Permanent denial  
**Status**: ⏳ Not Run  

---

#### FV-037: Camera Unavailable/Busy ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Camera cannot initialize  
**Steps**:
1. Start verification
2. Check error message

**Expected Result**: Show recoverable error; no false submission  
**Test Data**: Camera busy  
**Status**: ⏳ Not Run  

---

#### FV-038: Front Camera Operation ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Supported device  
**Steps**:
1. Verify using front camera
2. Check preview/capture orientation

**Expected Result**: Preview/capture orientation correct  
**Test Data**: Front camera  
**Status**: ⏳ Not Run  

---

### 6️⃣ CAMERA OPERATIONS (3 Tests)

#### FV-039: App Backgrounded During Verification ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Verification active  
**Steps**:
1. Background app during verification
2. Return to app
3. Check secure pause/restart

**Expected Result**: Pause/restart securely; no stale capture  
**Test Data**: Lifecycle interruption  
**Status**: ⏳ Not Run  

---

#### FV-040: Offline Before Verification ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Device offline  
**Steps**:
1. Disable network
2. Start verification
3. Check error message

**Expected Result**: Show network error; no false success  
**Test Data**: No internet  
**Status**: ⏳ Not Run  

---

#### FV-041: Network Lost After Capture ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Request in progress  
**Steps**:
1. Capture successfully
2. Disable network during submission
3. Check failure/retry handling

**Expected Result**: Fail/retry idempotently; no duplicate attendance  
**Test Data**: Connection drop  
**Status**: ⏳ Not Run  

---

### 7️⃣ NETWORK/API (5 Tests)

#### FV-042: Very Slow Network ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Throttled connection  
**Steps**:
1. Set network throttle (low bandwidth)
2. Submit verification
3. Check timeout/progress handling

**Expected Result**: Progress/timeout handled; no duplicate requests  
**Test Data**: High latency  
**Status**: ⏳ Not Run  

---

#### FV-043: Verification API Timeout ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Timeout simulated  
**Steps**:
1. Submit verification
2. Simulate >60s timeout
3. Check non-success assumption

**Expected Result**: Do not assume success; allow safe retry  
**Test Data**: Timeout  
**Status**: ⏳ Not Run  

---

#### FV-044: Face Service 5xx Error ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Provider failure simulated  
**Steps**:
1. Submit verification when API returns 5xx
2. Check error display

**Expected Result**: Show technical error; no attendance  
**Test Data**: 5xx error  
**Status**: ⏳ Not Run  

---

#### FV-045: Repeated Verify Taps ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Screen active  
**Steps**:
1. Tap Verify button rapidly (5-10 times)
2. Check idempotency
3. Verify no duplicate submissions

**Expected Result**: Idempotency prevents duplicates  
**Test Data**: Duplicate requests  
**Status**: ⏳ Not Run  

---

### 8️⃣ ATTENDANCE (10 Tests)

#### FV-046: Clock-In After Successful Verification ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Eligible employee  
**Steps**:
1. Clock In button
2. Pass verification
3. Check record

**Expected Result**: Exactly one verified clock-in recorded  
**Test Data**: Valid employee  
**Status**: ⏳ Not Run  

---

#### FV-047: Clock-Out After Successful Verification ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Active session exists  
**Steps**:
1. Clock Out button
2. Pass verification
3. Check clock-out recorded

**Expected Result**: Exactly one clock-out recorded  
**Test Data**: Valid employee  
**Status**: ⏳ Not Run  

---

#### FV-048: Face Mismatch During Clock-In ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Employee tries wrong face  
**Steps**:
1. Start clock-in with different person's face
2. Check rejection

**Expected Result**: Block clock-in  
**Test Data**: Mismatch  
**Status**: ⏳ Not Run  

---

#### FV-049: Liveness Failure During Clock-Out ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Active session exists  
**Steps**:
1. Start clock-out
2. Fail liveness (spoof detected)
3. Check non-recording

**Expected Result**: Do not record verified clock-out  
**Test Data**: Spoof/failure  
**Status**: ⏳ Not Run  

---

#### FV-050: Employee Has No Registered Face ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Active but not enrolled  
**Steps**:
1. Attempt face verification when no enrollment exists
2. Check guidance/blocking

**Expected Result**: Block and guide to permitted enrollment  
**Test Data**: No enrollment  
**Status**: ⏳ Not Run  

---

#### FV-051: Inactive Employee ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Account inactive  
**Steps**:
1. Attempt verification with inactive account
2. Check rejection

**Expected Result**: Reject attendance/verification  
**Test Data**: Inactive account  
**Status**: ⏳ Not Run  

---

#### FV-052: Duplicate Clock-In ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Already clocked in  
**Steps**:
1. Verify and clock-in again while active
2. Check duplicate prevention

**Expected Result**: Prevent duplicate active clock-in  
**Test Data**: Active clock-in exists  
**Status**: ⏳ Not Run  

---

#### FV-053: Face Succeeds but Attendance Save Fails ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: DB/API failure simulated  
**Steps**:
1. Pass face verification
2. Simulate database failure
3. Check reconciliation/error

**Expected Result**: Do not claim completion; reconcile safely  
**Test Data**: Persistence error  
**Status**: ⏳ Not Run  

---

#### FV-054: Correct Employee Binding ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Two employees available  
**Steps**:
1. Verify Employee A
2. Inspect records
3. Verify only A's data recorded

**Expected Result**: All records reference A only  
**Test Data**: Employee A  
**Status**: ⏳ Not Run  

---

#### FV-055: Manual Admin Attendance Source ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Admin attendance enabled  
**Steps**:
1. Admin updates attendance without face
2. Check source recording
3. Verify not marked as face-verified

**Expected Result**: Record manual/admin source, not face-verified  
**Test Data**: Manual action  
**Status**: ⏳ Not Run  

---

### 9️⃣ SECURITY (7 Tests)

#### FV-056: Expired Auth Token ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Expired session  
**Steps**:
1. Wait for token expiration
2. Submit verification
3. Check rejection

**Expected Result**: Reject unauthorized request  
**Test Data**: Expired token  
**Status**: ⏳ Not Run  

---

#### FV-057: Tampered Employee ID ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Authorized security test  
**Steps**:
1. Login as Employee A
2. Alter request to reference Employee B
3. Check backend rejection

**Expected Result**: Backend rejects/binds to authorized identity  
**Test Data**: Cross-user tamper  
**Status**: ⏳ Not Run  

---

#### FV-058: Replay Successful Request ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Authorized security test  
**Steps**:
1. Save successful transaction
2. Replay prior request
3. Check prevention

**Expected Result**: Prevent old verification authorizing new attendance  
**Test Data**: Replay  
**Status**: ⏳ Not Run  

---

#### FV-059: Unauthorized Biometric Access ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Different roles/accounts  
**Steps**:
1. Login as different user
2. Attempt access to another employee's biometric
3. Check access denial

**Expected Result**: Deny access  
**Test Data**: Unauthorized account  
**Status**: ⏳ Not Run  

---

#### FV-060: Biometric Data in Logs ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: QA debug access  
**Steps**:
1. Perform verification
2. Inspect client/server logs
3. Check for raw biometric/secrets

**Expected Result**: No raw biometric/template/secrets in insecure logs  
**Test Data**: Normal attempt  
**Status**: ⏳ Not Run  

---

#### FV-061: Audit Trail Completeness ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Audit access  
**Steps**:
1. Run success and failure attempts
2. Inspect audit logs
3. Check event details

**Expected Result**: Record event time/result/context/transaction reference appropriately  
**Test Data**: Pass and fail  
**Status**: ⏳ Not Run  

---

#### FV-062: Verification Rate Limiting ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Policy configured  
**Steps**:
1. Send rapid failed attempts (10+ in 60s)
2. Check throttling

**Expected Result**: Throttle according to configured abuse policy  
**Test Data**: Burst failures  
**Status**: ⏳ Not Run  

---

### 🔟 UX/RECOVERY (9 Tests)

#### FV-063: User Cancels Verification ✅
**Priority**: P2 | **Severity**: Minor  
**Preconditions**: Screen active  
**Steps**:
1. Start verification
2. Click Cancel/Back
3. Check clean exit

**Expected Result**: Exit cleanly; no attendance  
**Test Data**: Cancellation  
**Status**: ⏳ Not Run  

---

#### FV-064: Understandable Failure Message ✅
**Priority**: P2 | **Severity**: Minor  
**Preconditions**: Failure can be triggered  
**Steps**:
1. Cause failure (mismatch/quality)
2. Read message
3. Verify clarity

**Expected Result**: Explain next action without exposing sensitive internals  
**Test Data**: Failure  
**Status**: ⏳ Not Run  

---

#### FV-065: Retry After Quality Failure ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: First attempt poor  
**Steps**:
1. Fail quality check
2. Correct and retry
3. Verify success

**Expected Result**: Retry succeeds without stale/duplicate state  
**Test Data**: Poor then good  
**Status**: ⏳ Not Run  

---

#### FV-066: App Killed Mid Submission ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Test environment  
**Steps**:
1. Pass face
2. Kill app during save
3. Relaunch and check state

**Expected Result**: Consistent final state; no duplicate punch  
**Test Data**: Mid-transaction termination  
**Status**: ⏳ Not Run  

---

#### FV-067: Device Rotation ✅
**Priority**: P2 | **Severity**: Minor  
**Preconditions**: Rotation supported/locked  
**Steps**:
1. Rotate device during verification
2. Check UI/overlay

**Expected Result**: No crash/bypass; overlay remains correct or stays locked  
**Test Data**: Orientation change  
**Status**: ⏳ Not Run  

---

#### FV-068: Verification Session Expires ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Screen left idle  
**Steps**:
1. Wait beyond session validity
2. Attempt submission
3. Check expiration handling

**Expected Result**: Require fresh capture/challenge  
**Test Data**: Expired session  
**Status**: ⏳ Not Run  

---

#### FV-069: Second Face Enters Frame ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Flow started with one face  
**Steps**:
1. Start with one face
2. Second person enters frame
3. Check ambiguity rejection

**Expected Result**: Reject ambiguous capture  
**Test Data**: Dynamic multiple faces  
**Status**: ⏳ Not Run  

---

#### FV-070: Call/OS Interruption ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Verification active  
**Steps**:
1. Interrupt with call or system dialog
2. Return to app
3. Check secure restart

**Expected Result**: Securely restart/resume; no stale submission  
**Test Data**: OS interruption  
**Status**: ⏳ Not Run  

---

### 1️⃣1️⃣ PERFORMANCE (2 Tests)

#### FV-071: Normal Response-Time Test ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Production-like environment  
**Steps**:
1. Perform 10 valid verifications
2. Measure duration
3. Check SLA compliance

**Expected Result**: Meet configured product SLA; UI responsive  
**Test Data**: Normal Wi-Fi/4G  
**Status**: ⏳ Not Run  

---

#### FV-072: Concurrent Verification Load ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Load-test environment  
**Steps**:
1. Run peak concurrent requests (10-20 simultaneous)
2. Monitor for errors/mix-ups
3. Check stability

**Expected Result**: Stable service; no cross-request identity/result mix  
**Test Data**: Peak concurrency  
**Status**: ⏳ Not Run  

---

### 1️⃣2️⃣ DATA INTEGRITY (2 Tests)

#### FV-073: Unique Transaction IDs ✅
**Priority**: P0 | **Severity**: Critical  
**Preconditions**: Multiple attempts  
**Steps**:
1. Review transaction IDs from multiple attempts
2. Check uniqueness
3. Verify attendance links

**Expected Result**: Unique traceability; attendance links only intended success  
**Test Data**: Pass/fail attempts  
**Status**: ⏳ Not Run  

---

#### FV-074: Trusted Date/Time ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Server and device time available  
**Steps**:
1. Verify with correct time
2. Alter device clock
3. Test again
4. Check timezone/time policy

**Expected Result**: Apply authoritative timezone/time policy consistently  
**Test Data**: Timestamp test  
**Status**: ⏳ Not Run  

---

### 1️⃣3️⃣ COMPATIBILITY (2 Tests)

#### FV-075: Supported Android Matrix ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: Supported Android devices available  
**Steps**:
1. Execute P0 test suite on each Android version
2. Test on different device classes
3. Check behavior consistency

**Expected Result**: Core flow behaves consistently  
**Test Data**: Android 8.0, 9, 10, 11, 12+  
**Status**: ⏳ Not Run  

---

#### FV-076: Supported iOS Matrix ✅
**Priority**: P1 | **Severity**: Major  
**Preconditions**: iOS in scope  
**Steps**:
1. Execute P0 suite on target iPhones
2. Test iOS versions (13+)
3. Check consistency

**Expected Result**: Core flow behaves consistently  
**Test Data**: iOS 13+  
**Status**: ⏳ Not Run  

---

## 📅 Test Execution Timeline

### Day 1: P0 Critical Tests (28 Tests)
**Duration**: 4-5 hours

| Time | Test | Expected |
|---|---|---|
| 09:00-10:00 | Enrollment (FV-001, 003, 006, 008) | 4 PASS |
| 10:00-11:00 | Face Match (FV-009, 015) | 2 PASS |
| 11:00-12:00 | Liveness (FV-016-020, 023) | 6 PASS |
| 12:00-13:00 | **LUNCH** | |
| 13:00-14:00 | Camera/Network (FV-035, 041, 045) | 3 PASS |
| 14:00-15:00 | Attendance (FV-046-053) | 8 PASS |
| 15:00-16:00 | Security (FV-056-060) | 5 PASS |
| 16:00-17:00 | Recovery/Performance (FV-066, 069, 072-073) | 4 PASS |

**Day 1 Target**: 28/28 PASS ✅

---

### Day 2-3: P1 Major Tests (40 Tests)
**Duration**: 6-8 hours each

- Enrollment tests (FV-002, 004, 005, 007)
- Face Match tests (FV-010-014)
- Liveness tests (FV-021, 022)
- Environment tests (FV-024-027)
- Position tests (FV-029-033)
- Camera tests (FV-034, 036-039)
- Network tests (FV-042-044)
- Attendance tests (FV-050, 055)
- Security tests (FV-061-062)
- Recovery tests (FV-063-065, 068, 070)
- Performance/Data/Compatibility (FV-071, 074-076)

**Day 2-3 Target**: 40/40 PASS ✅

---

### Day 4: P2 Minor Tests (8 Tests)
**Duration**: 2-3 hours

- Environment (FV-028)
- Position (FV-032)
- Recovery (FV-063-064, 067)
- Compatibility variations

**Day 4 Target**: 8/8 PASS ✅

---

## 🎯 Success Criteria

✅ **Phase 1 (P0)**: 28/28 = 100% PASS  
✅ **Phase 2 (P1)**: 40/40 = 100% PASS  
✅ **Phase 3 (P2)**: 8/8 = 100% PASS  
✅ **TOTAL**: 76/76 = 100% PASS

**Overall**: ✅ **READY FOR PRODUCTION**

---

## 📝 Test Execution Tracking

Use this template for each test:

```
Test ID: FV-XXX
Test Name: [Name]
Priority: [P0/P1/P2]
Date: [YYYY-MM-DD]
Tester: [Name]
Preconditions: ✅ Met
Steps Executed: [1-5]
Test Data Used: [Details]
Expected: [Result]
Actual: [Result]
Status: PASS / FAIL / BLOCKED
Defect ID: [If failed]
Remarks: [Any notes]
```

---

## ✅ Deliverables

After all tests:
1. ✅ Filled test matrix (76 tests)
2. ✅ Defect report (if any)
3. ✅ Performance metrics
4. ✅ Production readiness sign-off
5. ✅ Known issues & workarounds

---

**Ready to execute? Let's start testing! 🚀**

