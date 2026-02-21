import cv2
from fer import FER
import pyttsx3
import random
import sys
from mood_logger import MoodLogger
from config import *

# Initialize components
engine = pyttsx3.init()
engine.setProperty('rate', SPEECH_RATE)
engine.setProperty('volume', SPEECH_VOLUME)
logger = MoodLogger(HISTORY_FILE) if ENABLE_MOOD_HISTORY else None

# Enhanced motivations with more variety
motivations = {
    "angry": [
        "Take a deep breath. You're stronger than your anger.",
        "Channel your frustration into something productive.",
        "It's okay to feel angry—just don't let it control you.",
        "Step back for a moment. This feeling will pass.",
        "Your anger is valid, but you have the power to respond calmly."
    ],
    "sad": [
        "Everything will be okay. You've survived 100% of your worst days.",
        "You're not alone. You are loved and valued.",
        "Crying is not a weakness. It's a sign of strength.",
        "This too shall pass. Better days are coming.",
        "Be gentle with yourself. You're doing the best you can."
    ],
    "happy": [
        "Keep smiling, it makes others happy too!",
        "You're glowing with positivity. Spread it around!",
        "Happiness is contagious—enjoy it!",
        "Your joy is beautiful. Hold onto this feeling.",
        "What a wonderful moment! Savor it."
    ],
    "surprise": [
        "Wow, you look surprised! Something unexpected must've happened.",
        "Surprises make life interesting—embrace the unknown!",
        "Life keeps us on our toes. Roll with it!",
        "Unexpected moments can lead to great things."
    ],
    "neutral": [
        "Sometimes, a neutral moment is peaceful. Enjoy it.",
        "Take this time to reflect and recharge.",
        "Calm moments are valuable. Use them wisely.",
        "Balance is good. You're in a steady place."
    ],
    "fear": [
        "Fear is natural. You can overcome it, step by step.",
        "Face your fears. You're braver than you believe.",
        "It's okay to be scared. Courage is acting despite fear.",
        "You've faced challenges before. You can do this too."
    ],
    "disgust": [
        "Something bothering you? Take a moment to breathe.",
        "Not everything deserves your energy. Let go of what disgusts you.",
        "Trust your instincts. It's okay to feel this way.",
        "Sometimes we need to distance ourselves from negativity."
    ]
}

def speak(text):
    """Enhanced speech function with console output"""
    print(f"🔊 System: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"⚠️ Speech error: {e}")

def detect_emotion_from_face():
    """Improved face detection with better error handling"""
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    if not cap.isOpened():
        speak("Sorry, I couldn't access your camera.")
        return None, 0.0

    speak("Scanning your face. Please look at the camera.")
    detected_emotion = "neutral"
    confidence = 0.0
    frame_count = 0
    emotion_scores = {}

    try:
        while frame_count < FRAME_CAPTURE_COUNT:
            ret, frame = cap.read()
            if not ret:
                break
            
            emotion_result = detector.top_emotion(frame)
            if emotion_result:
                emotion, score = emotion_result
                
                # Accumulate scores for averaging
                if emotion not in emotion_scores:
                    emotion_scores[emotion] = []
                emotion_scores[emotion].append(score)
                
                if score > confidence:
                    detected_emotion = emotion
                    confidence = score

            # Enhanced visual feedback
            cv2.putText(frame, "Scanning... Press 'q' to quit", 
                       (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Current: {detected_emotion} ({confidence:.2f})", 
                       (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            cv2.imshow("Mood Scanner", frame)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            
            frame_count += 1

        cap.release()
        cv2.destroyAllWindows()
        
        # Calculate average confidence for detected emotion
        if detected_emotion in emotion_scores:
            avg_confidence = sum(emotion_scores[detected_emotion]) / len(emotion_scores[detected_emotion])
            return detected_emotion, avg_confidence
        
        return detected_emotion, confidence
        
    except Exception as e:
        print(f"❌ Camera Error: {e}")
        cap.release()
        cv2.destroyAllWindows()
        return None, 0.0

def give_feedback(emotion, confidence):
    """Enhanced feedback with confidence reporting"""
    emotion = emotion.lower()
    
    if confidence > 0:
        speak(f"You seem to be feeling {emotion} with {int(confidence * 100)}% confidence.")
    else:
        speak(f"You seem to be feeling {emotion}.")

    if emotion in motivations:
        message = random.choice(motivations[emotion])
    else:
        message = "I hope you're doing well today."

    speak(message)
    
    # Log the mood if logging is enabled
    if logger:
        logger.log_mood(emotion, confidence, method="facial", notes="")
        print(f"📝 Mood logged to history")

def show_mood_history():
    """Display recent mood history"""
    if not logger:
        print("Mood logging is disabled")
        return
    
    recent = logger.get_recent_moods(5)
    if recent:
        print("\n📊 Recent Mood History:")
        for entry in recent:
            timestamp = entry['timestamp'][:19]  # Remove microseconds
            print(f"  • {timestamp}: {entry['mood']} ({entry['confidence']:.2f})")
    
    summary = logger.get_mood_summary()
    if summary:
        print("\n📈 Overall Mood Summary:")
        for mood, count in sorted(summary.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {mood}: {count} times")

def main():
    """Main program with menu options"""
    print("\n" + "="*50)
    print("🎭 Enhanced Mood Detection System")
    print("="*50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--history":
        show_mood_history()
        return
    
    emotion, confidence = detect_emotion_from_face()
    
    if emotion:
        give_feedback(emotion, confidence)
        
        # Show quick stats
        if logger:
            today_moods = logger.get_today_moods()
            print(f"\n📅 You've checked your mood {len(today_moods)} time(s) today")
    else:
        speak("I couldn't detect your emotion. Please try again with better lighting.")

if __name__ == "__main__":
    main()
