import os
import cv2
import numpy as np
import onnxruntime as ort
import base64
import hashlib
from datetime import datetime, timedelta
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Body, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio
from dotenv import load_dotenv
import logging
from collections import deque
from typing import Dict, Tuple, Optional
from pathlib import Path

# ==============================
# Logging Configuration
# ==============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# ==============================
# Load .env variables
# ==============================
load_dotenv()
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "secret-token-123")

app = FastAPI(title="Face Compare API (YuNet + SFace)")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (test_console.html)
static_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ==============================
# Constants & Temp Folder
# ==============================
TEMP_FOLDER = "temp"
STORAGE_FOLDER = "stored_images"  # NEW: Store uploaded images
os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(STORAGE_FOLDER, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_FORMATS = ["image/jpeg", "image/png"]

# Liveness & replay detection
RECENT_LIVE_HASHES = deque(maxlen=50)  # Track recent live frames
LIVENESS_THRESHOLD = 0.5
TURN_CHALLENGE_YAW_MIN = 15.0
BRIGHTNESS_THRESHOLD = 50
MOTION_THRESHOLD = 0.05

# ==============================
# Load YuNet + SFace Models
# ==============================
logger.info("Loading YuNet face detector and SFace recognizer...")

DETECTOR_MODEL = "models/face_detection_yunet_2023mar.onnx"
RECOGNIZER_MODEL = "models/face_recognition_sface_2021dec.onnx"
ATTRIBUTE_MODEL = "models/face_attrib_net.onnx"

try:
    # Create detector
    detector = cv2.FaceDetectorYN.create(
        model=DETECTOR_MODEL,
        config="",
        input_size=(320, 320),
        score_threshold=0.6,  # REDUCED from 0.9 - more sensitive
        nms_threshold=0.3,
        top_k=5000,
    )
    logger.info("✓ YuNet detector loaded successfully")
except Exception as e:
    logger.warning(f"✗ Failed to load YuNet detector: {e}")
    logger.warning(f"  Download models using: python download_models.py")
    detector = None

try:
    # Create recognizer
    recognizer = cv2.FaceRecognizerSF.create(
        model=RECOGNIZER_MODEL,
        config="",
    )
    logger.info("✓ SFace recognizer loaded successfully")
except Exception as e:
    logger.warning(f"✗ Failed to load SFace recognizer: {e}")
    logger.warning(f"  Download models using: python download_models.py")
    recognizer = None

try:
    attribute_session = ort.InferenceSession(ATTRIBUTE_MODEL, providers=["CPUExecutionProvider"])
except Exception as e:
    logger.warning(f"Failed to load face attribute model: {e}")
    attribute_session = None

def get_glasses_attributes(image_bytes: bytes) -> Optional[Dict[str, float]]:
    """Return local AI probabilities for eyeglasses and sunglasses."""
    if attribute_session is None:
        return None
    image, faces = detect_faces(image_bytes)
    if image is None or faces is None or len(faces) == 0:
        return None
    face = faces[np.argmax([item[2] * item[3] for item in faces])]
    x, y, w, h = [int(value) for value in face[:4]]
    crop = image[max(0, y):max(0, y + h), max(0, x):max(0, x + w)]
    if crop.size == 0:
        return None
    crop = cv2.cvtColor(cv2.resize(crop, (128, 128)), cv2.COLOR_BGR2RGB)
    tensor = np.transpose(crop.astype(np.float32) / 255.0, (2, 0, 1))[None, ...]
    probabilities = attribute_session.run(None, {"image": tensor})[0][0]
    return {"eyeglasses": float(probabilities[2]), "sunglasses": float(probabilities[4])}

# ==============================
# Helper: Base64 to bytes
# ==============================
def base64_to_bytes(data: str) -> bytes:
    """Convert base64 string (with or without data URL prefix) to bytes."""
    if data.startswith("data:image/jpeg;base64,"):
        data = data.replace("data:image/jpeg;base64,", "")
    elif data.startswith("data:image/png;base64,"):
        data = data.replace("data:image/png;base64,", "")
    return base64.b64decode(data)

# ==============================
# File validation helper
# ==============================
def validate_file(file_bytes: bytes, content_type: str):
    """Validate file size and format."""
    if content_type not in ALLOWED_FORMATS:
        raise HTTPException(status_code=400, detail="Only JPEG or PNG images allowed")
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10 MB")

# ==============================
# Token verification helper
# ==============================
def verify_token(request: Request):
    """Verify Authorization Bearer token."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing token")

# ==============================
# Detect faces using YuNet
# ==============================
def detect_faces(image_bytes: bytes) -> Tuple[Optional[cv2.Mat], Optional[np.ndarray]]:
    """
    Detect faces in image using YuNet.
    Returns (image, detections) where detections shape is (N, 15)
    Each row: [x1, y1, w, h, x_re, y_re, x_le, y_le, x_n, y_n, x_rm, y_rm, x_lm, y_lm, confidence]
    """
    try:
        np_img = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if img is None:
            logger.warning("Failed to decode image")
            return None, None

        if detector is None:
            logger.warning("Detector not initialized")
            return img, None

        # Resize for detection - YuNet works better with larger images
        h, w = img.shape[:2]
        
        # If image is too small, upscale it
        if h < 320 or w < 320:
            scale = max(320 / h, 320 / w)
            new_w = int(w * scale)
            new_h = int(h * scale)
            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            logger.info(f"Upscaled image from {w}x{h} to {new_w}x{new_h}")
            h, w = new_h, new_w
        
        detector.setInputSize((w, h))
        
        # OpenCV YuNet returns (face_count, faces).  The landmark rows are
        # always the second tuple item.
        result = detector.detect(img)
        
        # Handle different return types
        if result is None:
            logger.warning("Detector returned None")
            return img, None
        
        if isinstance(result, tuple):
            detections = result[1]
        else:
            detections = result
        
        # Ensure detections is ndarray and handle empty case
        if detections is None or (isinstance(detections, np.ndarray) and len(detections) == 0):
            logger.warning("No faces detected in image")
            return img, np.empty((0, 15), dtype=np.float32)
        
        # Make sure detections is 2D array
        if isinstance(detections, np.ndarray):
            if len(detections.shape) == 1:
                detections = detections.reshape(1, -1)
            logger.info(f"Detected {len(detections)} faces")
            return img, detections
        
        return img, None
    except Exception as e:
        logger.exception(f"Error detecting faces: {e}")
        return None, None

# ==============================
# Extract face embeddings using SFace
# ==============================
def get_embedding(image_bytes: bytes) -> Optional[np.ndarray]:
    """
    Extract face embedding from image using SFace.
    Returns normalized embedding or None if no face detected.
    """
    try:
        img, detections = detect_faces(image_bytes)
        if img is None or detections is None:
            logger.warning("No faces detected")
            return None
        
        if len(detections) == 0:
            logger.warning("No faces detected")
            return None

        if recognizer is None:
            logger.warning("Recognizer not initialized")
            return None

        # Use largest detected face
        faces = detections
        largest_idx = np.argmax([f[2] * f[3] for f in faces])
        face = faces[largest_idx]

        # SFace requires an aligned crop; YuNet provides five landmarks.
        face_roi = recognizer.alignCrop(img, face)
        if face_roi is None or face_roi.size == 0:
            return None

        embedding = recognizer.feature(face_roi)
        if embedding is None or len(embedding) == 0:
            return None

        # Normalize embedding
        embedding = embedding.astype(np.float32).flatten()
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return embedding
    except Exception as e:
        logger.exception(f"Error extracting embedding: {e}")
        return None

# ==============================
# Compare embeddings (cosine similarity)
# ==============================
def compare_faces(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """
    Compare two embeddings using cosine similarity.
    Returns score as percentage (0-100).
    """
    try:
        # Ensure both are 1D
        emb1 = emb1.flatten()
        emb2 = emb2.flatten()
        
        # Cosine similarity
        similarity = float(np.dot(emb1, emb2))
        score = round(similarity * 100, 2)
        return max(0.0, min(100.0, score))
    except Exception as e:
        logger.exception(f"Error comparing faces: {e}")
        return 0.0

# ==============================
# Estimate yaw from facial landmarks
# ==============================
def estimate_yaw_proxy(image_bytes: bytes) -> Optional[float]:
    """
    Estimate head yaw angle using facial landmarks.
    Returns yaw angle in degrees (positive = right, negative = left).
    """
    try:
        img, detections = detect_faces(image_bytes)
        if img is None or detections is None or len(detections) == 0:
            return None

        faces = detections
        # Get largest face
        largest_idx = np.argmax([f[2] * f[3] for f in faces])
        face = faces[largest_idx]

        # Extract landmarks (eye centers)
        right_eye = np.array([face[4], face[5]])  # x_re, y_re
        left_eye = np.array([face[6], face[7]])   # x_le, y_le
        nose = np.array([face[8], face[9]])       # x_n, y_n

        # Simple yaw estimation: eye line rotation relative to nose
        eye_center = (right_eye + left_eye) / 2
        eye_vector = right_eye - left_eye
        nose_vector = nose - eye_center

        # Calculate angle
        if np.linalg.norm(eye_vector) > 0 and np.linalg.norm(nose_vector) > 0:
            cos_angle = np.dot(eye_vector, nose_vector) / (
                np.linalg.norm(eye_vector) * np.linalg.norm(nose_vector)
            )
            cos_angle = np.clip(cos_angle, -1, 1)
            yaw = np.degrees(np.arccos(cos_angle))
            # Determine direction
            if nose_vector[0] < 0:
                yaw = -yaw
            return round(yaw, 2)

        return 0.0
    except Exception as e:
        logger.exception(f"Error estimating yaw: {e}")
        return None

# ==============================
# Correct white balance (lighting normalization)
# ==============================
def correct_white_balance(image: cv2.Mat) -> cv2.Mat:
    """Apply white balance correction."""
    try:
        result = cv2.cvtColor(image, cv2.COLOR_BGR2LAB).astype(np.float32)
        avg_a = np.mean(result[:, :, 1])
        avg_b = np.mean(result[:, :, 2])
        result[:, :, 1] -= ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] -= ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result = np.clip(result, 0, 255).astype(np.uint8)
        result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
        return result
    except Exception as e:
        logger.warning(f"White balance correction failed: {e}")
        return image

# ==============================
# Enhance low light images
# ==============================
def enhance_low_light(image: cv2.Mat) -> cv2.Mat:
    """Apply contrast limited adaptive histogram equalization (CLAHE)."""
    try:
        if len(image.shape) == 3:
            # Convert to HSV, enhance V channel
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            hsv[:, :, 2] = clahe.apply((hsv[:, :, 2] * 255).astype(np.uint8))
            hsv = np.clip(hsv, 0, 255).astype(np.uint8)
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        else:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            return clahe.apply(image)
    except Exception as e:
        logger.warning(f"Low light enhancement failed: {e}")
        return image

# ==============================
# Normalize lighting
# ==============================
def normalize_lighting(image_bytes: bytes) -> np.ndarray:
    """Normalize lighting in image."""
    try:
        np_img = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if img is None:
            return None

        # Apply white balance correction
        img = correct_white_balance(img)

        # Check brightness
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)

        if brightness < BRIGHTNESS_THRESHOLD:
            img = enhance_low_light(img)

        return img
    except Exception as e:
        logger.warning(f"Lighting normalization failed: {e}")
        return None

# ==============================
# Check if frame is replayed (screen replay detection)
# ==============================
def _is_replayed_frame(image_bytes: bytes) -> bool:
    """
    Detect if frame is likely a screen replay/photograph.
    Uses hash-based detection: if identical/very similar frame recently seen, likely replay.
    """
    try:
        frame_hash = hashlib.md5(image_bytes).hexdigest()

        # Check if hash recently seen
        for recent_hash in RECENT_LIVE_HASHES:
            if recent_hash == frame_hash:
                logger.warning("Replay detection: frame hash found in recent history")
                return True

        # Add to history
        RECENT_LIVE_HASHES.append(frame_hash)
        return False
    except Exception as e:
        logger.warning(f"Replay detection failed: {e}")
        return False

# ==============================
# Evaluate liveness
# ==============================
def evaluate_liveness(image_bytes: bytes) -> Tuple[bool, float, str]:
    """
    Evaluate if image shows a live face.
    Returns (is_live, score, reason).
    """
    try:
        # Detect face FIRST (don't check replay yet)
        img, detections = detect_faces(image_bytes)
        if img is None or detections is None or len(detections) == 0:
            return False, 0.0, "no_face_detected"

        faces = detections
        # Clock-in quality gate: require one usable, forward-facing whole face.
        largest_face = faces[np.argmax([f[2] * f[3] for f in faces])]
        x, y, w, h = [float(value) for value in largest_face[:4]]
        image_h, image_w = img.shape[:2]
        confidence = float(largest_face[-1])
        face_ratio = (w * h) / float(image_h * image_w)

        # YuNet landmarks: right eye, left eye, nose.
        right_eye = np.array([largest_face[4], largest_face[5]], dtype=float)
        left_eye = np.array([largest_face[6], largest_face[7]], dtype=float)
        nose = np.array([largest_face[8], largest_face[9]], dtype=float)
        eye_midpoint = (right_eye + left_eye) / 2.0
        eye_distance = float(np.linalg.norm(right_eye - left_eye))
        eye_tilt = abs(float(np.degrees(np.arctan2(left_eye[1] - right_eye[1], left_eye[0] - right_eye[0]))))
        nose_offset = abs(float(nose[0] - eye_midpoint[0])) / max(eye_distance, 1.0)

        fully_in_frame = x >= 8 and y >= 8 and x + w <= image_w - 8 and y + h <= image_h - 8
        
        # NEW: Check for eyes open (detect eye closure) - MOVED TO PRIORITY #1
        # Eyes detected at landmarks: right_eye [4,5], left_eye [6,7]
        # If eyes are very close together or missing, likely closed
        
        # STRICTER: Calculate eye aspect ratio to detect closed eyes
        # If eyes are closed, the y-distance between eyes becomes very small
        eye_vertical_distance = abs(right_eye[1] - left_eye[1])
        
        # VERY STRICT: Minimum vertical distance between eyes must be at least 10px
        # When eyes are closed, this drops to ~2-5px
        if eye_vertical_distance < 10.0:
            eyes_open = False
        else:
            eye_aspect_ratio = eye_distance / max(eye_vertical_distance, 1.0)
            # MUCH STRICTER: Eyes open requires
            # 1. Eye distance >= 30px (increased from 25)
            # 2. Aspect ratio >= 2.5 (increased from 2.2) 
            # BOTH conditions must be true
            eyes_open = eye_distance >= 30.0 and eye_aspect_ratio >= 2.5
        
        # Log eye detection for debugging
        logger.info(f"Eyes detection: distance={eye_distance:.1f}, vertical={eye_vertical_distance:.1f}, open={eyes_open}")
        
        large_enough = face_ratio >= 0.15 and w >= 200 and h >= 200  # STRICTER: 15% of image, 200x200px minimum
        centred = abs((x + w / 2.0) - image_w / 2.0) <= image_w * 0.25  # Face must be centered (not edges)
        facing_camera = eye_tilt <= 10.0 and nose_offset <= 0.18  # STRICTER: straighter face required

        if not fully_in_frame:
            return False, confidence, "whole_face_not_visible"
        if not eyes_open:  # PRIORITY #1: Check eyes are open FIRST
            return False, confidence, "eyes_closed_or_not_detected"
        if not large_enough:
            return False, confidence, "move_closer_to_camera"
        if not centred:
            return False, confidence, "centre_your_face"
        if not facing_camera:
            return False, confidence, "look_straight_at_camera"
        if confidence < 0.75:  # STRICTER: higher confidence threshold
            return False, confidence, "low_face_detection_confidence"

        # LAST: Check for replay/spoof (after all other checks)
        if _is_replayed_frame(image_bytes):
            return False, 0.3, "replay_detected"

        return True, confidence, "liveness_passed"
    except Exception as e:
        logger.exception(f"Error evaluating liveness: {e}")
        return False, 0.0, "error"

# ==============================
# Evaluate turn challenge
# ==============================
def evaluate_turn_challenge(
    initial_bytes: bytes,
    challenge_bytes: bytes,
    min_yaw_delta: float = TURN_CHALLENGE_YAW_MIN,
) -> Tuple[bool, float, str]:
    """
    Evaluate if user turned their head sufficiently.
    Returns (challenge_passed, yaw_delta, reason).
    """
    try:
        yaw_initial = estimate_yaw_proxy(initial_bytes)
        yaw_challenge = estimate_yaw_proxy(challenge_bytes)

        if yaw_initial is None or yaw_challenge is None:
            return False, 0.0, "landmark_detection_failed"

        yaw_delta = abs(yaw_challenge - yaw_initial)

        passed = bool(yaw_delta >= min_yaw_delta)
        reason = "turn_detected" if passed else "insufficient_turn"

        return passed, float(round(yaw_delta, 2)), reason
    except Exception as e:
        logger.exception(f"Error evaluating turn challenge: {e}")
        return False, 0.0, "error"

# ==============================
# ENDPOINTS
# ==============================

# ==============================
# Serve Test Console
# ==============================
@app.get("/test_console.html")
async def serve_test_console():
    """Serve the test console HTML file."""
    return FileResponse(Path(__file__).parent / "test_console.html")

@app.get("/test_console_v2.html")
async def serve_test_console_v2():
    """Serve the advanced test console HTML file."""
    return FileResponse(Path(__file__).parent / "test_console_v2.html")

@app.get("/test_upload_only.html")
async def serve_test_upload_only():
    """Serve the upload-only test console (no camera)."""
    return FileResponse(Path(__file__).parent / "test_upload_only.html")

# ==============================
# Health Check
# ==============================
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": True,
        "message": "Service is running",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "models": {
            "detector_ready": detector is not None,
            "recognizer_ready": recognizer is not None,
        },
    }

@app.post("/faceSkeleton")
async def face_skeleton(request: Request, capture: UploadFile = File(...)):
    """Return a lightweight YuNet landmark skeleton drawn on an image."""
    verify_token(request)
    image_bytes = await capture.read()
    validate_file(image_bytes, capture.content_type)
    image, detections = detect_faces(image_bytes)
    if image is None or detections is None or len(detections) == 0:
        return JSONResponse(status_code=400, content={
            "status": False, "message": "No face detected. Face the camera with your whole face visible.", "data": {}
        })

    face = detections[np.argmax([item[2] * item[3] for item in detections])]
    overlay = image.copy()
    points = [(int(face[index]), int(face[index + 1])) for index in range(4, 14, 2)]
    # eye-to-eye, eyes-to-nose, nose-to-mouth: a compact face triangle guide.
    for start, end in ((0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4)):
        cv2.line(overlay, points[start], points[end], (0, 255, 0), 2)
    for point in points:
        cv2.circle(overlay, point, 5, (0, 0, 255), -1)
    ok, encoded = cv2.imencode(".jpg", overlay)
    if not ok:
        raise HTTPException(status_code=500, detail="Unable to create skeleton image")
    return {
        "status": True,
        "message": "Face skeleton detected",
        "data": {"skeleton_image_base64": "data:image/jpeg;base64," + base64.b64encode(encoded.tobytes()).decode("ascii")},
    }

# ==============================
# Upload Reference Image
# ==============================
@app.post("/uploadImage")
async def upload_reference(reference: UploadFile = File(...), request: Request = None):
    """Upload reference image and store locally."""
    try:
        verify_token(request)

        try:
            contents = await asyncio.wait_for(reference.read(), timeout=60)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=408, detail="Error: Timeout. Try uploading again")

        validate_file(contents, reference.content_type)

        # Save to both temp and storage folders
        file_path_temp = os.path.join(TEMP_FOLDER, "reference.jpg")
        
        # Generate unique filename for storage
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file_ext = ".jpg" if reference.content_type == "image/jpeg" else ".png"
        storage_filename = f"reference_{timestamp}{file_ext}"
        file_path_storage = os.path.join(STORAGE_FOLDER, storage_filename)
        
        # Write to both locations
        with open(file_path_temp, "wb") as f:
            f.write(contents)
        
        with open(file_path_storage, "wb") as f:
            f.write(contents)

        file_size = len(contents)
        now = datetime.utcnow()

        logger.info(f"Reference image uploaded: {file_size} bytes")
        logger.info(f"Stored locally at: {file_path_storage}")

        return {
            "status": True,
            "message": "Reference image uploaded and stored successfully",
            "data": {
                "registered": True,
                "faces_count": 1,
                "file_size": file_size,
                "updated_at_utc": now.isoformat() + "Z",
                "storage_path": file_path_storage,
                "storage_filename": storage_filename,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error in upload_reference")
        raise HTTPException(status_code=500, detail="Internal server error")

# ==============================
# Compare Employee Face
# ==============================
@app.post("/employeeFaceCompare")
async def compare(
    request: Request,
    file1: UploadFile = File(None),
    file2: UploadFile = File(None),
    threshold: float = Body(70, embed=True),
    file1_base64: str = Body(None),
    file2_base64: str = Body(None),
):
    """
    Compare two faces: file1 vs file2 using cosine similarity.
    Returns face_match, match_score, and liveness/challenge info.
    """
    try:
        logger.info("---- Face Compare API Called (YuNet+SFace) ----")

        verify_token(request)
        logger.info("Token verified")

        # ==============================
        # FILE 1
        # ==============================
        if file1_base64:
            try:
                bytes1 = base64_to_bytes(file1_base64)
                validate_file(bytes1, "image/jpeg")
                logger.info("File1 received via base64")
            except Exception as e:
                logger.exception("Invalid base64 data for file1")
                raise HTTPException(status_code=400, detail="Invalid base64 data for file1")

        elif file1 is not None:
            try:
                bytes1 = await asyncio.wait_for(file1.read(), timeout=60)
                validate_file(bytes1, file1.content_type)
                logger.info("File1 received via upload")
            except asyncio.TimeoutError:
                logger.error("Timeout while reading file1")
                raise HTTPException(status_code=408, detail="Error: Timeout for file1. Try again")
        else:
            logger.error("file1 not provided")
            raise HTTPException(status_code=400, detail="❌ Reference image not provided. Please upload reference image first using 'Store Reference' button.")

        emb1 = get_embedding(bytes1)
        logger.info("File1 embedding extracted")

        # ==============================
        # FILE 2
        # ==============================
        if file2_base64:
            try:
                bytes2 = base64_to_bytes(file2_base64)
                validate_file(bytes2, "image/jpeg")
                logger.info("File2 received via base64")
            except Exception as e:
                logger.exception("Invalid base64 data for file2")
                raise HTTPException(status_code=400, detail="Invalid base64 data for file2")

        elif file2 is not None:
            try:
                bytes2 = await asyncio.wait_for(file2.read(), timeout=60)
                validate_file(bytes2, file2.content_type)
                logger.info("File2 received via upload")
            except asyncio.TimeoutError:
                logger.error("Timeout while reading file2")
                raise HTTPException(status_code=408, detail="Error: Timeout for file2. Try again")
        else:
            logger.error("file2 not provided")
            raise HTTPException(status_code=400, detail="❌ Live capture image not provided. Please capture image from camera using 'Use Camera' button.")

        emb2 = get_embedding(bytes2)
        logger.info("File2 embedding extracted")

        # ==============================
        # Face validation
        # ==============================
        if emb1 is None or emb2 is None:
            logger.warning("Face detection failed in one or more images")
            return JSONResponse(
                status_code=400,
                content={
                    "status": False,
                    "message": "Face recognition not successful",
                    "data": {
                        "face_match": False,
                        "match_score": 0.0,
                        "liveness_passed": False,
                        "liveness_score": 0.0,
                        "challenge_passed": False,
                        "challenge_reason": "no_face_detected",
                        "challenge_yaw_delta": 0.0,
                        "challenge_similarity": 0.0,
                    },
                },
            )

        # ==============================
        # Compare embeddings
        # ==============================
        final_score = compare_faces(emb1, emb2)
        final_match = bool(final_score >= threshold)

        # Eyewear is an independent AI attribute check. A face can still be
        # the same person with glasses on, but this workflow requires the
        # reference and live eyewear state to agree.
        reference_attributes = get_glasses_attributes(bytes1)
        live_attributes = get_glasses_attributes(bytes2)
        glasses_validation_available = reference_attributes is not None and live_attributes is not None
        reference_glasses = None
        live_glasses = None
        glasses_match = None
        glasses_reason = "glasses_validation_unavailable"
        if glasses_validation_available:
            reference_glasses = bool(
                reference_attributes["eyeglasses"] >= 0.50 or reference_attributes["sunglasses"] >= 0.50
            )
            live_glasses = bool(
                live_attributes["eyeglasses"] >= 0.50 or live_attributes["sunglasses"] >= 0.50
            )
            glasses_match = reference_glasses == live_glasses
            glasses_reason = "glasses_match" if glasses_match else "glasses_mismatch"
            final_match = bool(final_match and glasses_match)

        # Evaluate liveness on file2 (probe image)
        is_live, liveness_score, liveness_reason = evaluate_liveness(bytes2)

        # Evaluate turn challenge
        challenge_passed, yaw_delta, challenge_reason = evaluate_turn_challenge(bytes1, bytes2)

        logger.info(
            f"Match: {final_match} (score={final_score}), "
            f"Liveness: {is_live}, "
            f"Challenge: {challenge_passed} (yaw_delta={yaw_delta})"
        )

        return {
            "status": bool(final_match),
            "message": (
                "Face recognition successful"
                if final_match
                else "Face validation failed: eyewear does not match the reference"
                if glasses_validation_available and glasses_match is False
                else "Face recognition not successful"
            ),
            "data": {
                "face_match": bool(final_match),
                "match_score": float(final_score),
                "liveness_passed": bool(is_live),
                "liveness_score": round(float(liveness_score), 3),
                "challenge_passed": bool(challenge_passed),
                "challenge_reason": challenge_reason,
                "challenge_yaw_delta": float(yaw_delta),
                "challenge_similarity": float(round(final_score, 2)),
                "reference_glasses": reference_glasses,
                "live_glasses": live_glasses,
                "glasses_match": glasses_match,
                "glasses_validation_reason": glasses_reason,
                "reference_eyeglasses_score": round(reference_attributes["eyeglasses"], 3) if reference_attributes else None,
                "live_eyeglasses_score": round(live_attributes["eyeglasses"], 3) if live_attributes else None,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unhandled error in employeeFaceCompare")
        return JSONResponse(
            status_code=500,
            content={
                "status": False,
                "message": "Internal server error",
                "data": {
                    "face_match": False,
                    "match_score": 0.0,
                    "liveness_passed": False,
                    "liveness_score": 0.0,
                    "challenge_passed": False,
                    "challenge_reason": "error",
                    "challenge_yaw_delta": 0.0,
                    "challenge_similarity": 0.0,
                },
            },
        )

# ==============================
# Face Liveness Check
# ==============================
@app.post("/faceLiveness")
async def check_liveness(
    request: Request,
    capture: UploadFile = File(None),
    capture_base64: str = Body(None),
    store_db: bool = Form(False),
):
    """
    Check if captured face is live (not a photograph/replay).
    """
    try:
        logger.info("---- Face Liveness API Called ----")

        verify_token(request)

        # Get capture image
        if capture_base64:
            try:
                capture_bytes = base64_to_bytes(capture_base64)
                validate_file(capture_bytes, "image/jpeg")
                logger.info("Capture received via base64")
            except Exception as e:
                logger.exception("Invalid base64 data for capture")
                raise HTTPException(status_code=400, detail="Invalid base64 data for capture")

        elif capture is not None:
            try:
                capture_bytes = await asyncio.wait_for(capture.read(), timeout=60)
                validate_file(capture_bytes, capture.content_type)
                logger.info("Capture received via upload")
            except asyncio.TimeoutError:
                logger.error("Timeout while reading capture")
                raise HTTPException(status_code=408, detail="Error: Timeout for capture. Try again")
        else:
            raise HTTPException(status_code=400, detail="capture or capture_base64 is required")

        # Detect faces
        img, detections = detect_faces(capture_bytes)
        faces_count = len(detections) if detections is not None and isinstance(detections, np.ndarray) else 0

        if faces_count != 1:
            reason = "multiple_faces_detected" if faces_count > 1 else "no_face_detected"
            error_desc = "❌ Only one face allowed - please ensure only your face is visible" if faces_count > 1 else "❌ No face detected - please ensure your face is visible in frame"
            return JSONResponse(status_code=400, content={
                "status": False,
                "message": "Liveness check failed: exactly one face must be visible",
                "data": {
                    "liveness_passed": False, "liveness_score": 0.0,
                    "liveness_reason": reason,
                    "error_description": error_desc,
                    "spoof_detected": False,
                    "face_detected": bool(faces_count > 0), "faces_count": int(faces_count),
                    "capture_id": "", "captured_at_utc": datetime.utcnow().isoformat() + "Z",
                    "store_db": bool(store_db), "db_status": "not_stored", "storage_filename": None,
                    "reference_glasses": None, "live_glasses": None, "glasses_match": None,
                    "glasses_validation_reason": "not_checked",
                },
            })

        # Evaluate liveness
        is_live, liveness_score, liveness_reason = evaluate_liveness(capture_bytes)

        # ====== REQUIRE REFERENCE IMAGE ======
        reference_attributes = None
        live_attributes = get_glasses_attributes(capture_bytes)
        reference_glasses = live_glasses = glasses_match = None
        glasses_reason = "reference_image_not_available"
        reference_path = os.path.join(TEMP_FOLDER, "reference.jpg")
        
        # CHECK IF REFERENCE IMAGE EXISTS
        if not os.path.exists(reference_path):
            logger.warning("Reference image not found - liveness check requires reference")
            return JSONResponse(status_code=400, content={
                "status": False,
                "message": "Liveness check failed: Reference image required",
                "data": {
                    "liveness_passed": False,
                    "liveness_score": 0.0,
                    "liveness_reason": "reference_image_required",
                    "error_description": "❌ Reference image required - please upload reference image first",
                    "spoof_detected": False,
                    "face_detected": bool(faces_count > 0),
                    "faces_count": int(faces_count),
                    "capture_id": hashlib.md5(capture_bytes).hexdigest()[:16],
                    "captured_at_utc": datetime.utcnow().isoformat() + "Z",
                    "store_db": bool(store_db),
                    "db_status": "not_stored",
                    "storage_filename": None,
                    "reference_glasses": None,
                    "live_glasses": None,
                    "glasses_match": None,
                    "glasses_validation_reason": "reference_image_not_available",
                    "reference_eyeglasses_score": None,
                    "live_eyeglasses_score": round(live_attributes["eyeglasses"], 3) if live_attributes else None,
                },
            })
        
        # REFERENCE IMAGE EXISTS - Continue with validation
        with open(reference_path, "rb") as reference_file:
            reference_attributes = get_glasses_attributes(reference_file.read())
        if reference_attributes is not None and live_attributes is not None:
            reference_glasses = bool(reference_attributes["eyeglasses"] >= .5 or reference_attributes["sunglasses"] >= .5)
            live_glasses = bool(live_attributes["eyeglasses"] >= .5 or live_attributes["sunglasses"] >= .5)
            glasses_match = reference_glasses == live_glasses
            glasses_reason = "glasses_match" if glasses_match else "glasses_mismatch"
            if not glasses_match:
                is_live = False
                liveness_reason = "glasses_mismatch"

        # evaluate_liveness already performs the replay check and records the
        # frame hash. Checking it again here made every new capture look like
        # a replay of itself.
        spoof_detected = liveness_reason == "replay_detected"

        capture_id = hashlib.md5(capture_bytes).hexdigest()[:16]
        now = datetime.utcnow()

        logger.info(
            f"Liveness check: live={is_live}, score={liveness_score}, "
            f"spoof={spoof_detected}, faces={faces_count}"
        )

        storage_filename = None
        if store_db:
            content_type = capture.content_type if capture is not None else "image/jpeg"
            extension = ".png" if content_type == "image/png" else ".jpg"
            storage_filename = f"liveness_{now.strftime('%Y%m%d_%H%M%S_%f')}{extension}"
            with open(os.path.join(STORAGE_FOLDER, storage_filename), "wb") as stored_capture:
                stored_capture.write(capture_bytes)

        # Build user-friendly error description
        error_description_map = {
            "liveness_passed": "✅ Face is live and validated",
            "eyes_closed_or_not_detected": "❌ Please open your eyes and look straight at camera",
            "move_closer_to_camera": "❌ Please move closer to camera - face should fill more of screen (arm's length distance)",
            "centre_your_face": "❌ Please center your face in frame - don't position at edges",
            "look_straight_at_camera": "❌ Please look straight at camera - don't turn your head to the side",
            "whole_face_not_visible": "❌ Please ensure your entire face is visible in frame",
            "low_face_detection_confidence": "❌ Face quality too low - ensure good lighting and clear view",
            "replay_detected": "❌ Spoof/replay detected - please provide a live face",
            "glasses_mismatch": "❌ Glasses do not match reference image - please wear or remove glasses accordingly",
            "reference_image_required": "❌ Reference image required - please upload reference image first",
            "multiple_faces_detected": "❌ Only one face allowed - please ensure only your face is visible",
            "no_face_detected": "❌ No face detected - please ensure your face is visible in frame",
        }
        
        error_description = error_description_map.get(liveness_reason, f"❌ Validation failed: {liveness_reason}")

        return {
            "status": bool(is_live),
            "message": "Liveness check passed" if is_live else ("Liveness check failed: glasses do not match the reference" if glasses_match is False else "Liveness check failed"),
            "data": {
                "liveness_passed": is_live,
                "liveness_score": round(liveness_score, 3),
                "liveness_reason": liveness_reason,
                "error_description": error_description,
                "spoof_detected": spoof_detected,
                "face_detected": bool(faces_count > 0),
                "faces_count": int(faces_count),
                "capture_id": capture_id,
                "captured_at_utc": now.isoformat() + "Z",
                "store_db": store_db,
                "db_status": "stored" if store_db else "not_stored",
                "storage_filename": storage_filename,
                "reference_glasses": reference_glasses,
                "live_glasses": live_glasses,
                "glasses_match": glasses_match,
                "glasses_validation_reason": glasses_reason,
                "reference_eyeglasses_score": round(reference_attributes["eyeglasses"], 3) if reference_attributes else None,
                "live_eyeglasses_score": round(live_attributes["eyeglasses"], 3) if live_attributes else None,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unhandled error in faceLiveness")
        return JSONResponse(
            status_code=500,
            content={
                "status": False,
                "message": "Internal server error",
                "data": {
                    "liveness_passed": False,
                    "liveness_score": 0.0,
                    "liveness_reason": "error",
                    "spoof_detected": False,
                    "face_detected": False,
                    "faces_count": 0,
                    "capture_id": "",
                    "captured_at_utc": datetime.utcnow().isoformat() + "Z",
                    "store_db": False,
                    "db_status": "error",
                },
            },
        )

# ==============================
# Get Stored Images
# ==============================
@app.get("/dev/stored-images")
async def list_stored_images(request: Request):
    """List all stored reference images."""
    verify_token(request)
    
    try:
        files = os.listdir(STORAGE_FOLDER)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        
        details = []
        for filename in image_files:
            filepath = os.path.join(STORAGE_FOLDER, filename)
            size = os.path.getsize(filepath)
            mtime = os.path.getmtime(filepath)
            mtime_iso = datetime.fromtimestamp(mtime).isoformat() + "Z"
            details.append({
                "filename": filename,
                "size": size,
                "created_at_utc": mtime_iso,
                "path": filepath
            })
        
        return {
            "status": True,
            "message": f"Found {len(image_files)} stored images",
            "data": {
                "count": len(image_files),
                "images": details,
                "storage_folder": STORAGE_FOLDER
            }
        }
    except Exception as e:
        logger.exception("Error listing stored images")
        return {
            "status": False,
            "message": "Error listing images",
            "data": {"error": str(e)}
        }

# ==============================
# Get Stored Image (Download)
# ==============================
@app.get("/dev/stored-images/{filename}")
async def get_stored_image(filename: str, request: Request):
    """Download a stored reference image."""
    verify_token(request)
    
    try:
        # Security: prevent directory traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        filepath = os.path.join(STORAGE_FOLDER, filename)
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Image not found")
        
        return FileResponse(filepath, media_type="image/jpeg")
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error retrieving stored image")
        raise HTTPException(status_code=500, detail="Error retrieving image")

# ==============================
# DEV: Reset Cache
# ==============================
@app.post("/dev/reset-cache")
async def reset_cache(request: Request):
    """
    Development endpoint: clear temporary data and replay cache.
    """
    verify_token(request)

    try:
        # Clear recent hashes
        RECENT_LIVE_HASHES.clear()

        # Remove temp files
        temp_ref = os.path.join(TEMP_FOLDER, "reference.jpg")
        if os.path.exists(temp_ref):
            os.remove(temp_ref)

        logger.info("Cache reset successfully")

        return {
            "status": True,
            "message": "Cache reset successfully",
            "data": {"cleared": True},
        }

    except Exception as e:
        logger.exception("Error resetting cache")
        raise HTTPException(status_code=500, detail="Error resetting cache")

# ==============================
# DEV: Conditions Info
# ==============================
@app.get("/dev/conditions-info")
async def conditions_info(request: Request):
    """
    Development endpoint: return current configuration and conditions.
    """
    verify_token(request)
    
    # Count stored images
    stored_count = 0
    storage_size = 0
    try:
        files = os.listdir(STORAGE_FOLDER)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        stored_count = len(image_files)
        for f in image_files:
            storage_size += os.path.getsize(os.path.join(STORAGE_FOLDER, f))
    except:
        pass

    return {
        "status": True,
        "message": "Conditions info retrieved",
        "data": {
            "engine": "YuNet+SFace",
            "detector_model": DETECTOR_MODEL,
            "recognizer_model": RECOGNIZER_MODEL,
            "max_file_size": MAX_FILE_SIZE,
            "allowed_formats": ALLOWED_FORMATS,
            "liveness_threshold": LIVENESS_THRESHOLD,
            "turn_challenge_yaw_min": TURN_CHALLENGE_YAW_MIN,
            "brightness_threshold": BRIGHTNESS_THRESHOLD,
            "motion_threshold": MOTION_THRESHOLD,
            "recent_hashes_count": len(RECENT_LIVE_HASHES),
            "detector_ready": detector is not None,
            "recognizer_ready": recognizer is not None,
            "storage": {
                "folder": STORAGE_FOLDER,
                "stored_images_count": stored_count,
                "storage_size_bytes": storage_size,
                "storage_size_mb": round(storage_size / 1_000_000, 2),
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
    }

# ==============================
# Run FastAPI Server
# ==============================
if __name__ == "__main__":
    uvicorn.run("app_sface:app", host="0.0.0.0", port=8001, reload=False)
