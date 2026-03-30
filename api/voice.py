import speech_recognition as sr
import re

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio)
    except:
        return ""

def extract_details(text):
    text = text.lower()

    # Age extract
    age_match = re.search(r'\b(\d{1,3})\b', text)
    age = int(age_match.group()) if age_match else 30

    name_match = re.search(r'name is (\w+)', text)
    name = name_match.group(1) if name_match else "Unknown"

    # Symptoms = full text
    return name, age, text