import os
from typing import Optional
from gjdutils.env import get_env_var


def outloud(
    text: str,
    mp3_filen: str,
    prog: str,
    language_code: Optional[str] = None,
    bot_gender: Optional[str] = None,
    bot_name: Optional[str] = None,
    speed: Optional[str] = None,  # or 'slow'
    play: bool = False,
    verbose: int = 0,
):
    if prog == "google":
        response = outloud_google(
            text=text,
            mp3_filen=mp3_filen,  # type: ignore
            language_code=language_code,  # type: ignore
            bot_gender=bot_gender,
            speed=speed,
            verbose=verbose,
        )
    elif prog == "azure":
        response = outloud_azure(
            text=text,
            mp3_filen=mp3_filen,
            language_code=language_code,
            bot_gender=bot_gender,
            bot_name=bot_name,
            speed=speed,
            verbose=verbose,
        )
    elif prog == "elevenlabs":
        assert speed is None, "speed not supported for elevenlabs"
        response = outloud_elevenlabs(
            text=text,
            mp3_filen=mp3_filen,
            bot_name=bot_name,
            # speed=speed,
            verbose=verbose,
        )
    else:
        raise Exception(f"Unknown PROG '{prog}'")
    if play:
        from .audios import play_mp3

        play_mp3(mp3_filen, prog="cli")
    return response


def outloud_azure(
    text: str,
    mp3_filen: str,
    language_code: Optional[str] = "en-GB",
    bot_gender: Optional[str] = None,
    bot_name: Optional[str] = None,
    speed: Optional[str] = None,  # or 'slow'
    verbose: int = 0,
):
    """
    from https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?pivots=programming-language-python&tabs=macos%2Cterminal
    """
    import azure.cognitiveservices.speech as speechsdk

    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(
        subscription=get_env_var("SPEECH_KEY"),
        region=get_env_var("SPEECH_REGION"),
    )
    # https://learn.microsoft.com/en-us/answers/questions/693848/can-azure-text-to-speech-support-more-audio-files.html
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )
    audio_config = speechsdk.audio.AudioOutputConfig(
        use_default_speaker=True, filename=mp3_filen
    )

    # The language of the voice that speaks.
    # speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    speech_config.speech_synthesis_voice_name = bot_name  # type: ignore

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # ssml = f'<speak><prosody rate="30%">{text}</prosody></speak>'
    ssml = f"""
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="{bot_name}">
        <prosody rate="slow">
            {text}
        </prosody>
    </voice>
</speak>
    """.strip()
    # print(ssml)

    # speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml).get()

    if (
        speech_synthesis_result.reason  # type: ignore
        == speechsdk.ResultReason.SynthesizingAudioCompleted
    ):
        if verbose > 0:
            print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:  # type: ignore
        cancellation_details = speech_synthesis_result.cancellation_details  # type: ignore
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

    return speech_synthesis_result


def outloud_google(
    text: str,
    mp3_filen: str,
    language_code: str = "en-GB",
    bot_gender=None,
    speed=None,  # or 'slow'
    verbose: int = 0,
):
    from google.cloud import texttospeech

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
        raise Exception("Unknown gender: %s" % bot_gender)
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    if speed is None:
        synthesis_input = texttospeech.SynthesisInput(text=text)
    elif speed == "slow":
        # https://stackoverflow.com/questions/68742170/google-clouds-rate-and-pitch-prosody-attributes
        # ssml = f'<speak><prosody rate="slow">{text}</prosody></speak>'
        ssml = f'<speak><prosody rate="100%">{text}</prosody></speak>'
        synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    else:
        raise Exception(f"Unknown SPEED '{speed}'")
    # synthesis_input = texttospeech.SynthesisInput(text="Bonjour, Monsieur Natterbot!")
    # synthesis_input = texttospeech.SynthesisInput(text="Γεια σου, Natterbot!")

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,  # e.g. 'en-GB'
        ssml_gender=bot_gender,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(mp3_filen, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)  # type: ignore
        if verbose > 0:
            print(f"Audio content written to {mp3_filen}")

    return response


def outloud_elevenlabs(
    text: str,
    api_key: Optional[str] = None,
    mp3_filen: Optional[str] = None,
    bot_name: Optional[str] = None,
    model: str = "eleven_multilingual_v2",
    # speed=None,
    should_play: bool = False,
    verbose: int = 0,
):
    from elevenlabs import play, save
    from elevenlabs.client import ElevenLabs

    if api_key is None:
        api_key = get_env_var("ELEVENLABS_API_KEY")
    # i should figure out a better way to handle playing an mp3 file
    # assert (
    #     not mp3_filen and should_play
    # ), "Writing out uses up the bytes, so you can't then play"
    assert model in ["eleven_multilingual_v2", "eleven_turbo_v2_5"]
    # if speed is not None:
    #     raise Exception(f"Unknown SPEED '{speed}'")
    if bot_name is None:
        bot_name = "Charlotte"  # slower

    client = ElevenLabs(
        api_key=api_key,
    )
    audio = client.generate(
        text=text,
        voice=bot_name,
        model=model,
    )
    if mp3_filen is not None:
        save(audio, mp3_filen)  # type: ignore
    if should_play:
        if mp3_filen is None:
            play(audio)
        else:
            # if you've already saved, it will consume the bytes
            from .audios import play_mp3

            play_mp3(mp3_filen, prog="cli")
    return audio


# mp3_filen = TEMP_MP3_FILEN
# # response = outloud(text="Hello Natterbot!", mp3_filen=mp3_filen, language_code='en-GB')
# response = outloud(text="γεια σου", mp3_filen=mp3_filen, language_code='el')
