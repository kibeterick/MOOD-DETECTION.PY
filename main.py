import cv2
from fer import FER
import pyttsx3
import random

# Initialize speech engine
engine = pyttsx3.init()

# Motivations by mood
motivations = {
    "angry": [
        "Take a deep breath. You're stronger than your anger.",
        "Channel your frustration into something productive.",
        "It's okay to feel angry—just don't let it control you."
    ],
    "sad": [
        "Everything will be okay. You've survived 100% of your worst days.",
        "You're not alone. You are loved and valued.",
        "Crying is not a weakness. It's a sign of strength."
    ],
    "happy": [
        "Keep smiling, it makes others happy too!",
        "You're glowing with positivity. Spread it around!",
        "Happiness is contagious—enjoy it!"
    ],
    "surprise": [
        "Wow, you look surprised! Something unexpected must've happened.",
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
        "Not everything deserves your energy. Let go of what disgusts you."
    ]
}

def speak(text):
    print("System:", text)
    engine.say(text)
    engine.runAndWait()

def detect_emotion_from_face():
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(0)

    speak("Scanning your face. Please look at the camera.")
    detected_emotion = "neutral"
    confidence = 0.0

    try:
        for _ in range(30):  # Approx. 3 seconds
            ret, frame = cap.read()
            if not ret:
                break
            emotion_result = detector.top_emotion(frame)
            if emotion_result:
                emotion, score = emotion_result
                if score > confidence:
                    detected_emotion = emotion
                    confidence = score

            # Show camera feed with note
            cv2.putText(frame, "Scanning...", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Mood Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print("Camera Error:", e)
        cap.release()
        cv2.destroyAllWindows()

    return detected_emotion

def give_feedback(emotion):
    emotion = emotion.lower()
    speak(f"You seem to be feeling {emotion}.")

    if emotion in motivations:
        message = random.choice(motivations[emotion])
    else:
        message = "I hope you're doing well today."

    speak(message)

def main():
    emotion = detect_emotion_from_face()
    give_feedback(emotion)

if __name__ == "__main__":
    main()
