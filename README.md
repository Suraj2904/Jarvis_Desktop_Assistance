# 🤖 Jarvis — Python Desktop Voice Assistant

A fully voice-driven personal desktop assistant built with Python. Jarvis listens to your voice, speaks every reply out loud, opens websites, searches Wikipedia, tells the time, plays music, and holds AI-powered conversations using GPT-3.5-turbo.

---

## 📁 Project Structure

```
jarvisAI/
│
├── main.py          # Core assistant — all features and voice logic
├── openaitest.py    # Quick script to test your OpenAI API connection
├── config.py        # Your API keys 
└── README.md        # This file
```

---

## ✅ Features

| Feature | Voice Command Example |
|---|---|
| 🌐 Open websites | *"Open YouTube"* / *"Open Google"* / *"Open Instagram"* |
| 🎵 Play music | *"Play music"* |
| 🕐 Tell the time | *"Time"* |
| 📖 Wikipedia search | *"Wikipedia Elon Musk"* / *"Using Wikipedia Python"* |
| 📝 Open Notepad | *"Notepad"* |
| 🌍 Open Chrome | *"Chrome"* |
| 💻 Open CMD | *"Open CMD"* |
| 🤖 AI Chat (GPT-3.5) | *"Chat"* / *"Ask something"* |
| 👋 Exit | *"Goodbye"* / *"Bye"* / *"Exit"* |

---

## ⚙️ Requirements

- **Python 3.10+**
- **Windows OS** — uses Windows SAPI5 voice engine via pyttsx3
- **Microphone** connected and set as default input device
- **Internet connection** — needed for speech recognition, Wikipedia, and OpenAI

---

## 📦 Installation

### Step 1 — Install all dependencies

```bash
pip install speechrecognition pyaudio pyttsx3 openai wikipedia requests
```

> ⚠️ If `pyaudio` fails on Windows, run:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### Step 2 — Create `config.py`

Create a file named `config.py` in the same folder as `main.py`:

```python
apikey: str = "YOUR_OPENAI_API_KEY_HERE"
```

Get your key from: https://platform.openai.com/api-keys

> The AI Chat feature requires a valid OpenAI key.
> All other features (voice, time, music, Wikipedia, websites) work without it.

### Step 3 — Update your music folder path

In `main.py`, find and update this line to your actual music folder:

```python
music_dir = 'C:\\Users\\suraj\\OneDrive\\Desktop\\music'
```

---

## ▶️ How to Run

### Run the full assistant:
```bash
python main.py
```

Jarvis will:
1. Greet you based on the time of day (morning / afternoon / evening)
2. Ask for your name and greet you personally
3. Start listening for voice commands in a continuous loop

### Test your OpenAI connection first:
```bash
python openaitest.py
```
Sends a test prompt to GPT-3.5-turbo and prints the reply.
If it works, your API key is valid and chat will work in `main.py`.

---

## 🎤 Full Voice Command Reference

### 🌐 Open Websites
```
"Open YouTube"
"Open Google"
"Open Instagram"
"Open ChatGPT"
"Open Wikipedia"
"Open Facebook"
```

### 💻 Open Apps
```
"Open CMD"    → opens Command Prompt
"Notepad"     → opens Notepad
"Chrome"      → opens Google Chrome
```

### ℹ️ Information
```
"Time"                               → speaks the current time
"Wikipedia artificial intelligence"  → searches and reads a Wikipedia summary
"Using Wikipedia Taj Mahal"          → alternate phrasing, same result
```

### 🎵 Music
```
"Play music"    → plays the first song in your music folder
```

### 🤖 AI Chat
```
"Chat"    → Jarvis asks what you'd like to know, speaks GPT's reply aloud
"Ask"     → same trigger
```
> Chat is fully voice-in, voice-out. Jarvis remembers context within the session.

### 👋 Exit
```
"Goodbye"
"Bye"
"Exit"
```

---

## 🔧 Customisation

### Change voice gender
In `main.py` near the top:
```python
_VOICE_INDEX = 0   # 0 = Male voice
_VOICE_INDEX = 1   # 1 = Female voice  ← currently active
```

### Change speaking speed
Inside the `say()` function:
```python
engine.setProperty('rate', 170)   # words per minute — lower is slower
```

### Change the music folder
```python
music_dir = 'C:\\Users\\YourName\\Music'   # replace with your actual path
```

### Add more websites
In the `sites` list inside `main.py`:
```python
sites = [
    ["YouTube",  "https://www.youtube.com/"],
    ["Twitter",  "https://twitter.com/"],      # ← add entries like this
    ["LinkedIn", "https://linkedin.com/"],
]
```

---

## 🔍 How It Works

```
You speak
    ↓
Microphone captures audio           (pyaudio)
    ↓
Google converts audio to text       (speechrecognition)
    ↓
main.py matches text to a command
    ↓
Jarvis performs the action
    ↓
pyttsx3 speaks the reply aloud      (Windows SAPI5)
    ↓
Loop repeats — waiting for next command
```

---

## 🛠️ Technical Notes

### Why pyttsx3 is reinitialised on every `say()` call

Windows SAPI5 has a known bug where a globally shared `pyttsx3` engine
stops producing audio after the first `runAndWait()` call. The fix used here
is to create a fresh instance every time and call `engine.stop()` to cleanly
release COM resources:

```python
def say(text):
    engine = pyttsx3.init('sapi5')   # fresh instance — guarantees audio every time
    ...
    engine.runAndWait()
    engine.stop()                    # release SAPI5 COM object
```

### Why `from openai import OpenAI` instead of `import openai`

`openai.ChatCompletion.create()` was removed in `openai >= 1.0.0`.
Both files use the current v1.0+ client style:

```python
from openai import OpenAI
client = OpenAI(api_key=apikey)
response = client.chat.completions.create(...)
reply = response.choices[0].message.content   # dot notation, not dict keys
```

---

## 📋 Dependencies

| Package | Purpose |
|---|---|
| `speechrecognition` | Converts microphone audio to text via Google |
| `pyaudio` | Gives Python access to the microphone |
| `pyttsx3` | Offline text-to-speech — Jarvis's voice output |
| `openai` | GPT-3.5-turbo AI chat (v1.0+ API) |
| `wikipedia` | Fetches and summarises Wikipedia articles |
| `webbrowser` | Opens URLs in the default browser |
| `subprocess` | Launches apps like Notepad and CMD |
| `datetime` | Gets current time and date |
| `os` | File system access, runs system commands |

---

## 🔐 Security

**Never commit `config.py` to GitHub** — it contains your secret API key.

Add this to your `.gitignore`:
```
config.py
```

Share the project publicly with a `config.py` template instead:
```python
# config.py  — add your own key here
apikey: str = "YOUR_OPENAI_API_KEY_HERE"
```

---

## 🚀 Possible Future Improvements

- [ ] Wake word (*"Hey Jarvis"*) so it listens passively
- [ ] Weather forecast by city name
- [ ] Voice-set reminders with countdown timer
- [ ] Music controls by voice (pause, next, volume)
- [ ] GUI with live conversation history
- [ ] Multi-language support

---

## 👨‍💻 Author

**Suraj**
A Python learning project — a voice assistant inspired by Iron Man's J.A.R.V.I.S.

---

## 📄 License

This project is intended for educational and personal use only.
