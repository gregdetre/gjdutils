"""
Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.
https://cloud.google.com/text-to-speech/docs/libraries
"""

from google.cloud import texttospeech


def outloud(text: str, language_code: str = "en-GB", bot_gender=None):
    bot_gender = bot_gender.lower() if bot_gender else None
    # not all genders supported for all languages. see https://cloud.google.com/text-to-speech/docs/voices
    if bot_gender is None or bot_gender == "neutral":
        bot_gender = texttospeech.SsmlVoiceGender.NEUTRAL
    elif bot_gender in ["female", texttospeech.SsmlVoiceGender.FEMALE]:
        bot_gender = texttospeech.SsmlVoiceGender.FEMALE
    elif bot_gender in ["male", texttospeech.SsmlVoiceGender.MALE]:
        bot_gender = texttospeech.SsmlVoiceGender.MALE
    else:
        # gender = texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED
        raise Exception(f"Unknown gender: {bot_gender}")
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)
    # synthesis_input = texttospeech.SynthesisInput(text="Bonjour, Monsieur Natterbot!")
    # synthesis_input = texttospeech.SynthesisInput(text="Γεια σου, Natterbot!")

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=bot_gender
    )  # e.g. 'en-GB'

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response
