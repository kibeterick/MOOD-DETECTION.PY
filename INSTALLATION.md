# 📦 Installation Guide

Complete installation instructions for the Mood Detection System.

## Prerequisites

### Required Software
- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Webcam** (built-in or USB)
- **Microphone** (for voice recognition)
- **Internet connection** (for speech recognition API)

### System Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **Processor**: Dual-core 2.0GHz or better

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/kibeterick/MOOD-DETECTION.PY.git
cd MOOD-DETECTION.PY
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python test_system.py
```

If all imports succeed, you're ready to go!

## Platform-Specific Instructions

### Windows

#### Install Visual C++ Build Tools (if needed)
Some packages require C++ compiler:
1. Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
2. Install "Desktop development with C++"

#### PyAudio Installation (Alternative)
If PyAudio fails:
```bash
pip install pipwin
pipwin install pyaudio
```

### macOS

#### Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Install PortAudio
```bash
brew install portaudio
pip install pyaudio
```

### Linux (Ubuntu/Debian)

#### Install System Dependencies
```bash
sudo apt-get update
sudo apt-get install python3-dev python3-pip
sudo apt-get install portaudio19-dev
sudo apt-get install libopencv-dev
```

#### Install Python Packages
```bash
pip3 install -r requirements.txt
```

## Troubleshooting

### Issue: "No module named 'cv2'"
```bash
pip uninstall opencv-python
pip install opencv-python==4.8.0
```

### Issue: "Could not find a version that satisfies numpy"
```bash
pip install numpy>=1.22,<1.25
```

### Issue: "Pillow version conflict"
```bash
pip install pillow>=10.2.0,<10.3.0
```

### Issue: Camera not detected
```bash
# Test camera
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Failed')"
```

### Issue: Microphone not working
- **Windows**: Check Privacy Settings → Microphone → Allow apps
- **macOS**: System Preferences → Security & Privacy → Microphone
- **Linux**: Check `alsamixer` settings

## Running the Application

### Web Interface (Recommended)
```bash
python web_mood_app.py
```
Open browser: `http://localhost:5000`

### Command Line Interface
```bash
python enhanced_main.py
```

### View Mood History
```bash
python enhanced_main.py --history
```

## Updating

To update to the latest version:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf MOOD-DETECTION.PY  # Linux/macOS
# or
rmdir /s MOOD-DETECTION.PY  # Windows
```

## Getting Help

- Check [README.md](README.md) for usage instructions
- Read [VOICE_RECOGNITION_GUIDE.md](VOICE_RECOGNITION_GUIDE.md) for voice features
- Open an issue on [GitHub](https://github.com/kibeterick/MOOD-DETECTION.PY/issues)

## Next Steps

After installation:
1. Test camera detection
2. Test voice recognition
3. Explore the web interface
4. Read the user guide
5. Customize settings in `config.py`

Happy mood detecting! 🎭
