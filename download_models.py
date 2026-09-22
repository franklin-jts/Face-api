#!/usr/bin/env python3
"""
Download YuNet and SFace ONNX models from official sources.
Run this before starting app_sface.py
"""

import os
import urllib.request
import sys
from pathlib import Path

# Create models directory
models_dir = Path("models")
models_dir.mkdir(exist_ok=True)

# Model URLs (official OpenCV sources)
MODELS = {
    "face_detection_yunet_2023mar.onnx": (
        "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
        "YuNet Face Detector (2023)",
        26_000_000,  # ~26 MB
    ),
    "face_recognition_sface_2021dec.onnx": (
        "https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx",
        "SFace Face Recognizer (2021)",
        110_000_000,  # ~110 MB
    ),
}

def download_file(url: str, filepath: Path, description: str, expected_size: int):
    """Download a file from URL with progress."""
    if filepath.exists():
        file_size = filepath.stat().st_size
        print(f"✓ {description} already exists ({file_size / 1_000_000:.1f} MB)")
        return True

    print(f"\n📥 Downloading {description}...")
    print(f"   URL: {url}")
    print(f"   Expected size: ~{expected_size / 1_000_000:.1f} MB")

    try:
        def progress_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, int(downloaded * 100 / total_size))
            bar_length = 50
            filled = int(bar_length * downloaded / total_size)
            bar = "█" * filled + "░" * (bar_length - filled)
            sys.stdout.write(f"\r   [{bar}] {percent}% ({downloaded / 1_000_000:.1f} MB)")
            sys.stdout.flush()

        urllib.request.urlretrieve(url, filepath, progress_hook)
        print("\n   ✓ Downloaded successfully")
        return True
    except Exception as e:
        print(f"\n   ✗ Download failed: {e}")
        return False

def main():
    print("=" * 70)
    print("🎯 OpenCV YuNet + SFace Model Downloader")
    print("=" * 70)

    all_success = True
    for filename, (url, description, size) in MODELS.items():
        filepath = models_dir / filename
        if not download_file(url, filepath, description, size):
            all_success = False

    print("\n" + "=" * 70)
    if all_success:
        print("✅ All models downloaded successfully!")
        print("\nYou can now run: python app_sface.py")
    else:
        print("⚠️  Some models failed to download.")
        print("\nManual download:")
        for filename, (url, description, _) in MODELS.items():
            print(f"\n{description}:")
            print(f"  {url}")
            print(f"  Save to: models/{filename}")
    print("=" * 70)

if __name__ == "__main__":
    main()
