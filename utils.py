"""Utility functions for mood detection system"""

import cv2
import numpy as np
from typing import Tuple, Optional

def check_camera_available(camera_index: int = 0) -> bool:
    """Check if camera is available"""
    cap = cv2.VideoCapture(camera_index)
    if cap.isOpened():
        cap.release()
        return True
    return False

def enhance_frame(frame: np.ndarray) -> np.ndarray:
    """Enhance frame quality for better detection"""
    # Convert to LAB color space
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Merge channels
    enhanced = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    
    return enhanced

def draw_emotion_bar(frame: np.ndarray, emotions: dict, 
                     x: int = 10, y: int = 100) -> np.ndarray:
    """Draw emotion confidence bars on frame"""
    if not emotions:
        return frame
    
    sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
    
    for i, (emotion, score) in enumerate(sorted_emotions[:5]):
        bar_y = y + (i * 30)
        bar_width = int(score * 200)
        
        # Draw bar background
        cv2.rectangle(frame, (x, bar_y), (x + 200, bar_y + 20), (50, 50, 50), -1)
        
        # Draw confidence bar
        color = (0, 255, 0) if i == 0 else (100, 100, 255)
        cv2.rectangle(frame, (x, bar_y), (x + bar_width, bar_y + 20), color, -1)
        
        # Draw text
        text = f"{emotion}: {score:.2f}"
        cv2.putText(frame, text, (x + 5, bar_y + 15), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    return frame

def get_lighting_quality(frame: np.ndarray) -> Tuple[str, float]:
    """Assess lighting quality of the frame"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)
    
    if mean_brightness < 50:
        return "Too Dark", mean_brightness
    elif mean_brightness > 200:
        return "Too Bright", mean_brightness
    else:
        return "Good", mean_brightness

def detect_face_region(frame: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    """Detect face region using Haar Cascade"""
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) > 0:
        return tuple(faces[0])  # Return first face (x, y, w, h)
    return None
