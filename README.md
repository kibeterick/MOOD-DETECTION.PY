# 🎭 Mood Detection System

An intelligent mood detection system that analyzes facial expressions and voice to provide emotional support, motivational messages, and song recommendations.

## Features

- 📸 Real-time facial emotion detection using webcam
- 🎤 Voice-based mood analysis with speech recognition
- 💬 Sentiment analysis from text input
- 🎵 Personalized song recommendations based on mood
- 💪 Motivational messages and support
- 📊 Mood history tracking and analytics
- 🔊 Text-to-speech feedback

## Installation

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. If PyAudio fails on Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

## Usage

### Enhanced Main Program (Recommended)
```bash
python enhanced_main.py
```

### View Mood History
```bash
python enhanced_main.py --history
```

### Original Programs
- Face detection only: `python main.py`
- Voice analysis only: `python mood.py`
- Full featured: `python "mood detection.py"`

## Configuration

Edit `config.py` to customize:
- Camera settings
- Confidence thresholds
- Speech rate and volume
- Mood history logging

## Supported Emotions

- 😊 Happy
- 😢 Sad
- 😠 Angry
- 😨 Fear
- 😮 Surprise
- 😐 Neutral
- 🤢 Disgust

## Project Structure

- `enhanced_main.py` - Improved main program with logging
- `mood_logger.py` - Mood history tracking
- `config.py` - Configuration settings
- `utils.py` - Utility functions for image processing
- `main.py` - Original face detection program
- `mood.py` - Voice-based mood detection
- `mood detection.py` - Full-featured detection system

## Requirements

- Python 3.8+
- Webcam (for facial detection)
- Microphone (for voice detection)
- Internet connection (for speech recognition)

## Tips for Best Results

- Ensure good lighting for facial detection
- Look directly at the camera
- Speak clearly for voice recognition
- Minimize background noise

## Future Enhancements

- Mobile app integration
- Multi-user support
- Advanced analytics dashboard
- Integration with mental health resources
- Mood prediction based on patterns
