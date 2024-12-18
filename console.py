import os
from dotenv import load_dotenv
from Year2024.functions import DAY_FUNCTIONS  # Import funkcji z jednego pliku
from utils.language_loader import load_language

# Wczytanie zmiennych z pliku .env
load_dotenv()

def gen(TOKEN):
    # Generowanie sesji na podstawie TOKEN
    print(f"Wygenerowano sesję z TOKEN: {TOKEN}")
    input_url = "https://adventofcode.com/2024/day/1/input"
    DAY_FUNCTIONS[1](input_url, TOKEN)  # Wywołanie funkcji dla dnia 1 jako przykład

def get_session_token():
    """
    Funkcja sprawdza czy istnieje ciastkowa sesja w .env.
    Jeśli nie, prosi o podanie TOKEN-a i zapisuje go do pliku .env.
    """
    token = os.getenv("SESSION_TOKEN")
    if not token:
        token = input("Podaj TOKEN dla ciastkowej sesji: ")
        # Zapis TOKEN do pliku .env
        with open(".env", "a") as env_file:
            env_file.write(f"\nSESSION_TOKEN={token}")
        print("TOKEN zapisany do .env")
    return token

def get_language():
    language = os.getenv("LANGUAGE")
    if not language:
        language = "en"
        with open(".env", "a") as env_file:
            env_file.write(f"\nLANGUAGE={language}")
    return language

def get_auto_send():
    auto_send = os.getenv("AUTO_SEND")
    if not auto_send:
        auto_send = "TRUE"
        with open(".env", "a") as env_file:
            env_file.write(f"\nAUTO_SEND={auto_send}")
    return auto_send

def decrypt(message):
    message = 

def main():
    token = get_session_token()  # Pobranie ciastkowej sesji
    language = get_language()
    auto_send = get_auto_send()
    
    try:
        lang = load_language(language)
    except FileNotFoundError as e:
        print(e)
        return
    
    while True:
        print("\n"+(lang["select_day"]))
        try:
            day = int(input("Podaj numer dnia: "))
            if day == 0:
                print("Koniec programu.")
                break
            elif 1 <= day <= 25:
                if day in DAY_FUNCTIONS:
                    result = DAY_FUNCTIONS[day](token, auto_send)  # Wywołanie funkcji dla wybranego dnia
                    print(decrypt(result))
                else:
                    print(f"Funkcja dla dnia {day} nie jest zdefiniowana.")
            else:
                print("Podaj liczbę z zakresu 1-25.")
        except ValueError:
            print("Błąd: Podaj liczbę całkowitą.")

if __name__ == "__main__":
    main()
