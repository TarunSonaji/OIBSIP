"""
Voice Assistant - Beginner Tier
Internship Project - Python Programming Track

A simple voice-controlled assistant that listens to spoken commands
through the microphone and responds using text-to-speech.

Supported commands:
    - Greetings (hello / hi)
    - Current time
    - Current date
    - Web search
    - Exit / quit / stop / goodbye
"""

import sys
import datetime
import webbrowser
import urllib.parse
import os
import speech_recognition as sr
import pyttsx3


# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------

# How long (seconds) to wait for the user to START speaking before giving up.
LISTEN_TIMEOUT = 5

# Maximum length (seconds) of a single spoken phrase.
PHRASE_TIME_LIMIT = 8

# Speech rate (words per minute) for the TTS engine.
TTS_RATE = 175

# Keywords used for simple command matching.
GREETING_KEYWORDS = ["hello", "hi", "hey"]
TIME_KEYWORDS = ["time"]
DATE_KEYWORDS = ["date", "today"]
SEARCH_KEYWORDS = ["search"]
OPEN_KEYWORDS = ["open", "launch", "start"]
YOUTUBE_KEYWORDS = ["youtube"]
EXIT_KEYWORDS = ["exit", "quit", "stop", "goodbye", "bye"]


# ---------------------------------------------------------------------------
# Text-to-Speech
# ---------------------------------------------------------------------------

def init_tts_engine():
    """
    Initialize and configure the pyttsx3 text-to-speech engine.

    Returns:
        pyttsx3.Engine: A configured TTS engine instance.
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", TTS_RATE)
    engine.setProperty("volume", 1.0)
    return engine


def speak(engine, text):
    """
    Speak the given text out loud and also print it to the console
    for debugging/visibility purposes.

    Args:
        engine (pyttsx3.Engine): The TTS engine instance.
        text (str): The text to be spoken.
    """
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


# ---------------------------------------------------------------------------
# Voice Input
# ---------------------------------------------------------------------------

def init_recognizer_and_microphone():
    """
    Initialize the SpeechRecognition Recognizer and Microphone objects,
    and calibrate the recognizer for ambient noise.

    Returns:
        tuple: (recognizer, microphone)
    """
    recognizer = sr.Recognizer()

    try:
        microphone = sr.Microphone()
    except OSError as error:
        print(f"Error: Could not access a microphone. Details: {error}")
        sys.exit(1)

    # Calibrate for ambient noise once at startup.
    with microphone as source:
        print("Calibrating microphone for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Calibration complete.")

    return recognizer, microphone


def listen(recognizer, microphone, engine):
    """
    Listen for a single voice command through the microphone and
    convert it to text using Google's speech recognition service.

    Handles all speech-recognition and audio related errors gracefully,
    speaking a helpful message and returning None so the main loop can
    continue listening instead of crashing.

    Args:
        recognizer (sr.Recognizer): The speech recognizer instance.
        microphone (sr.Microphone): The microphone instance.
        engine (pyttsx3.Engine): The TTS engine, used for error messages.

    Returns:
        str or None: The recognized command in lowercase, or None if
        nothing usable was recognized.
    """
    try:
        with microphone as source:
            print("Listening...")
            audio = recognizer.listen(
                source,
                timeout=LISTEN_TIMEOUT,
                phrase_time_limit=PHRASE_TIME_LIMIT,
            )

        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        command = command.lower().strip()
        print(f"You said: {command}")
        return command

    except sr.WaitTimeoutError:
        # No speech detected within the timeout window; simply try again.
        print("No speech detected within the timeout window.")
        return None

    except sr.UnknownValueError:
        # Speech was detected but could not be understood.
        speak(engine, "Sorry, I didn't understand that. Please repeat.")
        return None

    except sr.RequestError as error:
        # The speech recognition service is unreachable or returned an error.
        print(f"Speech recognition service error: {error}")
        speak(
            engine,
            "Sorry, the speech recognition service is unavailable right now. "
            "Please check your internet connection and try again.",
        )
        return None

    except OSError as error:
        # Microphone/audio device related errors.
        print(f"Microphone/audio error: {error}")
        speak(engine, "There was a problem accessing the microphone.")
        return None

    except Exception as error:  # pylint: disable=broad-except
        # Catch-all for any unexpected issue so the program never crashes.
        print(f"Unexpected error while listening: {error}")
        speak(engine, "Something went wrong while listening. Please try again.")
        return None


# ---------------------------------------------------------------------------
# Command Handlers
# ---------------------------------------------------------------------------

def handle_greeting(engine):
    """Respond to a greeting command."""
    speak(engine, "Hello! How can I help you?")


def handle_time(engine):
    """Speak the current system time."""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(engine, f"The current time is {current_time}.")


def handle_date(engine):
    """Speak the current system date."""
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(engine, f"Today's date is {current_date}.")


def extract_search_query(command):
    """
    Extract the search query from a voice command such as
    "search for python tutorials" or "search web for machine learning".

    Args:
        command (str): The full recognized voice command.

    Returns:
        str: The extracted search query, or an empty string if none found.
    """
    query = command

    # Remove common leading phrases so only the actual query remains.
    prefixes_to_remove = [
        "search web for",
        "search the web for",
        "search for",
        "search",
    ]

    for prefix in prefixes_to_remove:
        if prefix in query:
            query = query.split(prefix, 1)[1]
            break

    return query.strip()


def handle_web_search(engine, command):
    """
    Extract a search query from the command, open the default web
    browser with a Google search for that query, and confirm verbally.

    Args:
        engine (pyttsx3.Engine): The TTS engine instance.
        command (str): The full recognized voice command.
    """
    query = extract_search_query(command)

    if not query:
        speak(engine, "I didn't catch what you want me to search for. Please try again.")
        return

    speak(engine, f"Searching the web for {query}.")

    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://www.google.com/search?q={encoded_query}"

    try:
        webbrowser.open(search_url)
    except Exception as error:  # pylint: disable=broad-except
        print(f"Error opening web browser: {error}")
        speak(engine, "Sorry, I could not open the web browser.")
        #for websites opening
def handle_open_website(engine, command):
    """Open a commonly requested website."""

    if "youtube" in command:
        speak(engine, "Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "google" in command:
        speak(engine, "Opening Google.")
        webbrowser.open("https://www.google.com")

    elif "github" in command:
        speak(engine, "Opening GitHub.")
        webbrowser.open("https://github.com")

    elif "linkedin" in command:
        speak(engine, "Opening LinkedIn.")
        webbrowser.open("https://www.linkedin.com")

    elif "instagram" in command:
        speak(engine, "Opening Instagram.")
        webbrowser.open("https://www.instagram.com")

    else:
        speak(
            engine,
            "I can open Google, YouTube, GitHub, LinkedIn, or Instagram."
        )
        
def handle_exit(engine):
    """Speak a farewell message. Program termination is handled by the caller."""
    speak(engine, "Goodbye! Have a great day.")


# ---------------------------------------------------------------------------
# Command Processing / Routing
# ---------------------------------------------------------------------------

def is_exit_command(command):
    """Check whether the command indicates the user wants to exit."""
    return any(keyword in command for keyword in EXIT_KEYWORDS)


def process_command(engine, command):
    """
    Determine which action to perform based on the recognized command
    and call the corresponding handler.

    Args:
        engine (pyttsx3.Engine): The TTS engine instance.
        command (str): The recognized voice command (lowercase).

    Returns:
        bool: True if the assistant should continue running,
              False if it should exit.
    """
    if is_exit_command(command):
        handle_exit(engine)
        return False

    if any(keyword in command for keyword in GREETING_KEYWORDS):
        handle_greeting(engine)
        
    elif any(keyword in command for keyword in OPEN_KEYWORDS):
        handle_open_website(engine, command)
        
    elif any(keyword in command for keyword in SEARCH_KEYWORDS):
        handle_web_search(engine, command)

    elif any(keyword in command for keyword in TIME_KEYWORDS):
        handle_time(engine)

    elif any(keyword in command for keyword in DATE_KEYWORDS):
        handle_date(engine)

    else:
        speak(
            engine,
            "Sorry, I don't know how to help with that yet. "
            "You can ask me for the time, the date, to search something, "
            "or say hello.",
        )

    return True


# ---------------------------------------------------------------------------
# Main Application Flow
# ---------------------------------------------------------------------------

def main():
    """Run the voice assistant's main loop."""
    engine = init_tts_engine()

    print("Starting Voice Assistant...")
    speak(engine, "Voice assistant is starting up.")

    recognizer, microphone = init_recognizer_and_microphone()

    speak(engine, "Hello! I am your voice assistant. How can I help you today?")

    running = True
    while running:
        command = listen(recognizer, microphone, engine)

        if command is None:
            # Nothing usable was recognized; loop back and listen again.
            continue

        running = process_command(engine, command)

    print("Voice Assistant has stopped.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nVoice Assistant interrupted by user. Exiting safely.")
        sys.exit(0)
