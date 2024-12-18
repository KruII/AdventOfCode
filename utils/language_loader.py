import json
import os

def load_language(lang_code="en"):
    """
    Wczytuje plik językowy z folderu languages na podstawie kodu języka.
    """
    language_file = os.path.join("languages", f"{lang_code}.json")
    
    if not os.path.exists(language_file):
        raise FileNotFoundError(f"Languages file {language_file} not exist.")
    
    with open(language_file, "r", encoding="utf-8") as file:
        translations = json.load(file)
    return translations
