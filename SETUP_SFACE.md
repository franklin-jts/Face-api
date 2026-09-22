# Face Recognition API (YuNet + SFace) — Setup Guide

## Quick Start

### 1. Download Models
```bash
python download_models.py
```

This downloads:
- ✅ **face_detection_yunet_2023mar.onnx** (~26 MB) — Face detection
- ✅ **face_recognition_sface_2021dec.onnx** (~110 MB) — Face recognition

**Total: ~136 MB** (vs ~159 MB for InsightFace)

Models are saved to `models/` directory.

### 2. Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

Ensure you have:
- `opencv-python-headless` (already in requirements.txt)
- `onnxruntime` (already in requirements.txt)
- `fastapi`
- `uvicorn`
- `numpy`

### 3. Start the App
```bash
python app_sface.py
```

Server runs on: **http://0.0.0.0:8001**

### 4. Test Console
Open in browser: **http://localhost:8001/test_console.html**

## API Endpoints

### `/health` — Health Check
```bash
curl http://localhost:8001/health
```

Returns model status and timestamp.

### `/uploadImage` (POST) — Upload Reference
```bash
curl -X POST http://localhost:8001/uploadImage \
  -H "Authorization: Bearer secret-token-123" \
  -F "reference=@photo.jpg"
```

### `/employeeFaceCompare` (POST) — Compare Two Faces
```bash
curl -X POST http://localhost:8001/employeeFaceCompare \
  -H "Authorization: Bearer secret-token-123" \
  -F "file1=@ref.jpg" \
  -F "file2=@probe.jpg" \
  -F "threshold=70"
```

### `/faceLiveness` (POST) — Check Liveness
```bash
curl -X POST http://localhost:8001/faceLiveness \
  -H "Authorization: Bearer secret-token-123" \
  -F "capture=@photo.jpg" \
  -F "store_db=false"
```

### Dev Endpoints
- **GET /dev/test-image** — Retrieve stored reference image
- **POST /dev/reset-cache** — Clear replay detection cache
- **GET /dev/conditions-info** — Show current config & thresholds

## Authentication
All endpoints require Bearer token in header:
```
Authorization: Bearer secret-token-123
```

Change default token in `.env`:
```
AUTH_TOKEN=your-secure-token-here
```

## Test Console Features
- ✅ File upload or camera capture
- ✅ Real-time JSON responses
- ✅ Image previews
- ✅ Liveness detection
- ✅ Face comparison with threshold

## Troubleshooting

### Models Not Downloading?
Download manually:
1. https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
2. https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx

Place both in `models/` directory.

### Port Already in Use?
Modify `app_sface.py`:
```python
if __name__ == "__main__":
    uvicorn.run("app_sface:app", host="0.0.0.0", port=8002, reload=True)
```

### Models Ready Check
```bash
curl http://localhost:8001/health
```

Look for: `"detector_ready": true, "recognizer_ready": true`

## Performance Notes
- **Model size:** ~136 MB (lighter than InsightFace)
- **License:** MIT (YuNet) + Apache 2.0 (SFace) — commercial safe
- **Detection:** YuNet (optimized for speed & accuracy)
- **Recognition:** SFace (512-dim embedding, cosine similarity)
- **Liveness:** Confidence + replay detection heuristics

## Comparison with Original (InsightFace)
| Feature | Original | YuNet+SFace |
|---------|----------|------------|
| Engine | InsightFace buffalo_s | YuNet + SFace |
| Model Size | ~159 MB | ~136 MB |
| License | Proprietary | MIT + Apache 2.0 |
| Commercial Use | ⚠️ License check needed | ✅ Safe |
| Embedding Dim | 512 | 512 |
| Speed | Baseline | Similar/Faster |
| API Contract | Identical | **Identical** |

## Running Both Versions
You can run both simultaneously:
- Original: `python app.py` (port 8000)
- New: `python app_sface.py` (port 8001)

They share the same `/temp` folder but keep separate replay caches.

## Integration with Flutter/Mobile
The JSON response structure is **identical** to the original app.py:
- Same field names
- Same HTTP status codes
- Same error messages

**No client-side changes needed!**

## Next Steps
1. ✅ Download models: `python download_models.py`
2. ✅ Start app: `python app_sface.py`
3. ✅ Open test console: http://localhost:8001/test_console.html
4. ✅ Deploy to production (EB, Docker, etc.)

---

**Questions?** Check `/docs` endpoint for auto-generated Swagger UI.
