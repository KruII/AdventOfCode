import os
from dotenv import load_dotenv, set_key
from Year2024.functions import DAY_FUNCTIONS
from utils.language_loader import load_language

# Wczytanie zmiennych z pliku .env
load_dotenv()

# Globalny obiekt konfiguracji
CONFIG = {
    "token": None,
    "language": None,
    "auto_send": None,
    "lang": None
}

# Lista zmiennych do późniejszego zapisania
MISSING_ENV_VARIABLES = {}

def get_env_variable(key, default_value, interactive=False, prompt=None):
    """
    Pobiera zmienną z .env lub tymczasowo używa domyślnej wartości.
    Jeśli interactive=True, prosi użytkownika o podanie wartości.
    """
    value = os.getenv(key)
    if not value:
        if interactive and prompt:  # W przypadku tokena pozwól użytkownikowi na interakcję
            value = input(prompt)
        else:
            value = default_value
            MISSING_ENV_VARIABLES[key] = value
    return value

def load_settings():
    """
    Ładowanie wszystkich ustawień do globalnego obiektu CONFIG.
    """
    CONFIG["language"] = get_env_variable("LANGUAGE", "en")
    CONFIG["lang"] = load_language(CONFIG["language"])

    # Interaktywne pobieranie tokena, jeśli go brak
    token = os.getenv("SESSION_TOKEN")
    if not token:  # Brak tokena - proszenie użytkownika
        token = input(CONFIG["lang"]["enter_session_token"] + " ")
        set_key(".env", "SESSION_TOKEN", token)  # Zapis tokena do pliku .env
        load_dotenv(override=True)  # Odświeżenie zmiennych środowiskowych
    CONFIG["token"] = token  # Ustawienie tokena w CONFIG
    CONFIG["auto_send"] = get_env_variable("AUTO_SEND", "TRUE").upper() == "TRUE"

    # Zapis brakujących zmiennych do pliku .env
    for key, value in MISSING_ENV_VARIABLES.items():
        print(f"{CONFIG['lang']['missing_variable']} {key}. {CONFIG['lang']['default_value_set']} {value}")
        set_key(".env", key, value)

def printer_text(message):
    """
    Wyświetla odpowiedzi i wyniki w zależności od danych wejściowych, korzystając z globalnego lang.
    """
    lang = CONFIG["lang"]
    
    if message[0] == "Error":
        print(f"{lang['error']} {message[1]}")
        return

    print(f"{lang['answer_on_first_star']} {message[0]}")
    print(f"{lang['answer_on_second_star']} {message[1]}")

    if message[3]:  # Obsługa gwiazdek
        for i in message[3]:
            if not i == 0:
                if isinstance(i, dict):
                    if i.get(1) == "Completed":
                        print(lang["already_completed"])
                    elif i.get(1) == "Good":
                        level = i.get(2)
                        print(f"{lang['level']} {level} {lang['sent_successfully']}")
                    elif i.get(1) == "Error":
                        print(f"{lang['error_in_level']} {i.get(2)}: {i.get(3)}")
                else:
                    print(lang["current_stars_count"] + f" {i}")

    print(lang["current_stars_count"] + f" {message[2]}")

def main():
    load_settings()  # Ładowanie konfiguracji globalnie
    
    while True:
        lang = CONFIG["lang"]
        print("\n" + lang["select_day"])
        
        try:
            day = int(input(lang["enter_day_number"]+" "))
            if day == 0:
                #print(lang["program_end"])
                break
            if 1 <= day <= 25:
                if day in DAY_FUNCTIONS:
                    result = DAY_FUNCTIONS[day](CONFIG["token"], CONFIG["auto_send"])
                    printer_text(result)
                else:
                    print(lang["function_not_defined"].format(day=day))
            else:
                print(lang["invalid_day_range"])
        except ValueError:
            print(lang["invalid_input"])

if __name__ == "__main__":
    main()
