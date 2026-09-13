# Voice Assistant (Beginner Tier)

## Project Description

A simple, beginner-friendly Python voice assistant that listens to spoken
commands through a microphone and responds using text-to-speech. It can
greet the user, tell the current time and date, perform a web search, and
exit safely on command.

This project was built as part of an internship task in the **Python
Programming Track (Beginner Tier)**.

## Objective

Build a Python-based voice assistant that:
- Listens to spoken commands through a microphone.
- Converts speech to text using an online speech recognition service.
- Responds to the user using synthesized speech (text-to-speech).
- Performs a small set of useful, beginner-appropriate actions.

## Features

- **Voice input** via microphone with ambient noise calibration.
- **Greeting response** — recognizes "hello" / "hi" and responds verbally.
- **Current time** — speaks the current system time.
- **Current date** — speaks the current system date.
- **Web search** — opens a Google search in the default browser for any
  query the user speaks (not hardcoded to one topic).
- **Graceful error handling** — never crashes on unrecognized speech,
  network issues, or microphone problems.
- **Text-to-speech for every response** using `pyttsx3`.
- **Exit command** — safely stops the program on "exit", "quit", "stop",
  or "goodbye".

## Technologies Used

- Python 3.11+
- [`SpeechRecognition`](https://pypi.org/project/SpeechRecognition/) (imported as `speech_recognition`)
- [`pyttsx3`](https://pypi.org/project/pyttsx3/)
- [`PyAudio`](https://pypi.org/project/PyAudio/) (required by `SpeechRecognition` for microphone access)
- Built-in modules: `datetime`, `webbrowser`, `urllib.parse`, `sys`

No external AI APIs, databases, or GUI frameworks are used.

## Project Structure

```
VoiceAssistant/
│
├── voice_assistant.py     # Main application code
├── requirements.txt       # Third-party dependencies
├── README.md               # Project documentation
├── .gitignore               # Files/folders excluded from git
└── screenshots/
    └── .gitkeep
```

## Required Python Version

Python **3.11 or newer** is recommended.

## Installation Instructions

### 1. Clone or download the project

Place the `VoiceAssistant` folder anywhere on your computer.

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

> **Windows note:** If `PyAudio` fails to install directly with `pip`,
> install it using a precompiled wheel instead:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

## How to Run the Project

With the virtual environment activated:

```bash
python voice_assistant.py
```

The assistant will:
1. Initialize the text-to-speech engine.
2. Speak a startup greeting.
3. Calibrate the microphone for ambient noise.
4. Begin listening for commands.

## Enabling Microphone Permissions on Windows

1. Open **Settings** → **Privacy & security** → **Microphone**.
2. Ensure **"Microphone access"** is turned **On**.
3. Ensure **"Let apps access your microphone"** is turned **On**.
4. Ensure your terminal application (Command Prompt, PowerShell, or VS
   Code's terminal) is allowed under **"Let desktop apps access your
   microphone"**.
5. Confirm the correct microphone is set as the **default recording
   device** in **Control Panel → Sound → Recording**.

## How the Assistant Works

1. The program starts and initializes `pyttsx3` for speech output.
2. It greets the user out loud.
3. It calibrates the microphone using `adjust_for_ambient_noise()` to
   reduce background noise interference.
4. It listens for a spoken command with a timeout and phrase time limit,
   so it never hangs indefinitely.
5. The captured audio is sent to Google's speech recognition service via
   `recognizer.recognize_google(audio)`.
6. The recognized text is printed to the console and matched against
   known command keywords.
7. The appropriate action is performed, and the response is always
   spoken aloud using `pyttsx3`.
8. The assistant keeps listening in a loop until an exit command is
   spoken.

## Example Voice Commands

| Say this...                     | Assistant does...                                   |
|----------------------------------|------------------------------------------------------|
| "Hello"                          | Responds with a spoken greeting                      |
| "What time is it?"               | Speaks the current time                              |
| "What is today's date?"          | Speaks the current date                              |
| "Search for Python tutorials"    | Opens a Google search for "Python tutorials"         |
| "Search for machine learning"    | Opens a Google search for "machine learning"         |
| "Goodbye"                        | Speaks a farewell and exits the program              |

## Error Handling

The assistant handles the following situations without crashing:

- **Unrecognized speech** (`speech_recognition.UnknownValueError`) —
  responds with "Sorry, I didn't understand that. Please repeat." and
  keeps listening.
- **Speech service unavailable** (`speech_recognition.RequestError`) —
  speaks a message about the service being unavailable and continues
  running.
- **No speech detected in time** — silently returns to listening again.
- **Microphone/audio device errors** — informs the user verbally and
  avoids crashing.
- **Unexpected exceptions** — caught by a general handler that reports
  the issue and keeps the program alive wherever possible.

## Limitations

- Requires an active internet connection, since it relies on Google's
  free web speech recognition service.
- Speech recognition accuracy depends on microphone quality, accent, and
  background noise.
- Only supports the commands described above (no natural language
  understanding, weather, smart home, or email features).
- `pyttsx3` voice quality and available voices depend on the operating
  system's installed speech engines.
- Not designed for continuous multi-turn conversations or context
  memory between commands.

## Privacy Considerations

- This application listens to microphone input only while actively
  waiting for a command.
- Captured audio is converted to text using Google's speech recognition
  service through the `SpeechRecognition` library. This means audio may
  be sent to Google's servers for processing as part of the recognition
  request.
- The application does **not** intentionally save, store, or log any
  voice recordings to disk.
- No database is used, and no personal data is persisted between runs.
- **Do not** speak passwords, financial details, or other sensitive
  personal information to the assistant.

## Future Improvements

- Add offline speech recognition (e.g., Vosk or PocketSphinx) to remove
  the internet dependency.
- Add wake-word detection ("Hey Assistant") instead of continuous
  listening.
- Support additional commands (reminders, notes, calculations).
- Add a simple GUI for visual feedback.
- Support multiple languages.

## Internship Task Information

- **Project:** Voice Assistant
- **Track:** Python Programming
- **Tier:** Beginner
- **Scope:** Implements only the mandatory Beginner Tier requirements —
  voice input, greeting response, time, date, web search, error
  handling, text-to-speech, and a safe exit command. No advanced
  features (NLP, weather APIs, email, smart home control, or
  transformers) were added, per task instructions.

---

## Testing Checklist

Use this checklist to verify every mandatory requirement works correctly:

- [ ] **1. Program starts successfully** — running `python voice_assistant.py`
      launches without errors and speaks a startup greeting.
- [ ] **2. Microphone is detected** — the console shows "Calibrating
      microphone..." followed by "Calibration complete." without errors.
- [ ] **3. "Hello" receives a spoken response** — say "hello" or "hi" and
      confirm the assistant replies "Hello! How can I help you?" audibly.
- [ ] **4. Time command works** — ask "What time is it?" and confirm the
      spoken response matches your system clock.
- [ ] **5. Date command works** — ask "What is today's date?" and confirm
      the spoken response matches today's date.
- [ ] **6. Web search opens correctly** — say "Search for Python
      tutorials" and confirm your default browser opens a Google search
      for "Python tutorials".
- [ ] **7. Unrecognized speech is handled gracefully** — stay silent or
      mumble something unclear; confirm the assistant says "Sorry, I
      didn't understand that. Please repeat." and keeps running.
- [ ] **8. Speech recognition service errors are handled** — disconnect
      your internet connection and speak a command; confirm the assistant
      reports the service is unavailable instead of crashing.
- [ ] **9. Exit command closes the program** — say "exit", "quit", "stop",
      or "goodbye" and confirm the assistant speaks a farewell and the
      program terminates.
- [ ] **10. No required feature crashes the application** — run through
      all commands above in sequence and confirm the program keeps
      running (except after the exit command) with no unhandled
      exceptions or crashes.

## 🎥 Demo Video

[Watch the Task 1 Voice Assistant Demo on LinkedIn](https://www.linkedin.com/posts/tarun-sonaji-8161b6332_oasisinfobyte-python-pythonprogramming-ugcPost-7504445301110448128-lVKV/?utm_source=social_share_send&utm_medium=android_app&rcm=ACoAAFOt1BIBnLaTO5l8x_KvLks41x1yXCzpgXk&utm_campaign=copy_link)