import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = os.getenv("NEWS_API_KEY")

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    # Convert text to speech and save as an MP3 file
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer before using it
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    # Wait for the playback to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove('temp.mp3')

def aiProcess(command):
    responses = {
        "hello": "Hello! I am here to assist you.",
        "how are you": "I am just a bunch of code, but I'm doing great!",
        "what is your name": "My name is Alexa.",
        "open google": "Opening Google.",
        "open youtube": "Opening YouTube.",
        "news": "Here are some recent headlines."
    }

    command_lower = command.lower()
    for key in responses:
        if key in command_lower:
            return responses[key]

    return "Sorry, I didn't understand that command."

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # Limit to 5 headlines
                speak(article['title'])
        else:
            speak("Sorry, I couldn't fetch the news.")
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Alexa...")
    while True:
        r = sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == "alexa":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Alexa active, listening for command...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print(f"Error: {e}")
__