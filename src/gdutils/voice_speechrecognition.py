# from https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py

#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

from typing import Optional
import speech_recognition as sr


def recognise_speech(display: Optional[str], verbose: int = 0):
    if display:
        print(display, end="", flush=True)
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Say something!")
        audio = r.listen(source)
    print("... PROCESSING")
    # recognize speech using Whisper API
    # try:
    #     print(f"Whisper API thinks you said {r.recognize_whisper_api(audio, api_key=OPENAI_API_KEY)}")
    # except sr.RequestError as e:
    #     print("Could not request results from Whisper API")
    text = r.recognize_whisper_api(audio, api_key=OPENAI_API_KEY)
    if verbose > 0:
        print(text)
    return text


if __name__ == "__main__":
    recognise_speech("Say something!", verbose=1)

# # recognize speech using Google Speech Recognition
# try:
#     # for testing purposes, we're just using the default API key
#     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#     # instead of `r.recognize_google(audio)`
#     print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
# except sr.UnknownValueError:
#     print("Google Speech Recognition could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Speech Recognition service; {0}".format(e))

# # recognize speech using Google Cloud Speech
# try:
#     print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=GCLOUD_SERVICE_ACCOUNT_JSON_FILEN))
# except sr.UnknownValueError:
#     print("Google Cloud Speech could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Cloud Speech service; {0}".format(e))

# # # recognize speech using Microsoft Bing Voice Recognition
# # BING_KEY = "INSERT BING API KEY HERE"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
# # try:
# #     print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
# # except sr.UnknownValueError:
# #     print("Microsoft Bing Voice Recognition could not understand audio")
# # except sr.RequestError as e:
# #     print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

# # # recognize speech using Microsoft Azure Speech
# # AZURE_SPEECH_KEY = "INSERT AZURE SPEECH API KEY HERE"  # Microsoft Speech API keys 32-character lowercase hexadecimal strings
# # try:
# #     print("Microsoft Azure Speech thinks you said " + r.recognize_azure(audio, key=AZURE_SPEECH_KEY))
# # except sr.UnknownValueError:
# #     print("Microsoft Azure Speech could not understand audio")
# # except sr.RequestError as e:
# #     print("Could not request results from Microsoft Azure Speech service; {0}".format(e))
