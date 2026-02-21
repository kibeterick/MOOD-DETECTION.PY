# 🎭 Mood Detection System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-red.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive real-time mood detection system using **facial recognition**, **voice analysis**, and **camera stabilization** with a beautiful web interface.

![Mood Detection Demo](https://img.shields.io/badge/Status-Active-success)

## ✨ Features

### 🎥 Advanced Computer Vision
- **Real-time facial emotion detection** using FER (Facial Expression Recognition)
- **Camera stabilization** with optical flow tracking
- **Motion smoothing** for steady video feed
- **Multi-face detection** support
- **Confidence scoring** for accurate results

### 🎤 Voice Recognition
- **Speech-to-text** conversion using Google Speech Recognition
- **Keyword emotion detection** (angry, sad, happy, worried, etc.)
- **Sentiment analysis** using TextBlob
- **Combined face + voice** emotion analysis
- **Real-time audio processing**

### 🌐 Web Interface
- **Beautiful responsive UI** with gradient design
- **Live camera feed** with emotion overlay
- **Real-time emotion display** with emojis
- **Confidence scores** and statistics
- **Motivational messages** based on detected mood
- **Session tracking** with detection counts
- **Voice control button** for hands-free operation

### 📊 Emotion Detection
Detects 7 emotions:
- 😊 Happy
- 😢 Sad
- 😠 Angry
- 😨 Fear
- 😮 Surprise
- 😐 Neutral
- 🤢 Disgust

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/kibeterick/MOOD-DETECTION.PY.git
cd MOOD-DETECTION.PY
```

2. **Create virtual environment**
```bash
python -m venv .venv
```

3. **Activate virtual environment**
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

**Web Interface (Recommended)**
```bash
python web_mood_app.py
```
Then open your browser to: `http://localhost:5000`

**Command Line Interface**
```bash
python enhanced_main.py
```

**View Mood History**
```bash
python enhanced_main.py --history
```

## 📱 Usage

### Web Interface
1. Open `http://localhost:5000` in your browser
2. Allow camera and microphone permissions
3. Your emotion will be detected automatically
4. Click **"🎤 Start Voice Detection"** to add voice analysis
5. Speak clearly about how you're feeling
6. Get personalized motivational messages

### Voice Commands
Say things like:
- "I'm feeling great today!"
- "I'm sad and depressed"
- "I'm so angry right now"
- "I'm worried and anxious"

## 🛠️ Configuration

Edit `config.py` to customize:
```python
CAMERA_INDEX = 0  # Change camera source
CONFIDENCE_THRESHOLD = 0.3  # Emotion detection sensitivity
SPEECH_RATE = 150  # Text-to-speech speed
ENABLE_LOGGING = True  # Mood history tracking
```

## 📂 Project Structure

```
MOOD-DETECTION.PY/
├── web_mood_app.py          # Flask web application (MAIN)
├── templates/
│   └── index.html           # Web interface
├── enhanced_main.py         # CLI version with logging
├── mood_logger.py           # Mood history tracking
├── config.py                # Configuration settings
├── utils.py                 # Image processing utilities
├── requirements.txt         # Python dependencies
├── VOICE_RECOGNITION_GUIDE.md  # Voice feature guide
├── main.py                  # Original face detection
├── mood.py                  # Voice-only detection
└── mood detection.py        # Full-featured CLI
```

## 🔧 Technical Details

### Technologies Used
- **Flask** - Web framework
- **OpenCV** - Computer vision and video processing
- **FER** - Facial Expression Recognition
- **SpeechRecognition** - Voice-to-text conversion
- **TextBlob** - Natural language processing
- **Pandas** - Data analysis for keyword matching
- **NumPy** - Numerical computations for stabilization

### Camera Stabilization
- Optical flow tracking using Lucas-Kanade method
- Feature point detection with `goodFeaturesToTrack`
- Affine transformation for motion compensation
- Temporal smoothing with frame averaging
- Real-time processing at 30 FPS

### Voice Analysis Pipeline
1. Audio capture from microphone
2. Speech-to-text using Google API
3. Keyword matching against emotion database
4. Sentiment polarity analysis
5. Confidence scoring and blending with facial data

## 📊 System Requirements

- **Python**: 3.8 or higher
- **Webcam**: Any USB or built-in camera
- **Microphone**: For voice recognition
- **RAM**: 4GB minimum, 8GB recommended
- **Internet**: Required for speech recognition API

## 🎯 Tips for Best Results

### Camera Detection
- Ensure good lighting (natural light is best)
- Look directly at the camera
- Keep face centered in frame
- Avoid extreme angles
- Remove glasses if detection is poor

### Voice Recognition
- Speak clearly and naturally
- Minimize background noise
- Use keywords like "happy", "sad", "angry"
- Wait for "Listening..." indicator
- Speak within 5-10 seconds

## 🐛 Troubleshooting

### Camera not working
```bash
# Check available cameras
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### Voice recognition fails
- Check microphone permissions in browser
- Ensure internet connection is active
- Try speaking louder or closer to mic

### Dependencies issues
```bash
# Reinstall with specific versions
pip install numpy>=1.22,<1.25
pip install pillow>=10.2.0,<10.3.0
```

## 🔮 Future Enhancements

- [ ] Mobile app (iOS/Android)
- [ ] Multi-user support with profiles
- [ ] Advanced analytics dashboard
- [ ] Mood prediction using ML
- [ ] Integration with mental health resources
- [ ] Export mood reports (PDF/CSV)
- [ ] Dark mode for web interface
- [ ] Multiple language support
- [ ] Emotion history graphs
- [ ] API for third-party integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Kibet Erick**
- GitHub: [@kibeterick](https://github.com/kibeterick)
- Repository: [MOOD-DETECTION.PY](https://github.com/kibeterick/MOOD-DETECTION.PY)

## 🙏 Acknowledgments

- FER library for facial emotion recognition
- OpenCV community for computer vision tools
- Flask framework for web development
- Google Speech Recognition API
- TextBlob for sentiment analysis

## 📞 Support

If you encounter any issues or have questions:
1. Check the [VOICE_RECOGNITION_GUIDE.md](VOICE_RECOGNITION_GUIDE.md)
2. Open an issue on GitHub
3. Review troubleshooting section above

---

⭐ If you find this project helpful, please give it a star!

Made with ❤️ by Kibet Erick
