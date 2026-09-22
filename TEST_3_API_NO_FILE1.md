# TEST 3: API Direct Call - Missing file1 Parameter

## 🎯 Test Objective
Verify that the `/employeeFaceCompare` API endpoint properly validates and rejects requests when the reference image (file1) parameter is missing.

---

## 📋 Test Prerequisites

### Required:
- [ ] API server running on port 8001
- [ ] At least one test image file
- [ ] curl or Postman installed
- [ ] Valid auth token: `secret-token-123`

### Prepare Test Image:
1. Find any image file on your computer (JPEG or PNG)
2. Note the full path (example: `C:\Users\KITS\Downloads\test_image.jpg`)
3. You'll use this as `file2` (live capture)

---

## 🔧 TEST METHOD 1: Using PowerShell (Windows)

### Command:
```powershell
$imagePath = "C:\path\to\your\image.jpg"
$token = "secret-token-123"

$form = @{
    file2 = Get-Item -Path $imagePath
}

$headers = @{
    "Authorization" = "Bearer $token"
}

$response = Invoke-RestMethod `
    -Uri "http://localhost:8001/employeeFaceCompare" `
    -Method Post `
    -Form $form `
    -Headers $headers

$response | ConvertTo-Json
```

### Step-by-Step Execution:

1. **Open PowerShell:**
   - Press: `Win + R`
   - Type: `powershell`
   - Press: `Enter`

2. **Navigate to test image directory:**
   ```powershell
   cd C:\Users\KITS\Downloads
   ```

3. **Run the command:**
   ```powershell
   $imagePath = "C:\Users\KITS\Downloads\test_image.jpg"
   $token = "secret-token-123"
   
   $form = @{
       file2 = Get-Item -Path $imagePath
   }
   
   $headers = @{
       "Authorization" = "Bearer $token"
   }
   
   $response = Invoke-RestMethod `
       -Uri "http://localhost:8001/employeeFaceCompare" `
       -Method Post `
       -Form $form `
       -Headers $headers
   
   $response | ConvertTo-Json
   ```

4. **Observe output**

---

## 🔧 TEST METHOD 2: Using curl (Git Bash / Command Line)

### Command:
```bash
curl -X POST http://localhost:8001/employeeFaceCompare \
  -H "Authorization: Bearer secret-token-123" \
  -F "file2=@C:/path/to/your/image.jpg"
```

### Step-by-Step Execution:

1. **Open Command Prompt or Git Bash:**
   - Windows: `cmd` or Git Bash
   - Navigate to image directory

2. **Run curl command:**
   ```bash
   curl -X POST http://localhost:8001/employeeFaceCompare ^
     -H "Authorization: Bearer secret-token-123" ^
     -F "file2=@C:\Users\KITS\Downloads\test_image.jpg"
   ```
   
   Note: On Windows cmd, use `^` to continue lines

3. **Observe output**

---

## 🔧 TEST METHOD 3: Using Postman (GUI - Easiest)

### Steps:

1. **Open Postman**
2. **Create New Request:**
   - Method: `POST`
   - URL: `http://localhost:8001/employeeFaceCompare`

3. **Add Headers Tab:**
   - Key: `Authorization`
   - Value: `Bearer secret-token-123`

4. **Add Body Tab:**
   - Select: `form-data`
   - Key: `file2`
   - Type: Select dropdown → `File`
   - Value: Click "Select Files" → choose your test image
   - **DO NOT add file1** (this is the point of the test)

5. **Click Send**

6. **Observe Response**

---

## ✅ EXPECTED RESPONSE

### Status Code:
```
400 Bad Request
```

### Response Body:
```json
{
  "detail": "❌ Reference image not provided. Please upload reference image first using 'Store Reference' button."
}
```

---

## 📋 Validation Checklist

### Response Status:
- [ ] Status code is `400` (not 500, not 200)
- [ ] Error response (not success response)
- [ ] Error is `Bad Request` type

### Response Content:
- [ ] Message mentions "Reference image"
- [ ] Message mentions "not provided"
- [ ] Message suggests "Store Reference" button
- [ ] Message is clear and user-friendly
- [ ] No technical jargon

### Error Quality:
- [ ] Error message is actionable
- [ ] User knows what to do next
- [ ] Error is not a generic 500 error
- [ ] Error helps user understand requirement

---

## 🔍 Detailed Response Analysis

### Good Response (✅ PASS):
```json
{
  "detail": "❌ Reference image not provided. Please upload reference image first using 'Store Reference' button."
}
```
- ✅ Clear message
- ✅ Explains what's missing
- ✅ Suggests how to fix
- ✅ User-friendly tone

### Bad Response (❌ FAIL):

**Generic Error:**
```json
{
  "detail": "Invalid request"
}
```
- ❌ Not descriptive
- ❌ Doesn't say what's missing
- ❌ User doesn't know what to do

**Technical Error:**
```json
{
  "detail": "KeyError: 'file1'"
}
```
- ❌ Technical jargon
- ❌ Confusing to user
- ❌ Not helpful

**500 Server Error:**
```json
{
  "detail": "Internal server error"
}
```
- ❌ Should be 400 (client error, not server error)
- ❌ Indicates bug in code
- ❌ Not validation, but failure

---

## 📊 Test Results Template

```
TEST 3: API Direct Call - Missing file1

Date: 2026-09-21
Test Method: [ ] PowerShell [ ] curl [ ] Postman

=== REQUEST ===
Method: POST
URL: http://localhost:8001/employeeFaceCompare
Headers: Authorization: Bearer secret-token-123
Body: file2=@image.jpg (NO file1)

=== RESPONSE ===
Status Code: _____ (Expected: 400)
Error Message: _____

=== VALIDATION ===
[ ] Status code is 400
[ ] Message mentions "Reference image"
[ ] Message is clear and helpful
[ ] No 500 error
[ ] No technical jargon

=== RESULT ===
[✓] PASS - Proper error handling
[ ] FAIL - Incorrect error response

Error Message Quality:
[ ] ✅ Excellent - Clear, actionable
[ ] ⚠️ Good - Understands but could be better
[ ] ❌ Poor - Confusing or unhelpful

NOTES:
_____________________
_____________________
```

---

## 🔄 Compare with TEST 1

### TEST 1 (Frontend Validation):
```
User clicks Compare without reference
↓
Alert shows: "STEP 1 Required: Please upload..."
↓
NO API call made
```

### TEST 3 (Backend Validation):
```
API request sent WITHOUT file1 parameter
↓
API receives request
↓
API checks for file1
↓
file1 is missing
↓
Returns 400 error: "Reference image not provided..."
↓
Error message helps user understand requirement
```

**Both levels of validation working** = ✅ **GOOD DESIGN**

---

## 🧪 Extended Testing

### TEST 3a: Missing file1 AND file2
```bash
curl -X POST http://localhost:8001/employeeFaceCompare \
  -H "Authorization: Bearer secret-token-123"
  
# No file1, no file2, no images at all
```

**Expected:** Should get error about file1 (checked first)

### TEST 3b: Missing file1 only
```bash
curl -X POST http://localhost:8001/employeeFaceCompare \
  -H "Authorization: Bearer secret-token-123" \
  -F "file2=@image.jpg"
  
# Has file2, but missing file1
```

**Expected:** Error about missing file1 (this is TEST 3)

### TEST 3c: Missing file2 only (for comparison)
```bash
curl -X POST http://localhost:8001/employeeFaceCompare \
  -H "Authorization: Bearer secret-token-123" \
  -F "file1=@image.jpg"
  
# Has file1, but missing file2
```

**Expected:** Error about missing file2 (same pattern, different parameter)

---

## 🎯 Success Criteria

TEST 3 PASSES if:
- [ ] API returns 400 status code (not 500)
- [ ] Error message is clear and helpful
- [ ] Error mentions "Reference image"
- [ ] Error suggests "Store Reference"
- [ ] User knows what to do next

TEST 3 FAILS if:
- [ ] API returns 200 (accepted bad request)
- [ ] API returns 500 (server crashed)
- [ ] Error message is confusing
- [ ] No error message provided
- [ ] User doesn't understand what's wrong

---

## 📝 Quick Reference Commands

### PowerShell (one-liner):
```powershell
Invoke-RestMethod -Uri "http://localhost:8001/employeeFaceCompare" -Method Post -Form @{file2=(Get-Item "C:\path\to\image.jpg")} -Headers @{"Authorization"="Bearer secret-token-123"} | ConvertTo-Json
```

### curl (one-liner):
```bash
curl -X POST http://localhost:8001/employeeFaceCompare -H "Authorization: Bearer secret-token-123" -F "file2=@C:\path\to\image.jpg"
```

### Postman:
1. New request
2. POST to: `http://localhost:8001/employeeFaceCompare`
3. Header: `Authorization: Bearer secret-token-123`
4. Body → form-data → file2 = [select image file]
5. Send

---

## 🎬 Execute This Test Now

Choose your preferred method (PowerShell, curl, or Postman) and run the test. Report:
- [ ] Status code received
- [ ] Error message received
- [ ] Is it clear and helpful?
- [ ] Did validation work?

**TEST 3 = API Backend Validation ✅**
