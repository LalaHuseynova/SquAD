from deep_translator import GoogleTranslator
import time

translator = GoogleTranslator(source="en", target="az")

# Cache-lər (təkrar tərcümənin qarşısını alır)
context_cache = {}
question_cache = {}
answer_cache = {}
title_cache = {}
sentence_cache = {}  # ❗ əlavə etdik (sən istifadə edirdin amma yox idi)


def translate_text(text, cache):
    # Boş mətn
    if not text:
        return ""

    # Cache-də varsa qaytar
    if text in cache:
        return cache[text]

    try:
        translated = translator.translate(text)

        # Əgər None qaytarsa → boş string et
        if translated is None:
            translated = ""

        cache[text] = translated

        #  Rate limit problemi olmasın deyə
        time.sleep(0.2)

        return translated

    except Exception as e:
        print(f"Translation error: {e}")

        #  None yox, boş string saxla (sonra crash olmasın)
        cache[text] = ""
        return ""