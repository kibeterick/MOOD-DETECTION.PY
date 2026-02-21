import speech_recognition as sr
from textblob import TextBlob
import pandas as pd
from textblob import TextBlob
import speech_recognition as sr
import pyttsx3
import random

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
        "It’s okay to take it slow today."
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
    "Neutral": ["'Let It Be' by The Beatles", "'Banana Pancakes' by Jack Johnson"]
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

# Analyze mood
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

# Main program
def main():
    text = get_audio()
    if text:
        mood = analyze_mood(text)
        speak(f"You seem to be feeling {mood}.")
        support_user(mood)

if __name__ == "__main__":
    main()
