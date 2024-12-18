import subprocess
import os
from dotenv import load_dotenv
from utils.language_loader import load_language

# Wczytanie zmiennych z pliku .env
load_dotenv()

def get_language():
    """
    Pobiera język z pliku .env lub prosi o wybór i zapisuje do .env
    """
    lang_code = os.getenv("LANGUAGE")  # Sprawdzenie, czy istnieje zmienna LANG

    if not lang_code:
        print("Wybierz język / Select language:")
        print("1. Polski (pl)")
        print("2. English (en)")

        # Prośba o wybór języka
        choice = input("Podaj numer (1/2): ").strip()
        lang_code = "pl" if choice == "1" else "en"

        # Zapis wyboru do pliku .env
        with open(".env", "a") as env_file:
            env_file.write(f"\nLANGUAGE={lang_code}")
        print(f"Język zapisany: {lang_code.upper()}")

    return lang_code

def main():
    # Pobierz język z funkcji
    lang_code = get_language()

    # Załaduj tłumaczenia na podstawie języka
    try:
        lang = load_language(lang_code)
    except FileNotFoundError as e:
        print(e)
        return

    # Główne menu programu
    print(lang["welcome"])
    print(lang["select_option"])
    print(lang["console_version"])
    print(lang["gui_version"])

    # Prośba o numer
    choice = input(lang["enter_number"] + " ").strip()

    if choice == "1":
        print(lang["running_console"])
        subprocess.run(["python", "console.py"], check=True)
    elif choice == "2":
        print(lang["running_gui"])
        subprocess.run(["python", "gui.py"], check=True)
    else:
        print(lang["invalid_choice"])

if __name__ == "__main__":
    main()
