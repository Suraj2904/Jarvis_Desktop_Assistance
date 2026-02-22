
import webbrowser
import subprocess
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import os

from openai import OpenAI
from config import apikey

client = OpenAI(api_key=apikey)
chatstr = ''

# 0 = Male voice  |  1 = Female voice
_VOICE_INDEX = 1


# =============================================================================
#  SAY  — fresh engine every call (fixes the "speaks only once" bug on Windows)
# =============================================================================

def say(text: str) -> None:
    """Speak text aloud. Reinitialises pyttsx3 each call to fix SAPI5 silence bug."""
    print(f"[Jarvis] {text}")
    try:
        engine = pyttsx3.init('sapi5')          # fresh instance every time
        voices = engine.getProperty('voices')
        if _VOICE_INDEX < len(voices):
            engine.setProperty('voice', voices[_VOICE_INDEX].id)
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.1)
        engine.say(text)
        engine.runAndWait()
        engine.stop()                           # cleanly release SAPI5 resources
    except Exception as e:
        print(f"[TTS Error] {e}")


# =============================================================================
#  CHAT  — GPT via openai v1.0+
# =============================================================================

def chat(prompt: str) -> str:
    global chatstr
    chatstr += f"User: {prompt}\nJarvis: "
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful voice assistant. "
                                               "Keep replies short and conversational."},
                {"role": "user",   "content": chatstr}
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = "Sorry, I encountered an error."
        print(f"[OpenAI Error] {e}")

    say(reply)
    chatstr += f"{reply}\n"
    return reply


# =============================================================================
#  GREET
# =============================================================================

def wishMe() -> None:
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        say("Good Morning!")
    elif 12 <= hour < 18:
        say("Good Afternoon!")
    else:
        say("Good Evening!")
    say("I am Jarvis sir. I am your Voice Assistant.")


# =============================================================================
#  GET NAME
# =============================================================================

def getName() -> None:
    global uname
    say("Can I please know your name?")
    uname = takeCommand()
    if uname:
        say(f"Nice to meet you, {uname}!")
    else:
        uname = "sir"


# =============================================================================
#  LISTEN
# =============================================================================

def takeCommand() -> str | None:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Listening...]")
        r.adjust_for_ambient_noise(source, duration=0.3)
        r.energy_threshold = 500
        r.pause_threshold  = 1
        audio = r.listen(source)

    try:
        print("[Recognizing...]")
        query = r.recognize_google(audio, language='en-IN')
        print(f"[You] {query}")
        return query
    except sr.UnknownValueError:
        say("Say that again please.")
    except sr.RequestError:
        say("Speech service unavailable.")
    return None


# =============================================================================
#  MAIN
# =============================================================================

if __name__ == "__main__":
    wishMe()
    getName()

    sites = [
        ["YouTube",   "https://www.youtube.com/"],
        ["Google",    "https://www.google.com/"],
        ["Instagram", "https://www.instagram.com/"],
        ["ChatGPT",   "https://chat.openai.com/"],
        ["Wikipedia", "https://wikipedia.org/"],
        ["Facebook",  "https://www.facebook.com/"],
    ]

    while True:
        query = takeCommand()
        if query is None:
            continue
        query = query.lower()

        # ── Open websites ──────────────────────────────────────────────────────
        opened = False
        for site in sites:
            if f"open {site[0].lower()}" in query:
                say(f"Opening {site[0]} sir.")
                webbrowser.open(site[1])
                opened = True
                break
        if opened:
            continue

        # ── Play music ─────────────────────────────────────────────────────────
        if "play music" in query:
            music_dir = 'C:\\Users\\suraj\\OneDrive\\Desktop\\music'
            if os.path.isdir(music_dir):
                songs = os.listdir(music_dir)
                if songs:
                    say("Playing music sir.")
                    os.startfile(os.path.join(music_dir, songs[0]))
                else:
                    say("No songs found in the music folder.")
            else:
                say("Music folder not found.")

        # ── Time ──────────────────────────────────────────────────────────────
        elif "time" in query:
            t = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir, the time is {t}.")

        # ── CMD ───────────────────────────────────────────────────────────────
        elif "open cmd" in query:
            say("Opening Command Prompt.")
            subprocess.Popen("cmd.exe")

        # ── Wikipedia ─────────────────────────────────────────────────────────
        elif "wikipedia" in query:
            say("Searching Wikipedia...")
            search = query.replace("using wikipedia", "").replace("wikipedia", "").strip()
            try:
                result = wikipedia.summary(search, sentences=2)
                say("According to Wikipedia.")
                say(result)
            except wikipedia.exceptions.DisambiguationError as e:
                say(f"That topic is ambiguous. Did you mean {e.options[0]}?")
            except Exception:
                say("Sorry, I could not find that on Wikipedia.")

        # ── Notepad ───────────────────────────────────────────────────────────
        elif "notepad" in query:
            try:
                subprocess.Popen("notepad.exe")
                say("Notepad opened successfully.")
            except Exception as e:
                say("Sorry, I couldn't open Notepad.")
                print(e)

        # ── Chrome ────────────────────────────────────────────────────────────
        elif "chrome" in query:
            try:
                os.system("start chrome")
                say("Google Chrome opened successfully.")
            except Exception as e:
                say("Sorry, I couldn't open Google Chrome.")
                print(e)

        # ── Chat ──────────────────────────────────────────────────────────────
        elif "chat" in query or "ask" in query:
            say("Sure, what would you like to ask?")
            prompt = takeCommand()
            if prompt:
                chat(prompt)

        # ── Exit ──────────────────────────────────────────────────────────────
        elif any(kw in query for kw in ["exit","Close", "bye", "goodbye"]):
            say("Goodbye sir. Have a nice day!")
            break