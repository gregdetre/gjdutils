from google.cloud import translate_v2 as translate
import html
from typing import Optional


def translate_text(
    text: str,
    lang_src_code: Optional[str],
    lang_tgt_code: str,
    verbose: int = 0,
):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages

    e.g.
        translated_text, result = translate_text(
            text="Hello, world",
            lang_src_code="en",
            lang_tgt_code="el",
            verbose=0,
        )
    """
    translate_client = translate.Client()

    lang_src_code = (
        lang_src_code[:2].lower() if isinstance(lang_src_code, str) else None
    )
    lang_tgt_code = lang_tgt_code[:2].lower()
    if lang_src_code == lang_tgt_code:
        return text, None

    # assert lang_src_code != lang_tgt_code, (
    #     "Identical src and tgt language codes: %s" % lang_src_code
    # )

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    if lang_src_code is None:
        result = translate_client.translate(text, target_language=lang_tgt_code)
    else:
        result = translate_client.translate(
            text,
            target_language=lang_tgt_code,
            source_language=lang_src_code,
        )

    translated_text = result["translatedText"]

    # fix escaping, e.g.
    #   I&#39;ve done it a week with no improvement
    #   ->
    #   I've done it a week with no improvement
    translated_text = html.unescape(translated_text)

    if verbose > 0:
        print(f"{lang_src_code} -> {lang_tgt_code}")
        print(f"\t\"{result['input']}\" -> \"{translated_text}\"")
        if lang_src_code is None:
            print(f"\t\tDetected source language: {result['detectedSourceLanguage']}")

    return translated_text, result


def detect_language(text: str, verbose: int = 0) -> tuple[str, dict]:
    """
    Detects the text's language.
    """
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(text)
    language, confidence = result["language"], result["confidence"]
    print(f"Ran detect_language for {text} -> {language} at confidence {confidence}")
    return language, confidence
