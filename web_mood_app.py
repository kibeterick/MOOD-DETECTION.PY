"""Web-based Mood Detection System with Flask"""

from flask import Flask, render_template, Response, jsonify, request
import cv2
from fer import FER
import random
import json
from datetime import datetime
import speech_recognition as sr
from textblob import TextBlob
import pandas as pd
import threading
import numpy as np
from collections import deque

app = Flask(__name__)

# Initialize FER detector
detector = FER(mtcnn=True)

# Video stabilization settings
class VideoStabilizer:
    def __init__(self, smoothing_window=5):
        self.smoothing_window = smoothing_window
        self.frame_buffer = deque(maxlen=smoothing_window)
        self.prev_gray = None
        self.transforms = deque(maxlen=30)
        
    def stabilize_frame(self, frame):
        """Apply stabilization to reduce camera shake"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if self.prev_gray is None:
            self.prev_gray = gray
            return frame
        
        # Detect feature points
        prev_pts = cv2.goodFeaturesToTrack(self.prev_gray, 
                                           maxCorners=200,
                                           qualityLevel=0.01,
                                           minDistance=30,
                                           blockSize=3)
        
        if prev_pts is not None:
            # Calculate optical flow
            curr_pts, status, err = cv2.calcOpticalFlowPyrLK(self.prev_gray, gray, prev_pts, None)
            
            # Filter valid points
            idx = np.where(status == 1)[0]
            prev_pts = prev_pts[idx]
            curr_pts = curr_pts[idx]
            
            if len(prev_pts) > 0:
                # Estimate transformation
                transform = cv2.estimateAffinePartial2D(prev_pts, curr_pts)[0]
                
                if transform is not None:
                    # Extract translation
                    dx = transform[0, 2]
                    dy = transform[1, 2]
                    
                    # Store transform
                    self.transforms.append([dx, dy])
                    
                    # Calculate smoothed trajectory
                    if len(self.transforms) >= self.smoothing_window:
                        smooth_dx = np.mean([t[0] for t in list(self.transforms)[-self.smoothing_window:]])
                        smooth_dy = np.mean([t[1] for t in list(self.transforms)[-self.smoothing_window:]])
                        
                        # Apply smoothed transformation
                        diff_dx = smooth_dx - dx
                        diff_dy = smooth_dy - dy
                        
                        # Create transformation matrix
                        M = np.array([[1, 0, diff_dx],
                                     [0, 1, diff_dy]], dtype=np.float32)
                        
                        # Apply transformation
                        h, w = frame.shape[:2]
                        frame = cv2.warpAffine(frame, M, (w, h))
        
        self.prev_gray = gray
        return frame
    
    def smooth_frame(self, frame):
        """Apply temporal smoothing"""
        self.frame_buffer.append(frame.copy())
        
        if len(self.frame_buffer) < self.smoothing_window:
            return frame
        
        # Average frames for smoothing
        smoothed = np.mean(self.frame_buffer, axis=0).astype(np.uint8)
        return smoothed

# Initialize stabilizer
stabilizer = VideoStabilizer(smoothing_window=5)

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Feelings dataset for keyword matching
feelings_data = {
    "keyword": [
        "angry", "hate", "irritated", "mad", "furious",
        "sad", "depressed", "cry", "unhappy", "miserable",
        "happy", "joy", "excited", "love", "great", "wonderful",
        "bored", "tired", "exhausted",
        "anxious", "worried", "nervous", "stressed"
    ],
    "feeling": [
        "angry", "angry", "angry", "angry", "angry",
        "sad", "sad", "sad", "sad", "sad",
        "happy", "happy", "happy", "happy", "happy", "happy",
        "neutral", "neutral", "neutral",
        "fear", "fear", "fear", "fear"
    ]
}
dataset = pd.DataFrame(feelings_data)

# Motivational messages
motivations = {
    "angry": [
        "Take a deep breath. You're stronger than your anger.",
        "Channel your frustration into something productive.",
        "It's okay to feel angry—just don't let it control you."
    ],
    "sad": [
        "Everything will be okay. You've survived 100% of your worst days.",
        "You're not alone. You are loved and valued.",
        "This too shall pass. Better days are coming."
    ],
    "happy": [
        "Keep smiling, it makes others happy too!",
        "You're glowing with positivity. Spread it around!",
        "Your joy is beautiful. Hold onto this feeling."
    ],
    "surprise": [
        "Wow! Something unexpected must've happened.",
        "Surprises make life interesting—embrace the unknown!"
    ],
    "neutral": [
        "Sometimes, a neutral moment is peaceful. Enjoy it.",
        "Take this time to reflect and recharge."
    ],
    "fear": [
        "Fear is natural. You can overcome it, step by step.",
        "Face your fears. You're braver than you believe."
    ],
    "disgust": [
        "Something bothering you? Take a moment to breathe.",
        "Not everything deserves your energy."
    ]
}

# Global variables
current_emotion = "neutral"
current_confidence = 0.0
current_message = "Welcome! Look at the camera to detect your mood."
voice_emotion = None
voice_text = ""
voice_confidence = 0.0
is_listening = False

def generate_frames():
    """Generate video frames with emotion detection"""
    global current_emotion, current_confidence, current_message
    
    camera = cv2.VideoCapture(0)
    
    # Set camera properties for better stability
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    camera.set(cv2.CAP_PROP_FPS, 30)
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Apply video stabilization
        frame = stabilizer.stabilize_frame(frame)
        frame = stabilizer.smooth_frame(frame)
        
        # Detect emotions
        result = detector.detect_emotions(frame)
        
        if result:
            emotions = result[0]['emotions']
            detected_emotion = max(emotions, key=emotions.get)
            confidence = emotions[detected_emotion]
            
            # Update global state
            current_emotion = detected_emotion
            current_confidence = confidence
            
            if confidence > 0.3:
                current_message = random.choice(motivations.get(detected_emotion, ["Stay positive!"]))
            
            # Draw on frame
            x, y, w, h = result[0]['box']
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Display emotion and confidence
            text = f"{detected_emotion}: {confidence:.2f}"
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.9, (0, 255, 0), 2)
            
            # Draw emotion bars
            y_offset = 30
            for emotion, score in sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]:
                bar_width = int(score * 200)
                cv2.rectangle(frame, (10, y_offset), (10 + bar_width, y_offset + 20), 
                            (0, 255, 0), -1)
                cv2.putText(frame, f"{emotion}: {score:.2f}", (10, y_offset + 15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y_offset += 30
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def match_feeling(text):
    """Match feeling from text using keyword dataset"""
    words = text.lower().split()
    for word in words:
        match = dataset[dataset['keyword'] == word]
        if not match.empty:
            return match.iloc[0]['feeling']
    return None

def analyze_voice_mood(text):
    """Analyze mood from voice text using sentiment analysis"""
    feeling = match_feeling(text)
    if feeling:
        return feeling, 0.8
    
    # Use TextBlob for sentiment analysis
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.3:
        return "happy", abs(polarity)
    elif polarity < -0.3:
        return "sad", abs(polarity)
    else:
        return "neutral", 0.5

@app.route('/get_emotion')
def get_emotion():
    """API endpoint to get current emotion data"""
    # Combine face and voice emotions
    combined_emotion = current_emotion
    combined_confidence = current_confidence
    
    if voice_emotion and voice_confidence > 0.5:
        # If voice detection is strong, blend it with face detection
        combined_emotion = voice_emotion
        combined_confidence = (current_confidence + voice_confidence) / 2
    
    return jsonify({
        'emotion': combined_emotion,
        'confidence': round(combined_confidence, 2),
        'message': current_message,
        'voice_text': voice_text,
        'voice_emotion': voice_emotion,
        'is_listening': is_listening,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/start_listening', methods=['POST'])
def start_listening():
    """Start voice recognition"""
    global is_listening, voice_emotion, voice_text, voice_confidence, current_message
    
    is_listening = True
    
    def listen():
        global is_listening, voice_emotion, voice_text, voice_confidence, current_message
        
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Recognize speech
                text = recognizer.recognize_google(audio)
                voice_text = text
                
                # Analyze mood from text
                emotion, confidence = analyze_voice_mood(text)
                voice_emotion = emotion
                voice_confidence = confidence
                
                # Update message
                current_message = random.choice(motivations.get(emotion, ["Stay positive!"]))
                
        except sr.WaitTimeoutError:
            voice_text = "No speech detected. Please try again."
        except sr.UnknownValueError:
            voice_text = "Could not understand audio. Please speak clearly."
        except sr.RequestError as e:
            voice_text = f"Speech recognition error: {str(e)}"
        except Exception as e:
            voice_text = f"Error: {str(e)}"
        finally:
            is_listening = False
    
    # Run listening in a separate thread
    thread = threading.Thread(target=listen)
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'listening', 'message': 'Listening to your voice...'})

@app.route('/stop_listening', methods=['POST'])
def stop_listening():
    """Stop voice recognition"""
    global is_listening
    is_listening = False
    return jsonify({'status': 'stopped', 'message': 'Voice recognition stopped'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎭 Mood Detection Web Server Starting...")
    print("="*60)
    print("\n📱 Open your browser and go to:")
    print("   http://localhost:5000")
    print("\n💡 The camera will start automatically")
    print("   Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
