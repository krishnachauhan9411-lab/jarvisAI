import pyttsx3
import speech_recognition as sr
import os
import pyautogui
import webbrowser
import google.generativeai as genai
from datetime import datetime

API_KEY = "Add_your_APIKEY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")
JARVIS_PROMPT = "You are Jarvis from Iron Man. Bes professional, concise and witty. Address user as sir. Keep responses under 3 sentences. User says: "
chat_session = model.start_chat(history=[])

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

def bolna(audio):
    print(f"Jarvis: {audio}")
    engine.say(audio)
    engine.runAndWait()

def sunna():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Listening...]")
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.pause_threshold = 1.0
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return "None"
    try:
        print("[Recognizing...]")
        query = r.recognize_google(audio, language="en-in")
        print(f"You: {query}")
        return query.lower()
    except:
        return "None"

def ai_brain(sawaal):
    try:
        response = chat_session.send_message(JARVIS_PROMPT + sawaal)
        return response.text.strip()
    except Exception as e:
        print(f"[AI Error]: {e}")
        return "Sir, I am having trouble connecting to my servers. Please try again."

def handle_command(query):
    if query == "None":
        return True
    if any(word in query for word in ["bye", "exit", "stop", "shutdown"]):
        bolna("Shutting down. Goodbye sir.")
        return False
    elif "open notepad" in query:
        bolna("Opening Notepad.")
        os.system("notepad.exe")
    elif "open youtube" in query:
        bolna("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in query:
        bolna("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "screenshot" in query:
        filename = f"jarvis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(filename)
        bolna("Screenshot saved.")
    elif "time" in query:
        bolna(datetime.now().strftime("It is %I:%M %p, sir."))
    elif "date" in query or "today" in query:
        bolna(datetime.now().strftime("Today is %A, %B %d, %Y."))
    else:
        bolna(ai_brain(query))
    return True

bolna("All systems operational. Jarvis is online sir.")
running = True
while running:
    query = sunna()
    running = handle_command(query)
