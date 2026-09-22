# 🚀 Git Commands Cheat Sheet - Push to GitHub

## 1️⃣ Initial Setup (One Time)

### Check if Git is installed
```bash
git --version
```

### Configure Git (First time only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"
```

### Create GitHub Repository
1. Go to https://github.com/new
2. Enter repository name: `FaceRecognitionAPI`
3. Add description: `Face Recognition API with YuNet+SFace and liveness detection`
4. Choose public or private
5. Click "Create repository"
6. You'll get a link: `https://github.com/your-username/FaceRecognitionAPI.git`

---

## 2️⃣ Clean Up Project (Before Push)

### On PowerShell (Windows)
```powershell
# Navigate to project folder
cd d:\new\FaceRecognitionAPI

# Delete log files
Remove-Item *.log

# Delete __pycache__
Remove-Item -Recurse -Force __pycache__

# Clear temp folder
Remove-Item -Recurse temp\*

# Check status
git status
```

### On Bash/Linux/Mac
```bash
# Navigate to project folder
cd /path/to/FaceRecognitionAPI

# Delete log files
rm *.log

# Delete __pycache__
rm -rf __pycache__

# Clear temp folder
rm -rf temp/*

# Check status
git status
```

---

## 3️⃣ Stage Files for Commit

### Option A: Add Individual Files
```bash
# Add main application
git add app_sface.py

# Add dependencies
git add requirements.txt
git add runtime.txt
git add procfile

# Add configuration
git add .gitignore
git add .elasticbeanstalk/
git add .platform/

# Add models
git add models/

# Add test console
git add test_console_v2.html

# Add documentation
git add readme.md
git add QUICK_START.md
git add SETUP_SFACE.md
```

### Option B: Add Everything Except Ignored Files (Recommended)
```bash
# This adds all files EXCEPT those in .gitignore
git add .
```

### Check What's Staged
```bash
# See staged files
git status

# See detailed changes
git diff --cached
```

---

## 4️⃣ Commit Changes

### Create Commit
```bash
# Simple commit message
git commit -m "Add Face Recognition API"

# Detailed commit message
git commit -m "Add Face Recognition API - YuNet+SFace

- Implement face detection using YuNet
- Implement face recognition using SFace
- Add strict liveness validation
- Add eye detection and head turn challenge
- Add glasses/eyewear detection
- Add reference image requirement
- Create test console web UI
- Add comprehensive documentation"
```

### View Commit Log
```bash
# See recent commits
git log

# See last 5 commits
git log -n 5

# See with one-line format
git log --oneline
```

---

## 5️⃣ Connect to GitHub

### First Time: Add Remote Repository

**If GitHub shows:**
```
git remote add origin https://github.com/your-username/FaceRecognitionAPI.git
git branch -M main
git push -u origin main
```

**Then run exactly that:**
```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR-USERNAME/FaceRecognitionAPI.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Check Remote Connection
```bash
# See connected remotes
git remote -v

# Should show:
# origin  https://github.com/your-username/FaceRecognitionAPI.git (fetch)
# origin  https://github.com/your-username/FaceRecognitionAPI.git (push)
```

---

## 6️⃣ Push to GitHub

### Push Main Branch
```bash
# First push (sets up tracking)
git push -u origin main

# Subsequent pushes
git push

# Push specific branch
git push origin main
```

### Push Specific Files Only
```bash
# Add and push specific file
git add app_sface.py
git commit -m "Update API"
git push
```

---

## 🔄 Common Workflows

### Complete Push Workflow
```bash
# 1. Check current status
git status

# 2. Add all files
git add .

# 3. Commit with message
git commit -m "Initial commit - Face Recognition API"

# 4. Push to GitHub
git push -u origin main

# 5. Verify on GitHub
# Go to https://github.com/your-username/FaceRecognitionAPI
```

### Update After Making Changes
```bash
# 1. Make changes to files
# (edit app_sface.py, etc.)

# 2. Check what changed
git status

# 3. Add changes
git add .

# 4. Commit
git commit -m "Fix eye detection threshold"

# 5. Push
git push
```

### Push Models Separately (If Size Issue)
```bash
# Add only models
git add models/
git commit -m "Add pre-trained ONNX models"
git push

# Or add other files
git add app_sface.py
git commit -m "Add main application"
git push
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: Authentication Failed
**Error**: `fatal: Authentication failed for 'https://github.com/...'`

**Solution**:
```bash
# Use SSH instead of HTTPS
# First generate SSH key (if don't have)
# Then update remote:
git remote set-url origin git@github.com:YOUR-USERNAME/FaceRecognitionAPI.git
git push
```

**OR use Personal Access Token:**
```bash
# Use your GitHub token as password when prompted
# Windows: Create token at https://github.com/settings/tokens
```

### Issue 2: File Too Large
**Error**: `error: GH001: Large files detected`

**Solution**:
```bash
# Use Git LFS for large files
git lfs install
git lfs track "*.onnx"
git add .gitattributes models/
git commit -m "Use Git LFS for models"
git push
```

### Issue 3: Already Exists on GitHub
**Error**: `Repository already exists`

**Solution**:
```bash
# Use existing repository
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/FaceRecognitionAPI.git
git push -u origin main
```

### Issue 4: Need to Pull First
**Error**: `error: failed to push some refs to 'origin'`

**Solution**:
```bash
# Pull changes first
git pull origin main

# Then push
git push
```

### Issue 5: Unwanted Files Committed
**Error**: `__pycache__` or logs included

**Solution**:
```bash
# Remove from git (but keep local file)
git rm --cached __pycache__
git rm --cached *.log

# Add to .gitignore
echo "__pycache__/" >> .gitignore
echo "*.log" >> .gitignore

# Commit
git commit -m "Remove cache and logs"
git push
```

---

## 📋 Complete Step-by-Step Example

### From Start to Push

**Step 1: Navigate to project**
```bash
cd d:\new\FaceRecognitionAPI
```

**Step 2: Check git status**
```bash
git status
```

**Step 3: Clean up (if needed)**
```powershell
Remove-Item *.log
Remove-Item -Recurse -Force __pycache__
```

**Step 4: Add files**
```bash
git add .
```

**Step 5: Check what's staged**
```bash
git status
```

**Step 6: Create commit**
```bash
git commit -m "Face Recognition API - YuNet+SFace with liveness

Core Features:
- Face detection & recognition
- Strict liveness validation
- Eye detection
- Head turn challenge
- Glasses detection
- Reference image requirement
- Web test console
- Complete documentation"
```

**Step 7: Add GitHub remote (first time only)**
```bash
git remote add origin https://github.com/YOUR-USERNAME/FaceRecognitionAPI.git
git branch -M main
```

**Step 8: Push to GitHub**
```bash
git push -u origin main
```

**Step 9: Verify on GitHub**
```
Go to: https://github.com/YOUR-USERNAME/FaceRecognitionAPI
```

✅ **Done!**

---

## 🎯 Quick Reference Commands

```bash
# Status
git status                    # Current status

# Add/Stage
git add .                     # Add all files
git add file.py              # Add specific file

# Commit
git commit -m "message"       # Create commit

# Push
git push                      # Push to GitHub
git push -u origin main       # First push

# Pull
git pull                      # Get latest from GitHub

# Remote
git remote -v                 # Show remote URLs
git remote add origin URL     # Add GitHub URL

# History
git log                       # Show commit history
git log --oneline            # One-line history

# Undo
git reset HEAD~1             # Undo last commit (keep changes)
git revert HEAD              # Revert last commit
git checkout -- file.py      # Undo changes to file
```

---

## 💡 Best Practices

1. **Always clean before push**
   ```bash
   Remove-Item *.log
   Remove-Item -Recurse __pycache__
   ```

2. **Write good commit messages**
   ```bash
   ❌ git commit -m "fix"
   ✅ git commit -m "Fix eye detection threshold from 2.2 to 2.5"
   ```

3. **Commit frequently**
   - Make small, logical commits
   - Not one giant commit at the end

4. **Pull before pushing**
   ```bash
   git pull
   git push
   ```

5. **Check status regularly**
   ```bash
   git status
   ```

---

## ✅ Ready to Push?

1. Clean up: Remove logs and cache
2. Stage files: `git add .`
3. Commit: `git commit -m "..."`
4. Push: `git push -u origin main`

That's it! 🚀

---

## 📞 Need Help?

- GitHub Docs: https://docs.github.com
- Git Docs: https://git-scm.com/doc
- My Project: `d:\new\FaceRecognitionAPI`

**Now go push your code!** 💪
