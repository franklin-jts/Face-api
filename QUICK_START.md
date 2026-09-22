# 🚀 Quick Start — YuNet+SFace Face Recognition API

## 3 Steps to Run

### Step 1: Download Models (~5-10 minutes)
```bash
python download_models.py
```

**What it does:**
- Downloads YuNet face detector (~26 MB)
- Downloads SFace recognizer (~110 MB)
- Saves to `models/` directory

**Status:**
```
✓ face_detection_yunet_2023mar.onnx downloaded
✓ face_recognition_sface_2021dec.onnx downloaded
```

### Step 2: Start the Server
```bash
python app_sface.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Application startup complete.
✓ YuNet detector loaded successfully
✓ SFace recognizer loaded successfully
```

### Step 3: Test It
**Option A: Use Test Console (Recommended)**
- Open browser: http://localhost:8001/test_console.html
- Upload images or use camera
- Click "Check Liveness" or "Compare Faces"

**Option B: Use cURL**
```bash
curl http://localhost:8001/health \
  -H "Authorization: Bearer secret-token-123"
```

---

## Test Console Features

### 🎯 Face Liveness
1. Upload an image (or use camera)
2. Click "Check Liveness"
3. Get response: `liveness_passed: true/false`

### 🔄 Face Compare
1. Upload reference image (file1)
2. Upload/capture live image (file2)
3. Set threshold (default: 70)
4. Click "Compare Faces"
5. Get: `face_match`, `match_score`, `liveness_passed`

---

## API Response Examples

### Liveness Check
```json
{
  "status": true,
  "message": "Liveness check passed",
  "data": {
    "liveness_passed": true,
    "liveness_score": 0.82,
    "liveness_reason": "liveness_passed",
    "spoof_detected": false,
    "face_detected": true,
    "faces_count": 1,
    "capture_id": "a1b2c3d4e5f6g7h8",
    "captured_at_utc": "2026-09-18T16:42:47Z",
    "store_db": false,
    "db_status": "not_stored"
  }
}
```

### Face Compare
```json
{
  "status": true,
  "message": "Face recognition successful",
  "data": {
    "face_match": true,
    "match_score": 85.5,
    "liveness_passed": true,
    "liveness_score": 0.78,
    "challenge_passed": true,
    "challenge_reason": "turn_detected",
    "challenge_yaw_delta": 18.5,
    "challenge_similarity": 85.5
  }
}
```

---

## Auth Token

Default: `secret-token-123`

Change in `.env`:
```
AUTH_TOKEN=your-secret-token-here
```

All requests require:
```
Authorization: Bearer secret-token-123
```

---

## Troubleshooting

### "Models not found" error?
```bash
python download_models.py
```

### "Port 8001 already in use"?
Edit `app_sface.py` (last line):
```python
uvicorn.run("app_sface:app", host="0.0.0.0", port=8002)  # Change 8001 to 8002
```

### "Models still loading"?
Check status:
```bash
curl http://localhost:8001/health -H "Authorization: Bearer secret-token-123"
```

Look for:
```json
{
  "models": {
    "detector_ready": true,
    "recognizer_ready": true
  }
}
```

---

## Performance

- **Model Size:** 136 MB (vs 159 MB InsightFace)
- **License:** MIT + Apache 2.0 (✅ Commercial safe)
- **Embedding:** 512 dimensions
- **Speed:** Similar to original
- **Accuracy:** High (YuNet optimized for real-world)

---

## All Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Check server & models status |
| POST | `/uploadImage` | Upload reference face |
| POST | `/employeeFaceCompare` | Compare two faces |
| POST | `/faceLiveness` | Check if face is live |
| GET | `/dev/test-image` | Get stored reference (dev) |
| POST | `/dev/reset-cache` | Clear cache (dev) |
| GET | `/dev/conditions-info` | Show config (dev) |
| GET | `/test_console.html` | Test console UI |

---

## Next: Deploy to Production

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python download_models.py
CMD ["python", "app_sface.py"]
```

### Elastic Beanstalk
Same setup — run `download_models.py` before deployment.

---

## Support

- Full API docs: http://localhost:8001/docs
- Swagger UI: http://localhost:8001/redoc
- Issues: Check logs in terminal

---

**Ready?** Start with: `python download_models.py` 🚀
