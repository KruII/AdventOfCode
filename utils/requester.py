import requests
from bs4 import BeautifulSoup

class Requester:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.cookies.set("session", token)  # Ustawienie ciasteczka sesji na poziomie sesji

    def fetch_input_data(self):
        """Pobiera dane wejściowe z URL."""
        input_url = f"{self.base_url}/input"
        response = self.session.get(input_url)
        response.raise_for_status()
        return response.text

    def check_day_success(self):
        """
        Sprawdza, czy element z klasą 'day-success' zawiera na końcu '*' lub '**'.
        Zwraca 1, jeśli '*' i 2, jeśli '**'.
        """
        response = self.session.get(self.base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        element = soup.find(class_="day-success")  # Szukamy jednego elementu z klasą "day-success"
        
        if element and element.text.strip().endswith("**"):
            return 2
        elif element and element.text.strip().endswith("*"):
            return 1
        else:
            return 0  # Jeśli nie ma '*' lub '**'


    def send_result(self, level, answer):
        """Wysyła wynik dla danego poziomu."""
        post_url = f"{self.base_url}/answer"
        data = {"level": level, "answer": answer}
        response = self.session.post(post_url, data=data)
        if response.status_code == 200:
            return({1:"Good", 2:level})
        else:
            return({1:"Error", 2:level, 3:response.status_code })
