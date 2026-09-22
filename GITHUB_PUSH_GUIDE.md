# 📤 GitHub Push Guide - Face Recognition API

## 🎯 Main Files to Push

### ✅ REQUIRED FILES (Must Include)

#### 1. **Core Application**
```
app_sface.py              ← Main FastAPI application (YuNet + SFace engine)
requirements.txt          ← Python dependencies
runtime.txt              ← Python version (for deployment)
procfile                 ← Heroku/AWS Elastic Beanstalk config
```

#### 2. **Configuration**
```
.gitignore               ← Git ignore rules
.elasticbeanstalk/
  └── config.yml         ← AWS Elastic Beanstalk config
.platform/
  └── nginx/
      └── conf.d/
          └── upload.conf ← Nginx upload size config
```

#### 3. **Pre-trained Models**
```
models/
  ├── face_detection_yunet_2023mar.onnx       ← YuNet detector (for face detection)
  ├── face_recognition_sface_2021dec.onnx     ← SFace recognizer (for face matching)
  └── face_attrib_net.onnx                    ← Attribute detector (for glasses detection)
```

#### 4. **Test Consoles (HTML)**
```
test_console_v2.html     ← Main test console (Step 1-2 workflows)
test_console.html        ← Simple UI (optional)
test_upload_only.html    ← Upload-only testing (optional)
```

---

### 📚 OPTIONAL BUT RECOMMENDED (Documentation)

#### Essential Docs
```
readme.md                          ← Main project documentation
QUICK_START.md                     ← Quick setup guide
SETUP_SFACE.md                     ← YuNet + SFace setup
API_READY.md                       ← API status
```

#### Testing Docs (For Users/Developers)
```
THRESHOLD_TESTING_GUIDE.md         ← How to test threshold
THRESHOLD_EXAMPLES.md              ← Real examples
COMPLETE_WORKFLOW.md               ← Full workflow guide
QUICK_TEST_CHECKLIST.md            ← Testing checklist
```

#### Technical Docs (Reference)
```
FACE_DETECTION_FIX.md              ← Face detection details
EYES_OPEN_VALIDATION.md            ← Eyes validation logic
FINAL_VALIDATION_REPORT.md         ← Validation details
```

---

### ❌ DO NOT PUSH (Remove Before Push)

#### Build/Runtime Files
```
__pycache__/                       ← Python cache (add to .gitignore)
*.pyc                              ← Compiled Python files
*.pyo                              ← Python optimized files
.Python                            ← Virtual environment
venv/                              ← Virtual environment folder
env/                               ← Virtual environment folder
```

#### Logs
```
server-8001.err.log                ← Error logs
server-8001.out.log                ← Output logs
*.log                              ← All log files
```

#### Temporary Files
```
temp/                              ← Temporary files (clear before push)
stored_images/                     ← Test images (optional - remove or .gitignore)
```

#### Old/Duplicate Code
```
app.py                             ← Old version (use app_sface.py instead)
test_eyes_detection.py             ← Test script (optional)
download_models.py                 ← Download script (optional - docs only)
```

#### Misc Documentation (Optional - Remove if Cluttered)
```
CHANGES_MADE.md
COMPARISON_TEST_GUIDE.md
ISSUE_RESOLVED.md
TEST_CASE_NO_REFERENCE.md
TEST_ERROR_HANDLING.md
... (all other temporary docs)
```

---

## 📦 Clean File Structure for GitHub

```
FaceRecognitionAPI/
├── app_sface.py                        ✅ MAIN APPLICATION
├── requirements.txt                    ✅ DEPENDENCIES
├── runtime.txt                         ✅ PYTHON VERSION
├── procfile                            ✅ DEPLOYMENT CONFIG
├── .gitignore                          ✅ GIT IGNORE
│
├── models/                             ✅ PRE-TRAINED MODELS
│   ├── face_detection_yunet_2023mar.onnx
│   ├── face_recognition_sface_2021dec.onnx
│   └── face_attrib_net.onnx
│
├── .elasticbeanstalk/
│   └── config.yml                      ✅ AWS CONFIG
│
├── .platform/nginx/conf.d/
│   └── upload.conf                     ✅ NGINX CONFIG
│
├── test_console_v2.html                ✅ TEST CONSOLE
├── test_console.html                   ⚠️ OPTIONAL
├── test_upload_only.html               ⚠️ OPTIONAL
│
├── readme.md                           ✅ MAIN DOCS
├── QUICK_START.md                      ✅ SETUP GUIDE
├── SETUP_SFACE.md                      ✅ ENGINE SETUP
├── THRESHOLD_TESTING_GUIDE.md          ✅ TESTING GUIDE
├── COMPLETE_WORKFLOW.md                ✅ WORKFLOW
│
└── .git/                               ✅ GIT HISTORY
```

---

## 🚀 Step-by-Step GitHub Push

### Step 1: Clean Up Project
```bash
# Remove temporary files
rm -r __pycache__
rm *.log
rm -r temp/*
rm stored_images/*.jpg
rm stored_images/*.png

# OR on Windows PowerShell:
Remove-Item -Recurse -Force __pycache__
Remove-Item *.log
Remove-Item -Recurse temp/*
```

### Step 2: Verify .gitignore
```
# Create/update .gitignore file:
__pycache__/
*.pyc
*.pyo
*.egg-info/
.Python
venv/
env/
.env
*.log
temp/
stored_images/
.DS_Store
```

### Step 3: Stage Files
```bash
# Add main files
git add app_sface.py
git add requirements.txt
git add runtime.txt
git add procfile
git add readme.md
git add QUICK_START.md
git add SETUP_SFACE.md
git add .gitignore

# Add models
git add models/

# Add configs
git add .elasticbeanstalk/
git add .platform/

# Add test consoles
git add test_console_v2.html
git add test_console.html

# Add docs
git add THRESHOLD_TESTING_GUIDE.md
git add THRESHOLD_EXAMPLES.md
git add COMPLETE_WORKFLOW.md
```

### Step 4: Create Commit
```bash
git commit -m "Face Recognition API - YuNet+SFace with liveness detection

Features:
- YuNet face detection + SFace face recognition
- Strict liveness validation with eye detection
- Reference image requirement for face comparison
- Threshold-based face matching (0-100)
- Head turn challenge validation
- Glasses/eyewear detection
- REST API with JSON responses
- Test console for all workflows

Endpoints:
- POST /faceLiveness - Check if face is live
- POST /employeeFaceCompare - Compare two faces
- POST /uploadImage - Store reference image
- GET /dev/stored-images - List stored images
- GET /docs - API documentation

Models:
- YuNet (2023) for face detection
- SFace (2021) for face recognition
- Attribute detector for glasses/eyewear

Testing:
- test_console_v2.html - Full workflow testing
- Threshold testing guide included
- Complete workflow documentation"
```

### Step 5: Push to GitHub
```bash
git push origin main

# Or if creating new branch:
git push -u origin feature/face-recognition-api
```

---

## 📋 Pre-Push Checklist

- [ ] **app_sface.py** - Main application ready
- [ ] **requirements.txt** - All dependencies listed
- [ ] **runtime.txt** - Python version specified
- [ ] **procfile** - Deployment config ready
- [ ] **models/** - All 3 ONNX files present
- [ ] **.gitignore** - Properly configured
- [ ] **readme.md** - Documentation complete
- [ ] **test_console_v2.html** - Latest version
- [ ] **No log files** - Deleted all *.log files
- [ ] **No __pycache__** - Cleaned cache
- [ ] **No stored_images** - Cleared test images
- [ ] **Models size** - Check file sizes
- [ ] **Git status clean** - Run `git status`

---

## ⚠️ Common Issues & Solutions

### Issue 1: Models Too Large
**Problem**: Git complains "file too large" for ONNX models
**Solution**: 
- Use Git LFS (Large File Storage)
  ```bash
  git lfs install
  git lfs track "*.onnx"
  git add .gitattributes
  git add models/
  ```

### Issue 2: __pycache__ Still Showing
**Problem**: Python cache files included
**Solution**:
```bash
git rm -r --cached __pycache__
echo "__pycache__/" >> .gitignore
git add .gitignore
git commit -m "Remove __pycache__"
```

### Issue 3: Log Files Committed
**Problem**: Large log files included
**Solution**:
```bash
git rm --cached *.log
echo "*.log" >> .gitignore
git add .gitignore
git commit -m "Remove log files"
```

---

## 📊 File Sizes Reference

**Expected Sizes**:
- app_sface.py: ~50 KB
- face_detection_yunet_2023mar.onnx: ~7.1 MB
- face_recognition_sface_2021dec.onnx: ~6.6 MB
- face_attrib_net.onnx: ~1.4 MB
- test_console_v2.html: ~50 KB
- Requirements.txt: ~2 KB

**Total**: ~15-20 MB (reasonable for GitHub)

---

## 🎯 GitHub Repo README Template

```markdown
# Face Recognition API - YuNet + SFace

Advanced face recognition API with strict liveness detection, built on OpenCV's YuNet face detector and SFace recognizer.

## Features

✅ Real-time face detection (YuNet 2023)
✅ Face recognition & matching (SFace 2021)
✅ Strict liveness validation (eye detection, replay detection)
✅ Threshold-based matching (customizable 0-100)
✅ Head turn challenge validation
✅ Glasses/eyewear detection
✅ Reference image requirement
✅ REST API with JSON responses
✅ Web-based test console

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Download models:
   ```bash
   python download_models.py
   ```

3. Start server:
   ```bash
   python app_sface.py
   ```

4. Open test console:
   ```
   http://localhost:8001/test_console_v2.html
   ```

## API Endpoints

- `POST /faceLiveness` - Check if face is live
- `POST /employeeFaceCompare` - Compare two faces
- `POST /uploadImage` - Store reference image
- `GET /docs` - Swagger documentation

## Configuration

- Liveness threshold: 0.5 (configurable)
- Face match threshold: 70 (0-100, customizable)
- Minimum face size: 200x200px or 15% of image
- Maximum face deviation: ±25% from center

## Documentation

- [QUICK_START.md](QUICK_START.md) - Setup guide
- [THRESHOLD_TESTING_GUIDE.md](THRESHOLD_TESTING_GUIDE.md) - Threshold testing
- [COMPLETE_WORKFLOW.md](COMPLETE_WORKFLOW.md) - Full workflow

## License

[Your License]

## Author

[Your Name]
```

---

## 🎯 Next Steps

1. **Clean up** the project directory
2. **Update .gitignore**
3. **Create GitHub repo**
4. **Push code** using steps above
5. **Add README** with project info
6. **Share link** for collaboration

---

## ✅ Ready to Push?

Use this command to verify:
```bash
git status
```

Should show only main files, not logs or cache.

**Then push:**
```bash
git push origin main
```

Done! 🚀
