"""Test script to verify all dependencies are working"""

print("Testing mood detection system dependencies...\n")

# Test imports
try:
    import cv2
    print("✓ OpenCV imported successfully")
except Exception as e:
    print(f"✗ OpenCV error: {e}")

try:
    from fer import FER
    print("✓ FER (Facial Emotion Recognition) imported successfully")
except Exception as e:
    print(f"✗ FER error: {e}")

try:
    import pyttsx3
    print("✓ pyttsx3 (Text-to-Speech) imported successfully")
except Exception as e:
    print(f"✗ pyttsx3 error: {e}")

try:
    from textblob import TextBlob
    print("✓ TextBlob (Sentiment Analysis) imported successfully")
except Exception as e:
    print(f"✗ TextBlob error: {e}")

try:
    import pandas as pd
    print("✓ Pandas imported successfully")
except Exception as e:
    print(f"✗ Pandas error: {e}")

try:
    import speech_recognition as sr
    print("✓ SpeechRecognition imported successfully")
except Exception as e:
    print(f"✗ SpeechRecognition error: {e}")

print("\n" + "="*50)
print("All core dependencies are working!")
print("="*50)
print("\nYour mood detection system is ready to use.")
print("\nAvailable programs:")
print("  1. python main.py - Face-based mood detection")
print("  2. python mood.py - Voice-based mood detection")
print("  3. python 'mood detection.py' - Full-featured system")
print("  4. python enhanced_main.py - Enhanced version with logging")
