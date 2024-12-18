import os
import subprocess
from dotenv import load_dotenv
from Year2024.functions import DAY_FUNCTIONS  # Import funkcji z jednego pliku

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

def main():
    token = get_session_token()  # Pobranie ciastkowej sesji
    
    while True:
        print("\nWybierz dzień (1-25) lub 0 aby zakończyć:")
        try:
            day = int(input("Podaj numer dnia: "))
            if day == 0:
                print("Koniec programu.")
                break
            elif 1 <= day <= 25:
                if day in DAY_FUNCTIONS:
                    input_url = f"https://adventofcode.com/2024/day/{day}/input"
                    DAY_FUNCTIONS[day](input_url, token)  # Wywołanie funkcji dla wybranego dnia
                else:
                    print(f"Funkcja dla dnia {day} nie jest zdefiniowana.")
            else:
                print("Podaj liczbę z zakresu 1-25.")
        except ValueError:
            print("Błąd: Podaj liczbę całkowitą.")

if __name__ == "__main__":
    main()
