# =============================================================================
# INSTALLATION COMMAND for Python 3.10:
# Run this in your terminal (with your .venv activated)
# pip install opencv-python fer deepface moviepy pyttsx3 textblob pandas speechrecognition pyaudio
#
# If PyAudio fails, try:
# pip install pipwin
# pipwin install pyaudio
#
# If you have TensorFlow issues, try:
# pip uninstall tensorflow
# pip install tensorflow-cpu
# =============================================================================

import speech_recognition as sr
from textblob import TextBlob
import pandas as pd
import pyttsx3
import random
import cv2
from fer import FER
import time
from deepface import DeepFace

# Initialize TTS engine
engine = pyttsx3.init()

# Feelings dataset
data = {
    "keyword": [
        "angry", "hate", "irritated",
        "sad", "depressed", "cry",
        "happy", "joy", "excited", "love",
        "bored", "tired",
        "anxious", "worried"
    ],
    "feeling": [
        "Angry", "Angry", "Angry",
        "Sad", "Sad", "Sad",
        "Happy", "Happy", "Excited", "Happy",
        "Bored", "Tired",
        "Anxious", "Anxious"
    ]
}
dataset = pd.DataFrame(data)

# Motivational messages by mood
motivations = {
    "Sad": [
        "Everything will be okay. You're stronger than you think.",
        "This too shall pass. Just hold on.",
        "You are not alone. Talk to someone you trust."
    ],
    "Angry": [
        "Take a deep breath. You can rise above this.",
        "Anger doesn't solve anything, but talking might.",
        "Try to calm down and express yourself clearly."
    ],
    "Anxious": [
        "Pause and breathe. You're doing your best.",
        "Try to focus on the present moment.",
        "Reach out to a friend. You're not alone."
    ],
    "Tired": [
        "Make sure you get enough rest.",
        "Your body is asking for a break—listen to it.",
        "It's okay to take it slow today."
    ],
    "Happy": [
        "Keep smiling, it suits you!",
        "Spread your happiness with others.",
        "It’s a great day to keep the positivity going!"
    ],
    "Excited": [
        "Channel that energy into something great!",
        "Excitement is a sign you're passionate—go for it!"
    ],
    "Neutral": [
        "It's a calm moment—enjoy it.",
        "Use this time to reflect or relax."
    ],
    "Surprised": [
        "Surprises can be exciting! What just happened?",
        "Life is full of unexpected moments."
    ],
    "Fear": [
        "It's okay to feel scared. Take a moment to breathe.",
        "Remember your strength in facing challenges."
    ],
    "Disgust": [
        "Sometimes things don't sit right with us.",
        "Take a moment to understand what's bothering you."
    ]
}

# Suggested songs by mood
songs = {
    "Sad": ["'Fix You' by Coldplay", "'Someone Like You' by Adele"],
    "Angry": ["'Lose Yourself' by Eminem", "'Numb' by Linkin Park"],
    "Anxious": ["'Weightless' by Marconi Union", "'Let It Go' by James Bay"],
    "Tired": ["'Landslide' by Fleetwood Mac", "'Let Her Go' by Passenger"],
    "Happy": ["'Happy' by Pharrell Williams", "'Can't Stop the Feeling' by Justin Timberlake"],
    "Excited": ["'On Top of the World' by Imagine Dragons", "'Don't Stop Me Now' by Queen"],
    "Neutral": ["'Let It Be' by The Beatles", "'Banana Pancakes' by Jack Johnson"],
    "Surprised": ["'Surprise' by Glee Cast", "'A Sky Full of Stars' by Coldplay"],
    "Fear": ["'Shake It Out' by Florence + The Machine", "'Roar' by Katy Perry"],
    "Disgust": ["'Stronger' by Kelly Clarkson", "'Unbreakable' by Alicia Keys"]
}


# Speak output
def speak(text):
    print("System:", text)
    engine.say(text)
    engine.runAndWait()


# Match feeling from dataset
def match_feeling(text):
    words = text.lower().split()
    for word in words:
        match = dataset[dataset['keyword'] == word]
        if not match.empty:
            return match.iloc[0]['feeling']
    return None


# Analyze mood from text
def analyze_mood(text):
    feeling = match_feeling(text)
    if feeling:
        return feeling
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.3:
        return "Happy"
    elif polarity < -0.3:
        return "Sad"
    else:
        return "Neutral"


# Analyze mood from facial expression
def analyze_facial_mood():
    # Initialize the FER detector
    detector = FER(mtcnn=True)

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        speak("Sorry, I couldn't access your camera.")
        return None

    speak("I'll analyze your facial expression. Get ready and look at the camera.")
    time.sleep(2)

    # Capture a single frame
    ret, frame = cap.read()

    if not ret:
        speak("Sorry, I couldn't capture an image.")
        cap.release()
        return None

    # Detect emotions
    result = detector.detect_emotions(frame)

    cap.release()
    cv2.destroyAllWindows()

    if not result:
        speak("I couldn't detect a face. Let's try another method.")
        return None

    # Get the dominant emotion
    dominant_emotion = max(result[0]['emotions'], key=result[0]['emotions'].get)
    confidence = result[0]['emotions'][dominant_emotion]

    # Format the emotion name to match our dataset
    emotion_map = {
        'happy': 'Happy',
        'sad': 'Sad',
        'angry': 'Angry',
        'fear': 'Fear',
        'surprise': 'Surprised',
        'neutral': 'Neutral',
        'disgust': 'Disgust'
    }

    formatted_emotion = emotion_map.get(dominant_emotion, 'Neutral')

    speak(f"I detected you're feeling {formatted_emotion} with {confidence:.0%} confidence.")
    return formatted_emotion


# Alternative method using DeepFace for more robust detection
def analyze_facial_mood_deepface():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        speak("Sorry, I couldn't access your camera.")
        return None

    speak("I'll analyze your facial expression. Get ready and look at the camera.")
    time.sleep(2)

    # Capture a single frame
    ret, frame = cap.read()

    if not ret:
        speak("Sorry, I couldn't capture an image.")
        cap.release()
        return None

    cap.release()
    cv2.destroyAllWindows()

    try:
        # Analyze the image
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # Get the dominant emotion
        dominant_emotion = result[0]['dominant_emotion']

        # Format the emotion name to match our dataset
        emotion_map = {
            'happy': 'Happy',
            'sad': 'Sad',
            'angry': 'Angry',
            'fear': 'Fear',
            'surprise': 'Surprised',
            'neutral': 'Neutral',
            'disgust': 'Disgust'
        }

        formatted_emotion = emotion_map.get(dominant_emotion, 'Neutral')

        speak(f"I detected you're feeling {formatted_emotion}.")
        return formatted_emotion
    except Exception as e:
        speak("I had trouble analyzing your facial expression.")
        return None


# Suggest motivation, referral, and music
def support_user(feeling):
    if feeling not in motivations:
        feeling = "Neutral"
    motivation = random.choice(motivations[feeling])
    song = random.choice(songs[feeling])
    referral = "Consider talking to a close friend or a counselor if you're feeling overwhelmed."

    speak(motivation)
    speak(referral)
    speak(f"Here is a song that might help: {song}")


# Get audio input
def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please say something...")
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand what you said.")
            return None
        except sr.RequestError:
            speak("Speech recognition service failed.")
            return None


# Get user's choice for input method
def get_input_method():
    speak("How would you like to share your mood with me?")
    speak("Say 'voice' to speak, or 'face' for facial analysis.")

    text = get_audio()
    if text:
        if "face" in text.lower():
            return "face"
        elif "voice" in text.lower():
            return "voice"

    # Default to voice if no clear choice
    return "voice"


# Main program
def main():
    speak("Welcome to the Mood Detection System!")

    # Get user's preferred input method
    method = get_input_method()

    if method == "face":
        # Analyze facial mood
        mood = analyze_facial_mood()
        if not mood:
            # Try alternative method if first one fails
            mood = analyze_facial_mood_deepface()
        if not mood:
            # Fall back to voice if face detection fails
            speak("Let's try voice analysis instead.")
            text = get_audio()
            if text:
                mood = analyze_mood(text)
    else:
        # Analyze voice mood
        text = get_audio()
        if text:
            mood = analyze_mood(text)
        else:
            mood = None

    if mood:
        speak(f"You seem to be feeling {mood}.")
        support_user(mood)
    else:
        speak("I couldn't determine your mood. Please try again.")


if __name__ == "__main__":
    main()