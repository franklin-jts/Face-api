#!/usr/bin/env python3
"""Test eyes detection logic"""
import numpy as np

# Simulate eye landmarks
def test_eyes_detection(eye_distance, eye_vertical_distance):
    """Test if eyes are detected as open or closed"""
    eye_aspect_ratio = eye_distance / max(eye_vertical_distance, 1.0)
    eyes_open = eye_distance >= 20.0 and eye_aspect_ratio >= 1.8
    return eyes_open, eye_aspect_ratio

print("=" * 50)
print("EYES DETECTION TEST")
print("=" * 50)

# Test Case 1: Eyes OPEN (normal)
print("\nTest 1: Eyes OPEN (Normal)")
eyes_open, ratio = test_eyes_detection(35.0, 15.0)  # Normal open eyes
print(f"  Eye distance: 35.0 px")
print(f"  Eye vertical distance: 15.0 px")
print(f"  Aspect ratio: {ratio:.2f}")
print(f"  Result: {'✅ OPEN' if eyes_open else '❌ CLOSED'}")

# Test Case 2: Eyes CLOSED
print("\nTest 2: Eyes CLOSED")
eyes_open, ratio = test_eyes_detection(8.0, 8.0)  # Closed eyes
print(f"  Eye distance: 8.0 px")
print(f"  Eye vertical distance: 8.0 px")
print(f"  Aspect ratio: {ratio:.2f}")
print(f"  Result: {'✅ OPEN' if eyes_open else '❌ CLOSED'}")

# Test Case 3: Eyes partially closed
print("\nTest 3: Eyes PARTIALLY CLOSED")
eyes_open, ratio = test_eyes_detection(25.0, 18.0)  # Partially closed
print(f"  Eye distance: 25.0 px")
print(f"  Eye vertical distance: 18.0 px")
print(f"  Aspect ratio: {ratio:.2f}")
print(f"  Result: {'✅ OPEN' if eyes_open else '❌ CLOSED'}")

# Test Case 4: Eyes almost closed
print("\nTest 4: Eyes ALMOST CLOSED")
eyes_open, ratio = test_eyes_detection(15.0, 14.0)  # Almost closed
print(f"  Eye distance: 15.0 px")
print(f"  Eye vertical distance: 14.0 px")
print(f"  Aspect ratio: {ratio:.2f}")
print(f"  Result: {'✅ OPEN' if eyes_open else '❌ CLOSED'}")

print("\n" + "=" * 50)
print("Thresholds:")
print("  Eye distance min: 20.0 px")
print("  Aspect ratio min: 1.8")
print("=" * 50)
