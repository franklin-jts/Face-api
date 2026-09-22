# 💾 Local Image Storage Guide

## Overview

Uploaded images are now **stored locally** on disk in the `stored_images/` folder with timestamps.

**Storage Location:** `d:\new\FaceRecognitionAPI\stored_images\`

---

## How It Works

### Upload Flow

1. **User uploads image** via API or test console
2. **Image is saved to two locations:**
   - `temp/reference.jpg` (temporary, used for comparison)
   - `stored_images/reference_YYYYMMDD_HHMMSS.jpg` (permanent storage)

3. **Response includes storage details:**
```json
{
  "status": true,
  "message": "Reference image uploaded and stored successfully",
  "data": {
    "registered": true,
    "file_size": 125000,
    "storage_path": "stored_images/reference_20260918_170527.jpg",
    "storage_filename": "reference_20260918_170527.jpg",
    "updated_at_utc": "2026-09-18T17:05:27Z"
  }
}
```

---

## New API Endpoints

### List All Stored Images

**GET** `/dev/stored-images`

```bash
curl http://localhost:8001/dev/stored-images \
  -H "Authorization: Bearer secret-token-123"
```

**Response:**
```json
{
  "status": true,
  "message": "Found 3 stored images",
  "data": {
    "count": 3,
    "storage_folder": "stored_images",
    "images": [
      {
        "filename": "reference_20260918_170527.jpg",
        "size": 125000,
        "created_at_utc": "2026-09-18T17:05:27Z",
        "path": "stored_images/reference_20260918_170527.jpg"
      },
      {
        "filename": "reference_20260918_171043.jpg",
        "size": 130000,
        "created_at_utc": "2026-09-18T17:10:43Z",
        "path": "stored_images/reference_20260918_171043.jpg"
      }
    ]
  }
}
```

---

### Download Stored Image

**GET** `/dev/stored-images/{filename}`

```bash
curl http://localhost:8001/dev/stored-images/reference_20260918_170527.jpg \
  -H "Authorization: Bearer secret-token-123" \
  -o downloaded_image.jpg
```

Returns the image file (binary data).

---

### Check Storage Info

**GET** `/dev/conditions-info`

```bash
curl http://localhost:8001/dev/conditions-info \
  -H "Authorization: Bearer secret-token-123"
```

**Response (relevant part):**
```json
{
  "data": {
    "storage": {
      "folder": "stored_images",
      "stored_images_count": 3,
      "storage_size_bytes": 375000,
      "storage_size_mb": 0.38
    }
  }
}
```

---

## Directory Structure

```
d:\new\FaceRecognitionAPI\
├── stored_images/                          ← NEW: Permanent storage
│   ├── reference_20260918_170527.jpg
│   ├── reference_20260918_171043.jpg
│   └── reference_20260918_173215.jpg
├── temp/                                   ← Temporary working folder
│   └── reference.jpg                       ← Current active reference
├── models/
│   ├── face_detection_yunet_2023mar.onnx
│   └── face_recognition_sface_2021dec.onnx
├── app_sface.py
├── test_console.html
├── test_console_v2.html
└── ...
```

---

## Testing Locally Stored Images

### Via Test Console V2

1. **Open:** http://localhost:8001/test_console_v2.html
2. **Step 1: Store Reference Image**
   - Upload image
   - Click "💾 Upload & Store Reference"
   - Response shows: `storage_path: "stored_images/reference_YYYYMMDD_HHMMSS.jpg"`

3. **Step 2a/2b: Test Liveness/Comparison**
   - Uses both stored images and new captures
   - Stored images persist across tests

### View Stored Images

```bash
# List all stored
curl http://localhost:8001/dev/stored-images \
  -H "Authorization: Bearer secret-token-123"

# Check storage stats
curl http://localhost:8001/dev/conditions-info \
  -H "Authorization: Bearer secret-token-123" | grep -A 5 '"storage"'

# Download specific image
curl http://localhost:8001/dev/stored-images/reference_20260918_170527.jpg \
  -H "Authorization: Bearer secret-token-123" \
  -o my_image.jpg
```

---

## Filename Format

**Pattern:** `reference_YYYYMMDD_HHMMSS.(jpg|png)`

**Example:** `reference_20260918_143025.jpg`

- `YYYY` = Year (2026)
- `MM` = Month (09)
- `DD` = Day (18)
- `HH` = Hour (14)
- `MM` = Minute (30)
- `SS` = Second (25)

Each upload gets a **unique timestamp** → **No overwrites!**

---

## Storage Features

✅ **Automatic timestamping** - Each upload gets unique filename
✅ **Persistent storage** - Images remain after server restart
✅ **Easy retrieval** - List and download endpoints
✅ **Storage monitoring** - Check size and count
✅ **Security** - Path traversal protection on downloads
✅ **Local access** - Direct file system access

---

## Cleanup & Management

### Manual Cleanup

**Delete old stored images:**
```powershell
# Delete all stored images
Remove-Item .\stored_images\* -Force

# Delete specific image
Remove-Item .\stored_images\reference_20260918_170527.jpg
```

### Clear Cache & Storage

**POST** `/dev/reset-cache`

```bash
curl -X POST http://localhost:8001/dev/reset-cache \
  -H "Authorization: Bearer secret-token-123"
```

This:
- Clears replay detection cache
- Deletes `temp/reference.jpg`
- **Does NOT delete** `stored_images/` (permanent storage)

---

## API Usage Examples

### Upload & Store

```bash
curl -X POST http://localhost:8001/uploadImage \
  -H "Authorization: Bearer secret-token-123" \
  -F "reference=@photo.jpg"
```

**Returns:**
```json
{
  "storage_path": "stored_images/reference_20260918_143025.jpg",
  "storage_filename": "reference_20260918_143025.jpg"
}
```

### List Stored

```bash
curl http://localhost:8001/dev/stored-images \
  -H "Authorization: Bearer secret-token-123" | python -m json.tool
```

### Download Stored

```bash
curl http://localhost:8001/dev/stored-images/reference_20260918_143025.jpg \
  -H "Authorization: Bearer secret-token-123" \
  --output retrieved_image.jpg
```

### Check Storage Size

```bash
curl http://localhost:8001/dev/conditions-info \
  -H "Authorization: Bearer secret-token-123" | \
  python -c "import sys, json; print(json.load(sys.stdin)['data']['storage'])"
```

**Output:**
```json
{
  "folder": "stored_images",
  "stored_images_count": 5,
  "storage_size_bytes": 625000,
  "storage_size_mb": 0.63
}
```

---

## For Flutter Integration

### Android/iOS Implementation

```dart
// 1. Upload image
POST /uploadImage
  → Returns: storage_path, storage_filename, file_size

// 2. Use storage filename for later retrieval
GET /dev/stored-images/{filename}
  → Download image if needed

// 3. Test liveness on stored
POST /faceLiveness
  (Uses current active reference)

// 4. Compare with stored
POST /employeeFaceCompare
  file1: reference (stored)
  file2: capture (new from camera)
```

---

## Monitoring & Debugging

### Check what's stored

```bash
# List files in stored_images
dir stored_images

# Show file sizes
Get-ChildItem .\stored_images\ -Recurse | Select-Object Name, Length
```

### Monitor storage growth

```bash
# Check storage folder size
(Get-ChildItem .\stored_images\ -Recurse | Measure-Object -Property Length -Sum).Sum
```

### API health check

```bash
curl http://localhost:8001/health \
  -H "Authorization: Bearer secret-token-123"
```

---

## ✅ Checklist

- [x] Images stored in `stored_images/` folder
- [x] Timestamped filenames prevent overwrites
- [x] List endpoint to view all stored images
- [x] Download endpoint to retrieve images
- [x] Storage stats in conditions-info
- [x] Permanent storage (survives server restarts)
- [x] Test console integration ready

---

## Status

**✅ Local image storage fully implemented and ready!**

- Upload images
- Automatically stored with timestamps
- Retrieve anytime
- Use for testing
- Persistent storage

---

## Next Steps

1. **Upload images** via test console
2. **View stored** images: GET `/dev/stored-images`
3. **Test liveness** on stored
4. **Compare** with new captures
5. **Download** anytime: GET `/dev/stored-images/{filename}`

**Example Workflow:**
```
1. Upload john_doe.jpg
   → Saved as: stored_images/reference_20260918_143025.jpg
2. Check what's stored
   → curl /dev/stored-images
3. Test liveness
   → POST /faceLiveness (uses active reference)
4. Compare with camera
   → POST /employeeFaceCompare (file1=stored, file2=camera)
5. Download for verification
   → GET /dev/stored-images/reference_20260918_143025.jpg
```

Ready to use! 🚀
