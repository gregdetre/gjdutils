# from https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py

#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

from typing import Optional
import speech_recognition as sr
from gjdutils.env import get_env_var


def recognise_speech(display: Optional[str], verbose: int = 0):
    """
    Recognises speech from the microphone and returns the transcribed text.

    Press ENTER when you've finished recording.

    Designed for command-line use.
    """
    openai_api_key = get_env_var("OPENAI_API_KEY")
    if display:
        print(display, end="", flush=True)
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    print("... PROCESSING")
    text = r.recognize_whisper(audio, api_key=openai_api_key)
    if verbose > 0:
        print(text)
    return text


if __name__ == "__main__":
    recognise_speech("Say something!", verbose=1)
