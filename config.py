# Configuration file for mood detection system

# Camera settings
CAMERA_INDEX = 0
FRAME_CAPTURE_COUNT = 30
SCAN_DURATION_SECONDS = 3

# Confidence thresholds
MIN_EMOTION_CONFIDENCE = 0.3
MIN_FACE_DETECTION_CONFIDENCE = 0.5

# Speech settings
SPEECH_RATE = 150
SPEECH_VOLUME = 0.9

# Sentiment analysis thresholds
POSITIVE_THRESHOLD = 0.3
NEGATIVE_THRESHOLD = -0.3

# Logging
ENABLE_MOOD_HISTORY = True
HISTORY_FILE = "mood_history.json"
