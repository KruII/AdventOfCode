import re
from utils.requester import Requester
from utils.auto_send import auto_send as Auto

def calculate_multiplication_sum(token, auto_send):
    """
    Pobiera dane z URL z autoryzacją TOKEN, oblicza sumę wyników prawidłowych mnożeń
    w formacie mul(X,Y) oraz uwzględnia do()/don't(), a następnie wysyła wynik POST-em.
    """
    def extract_sums(data):
        """
        Wyodrębnia wyniki mnożeń dla obu części:
        - Część 1: Wszystkie instrukcje `mul(X,Y)`.
        - Część 2: Instrukcje `mul(X,Y)` aktywne wg `do()` i `don't()`.
        """
        mul_pattern = r"mul\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)"
        control_pattern = r"(do\(\)|don't\(\))"
        
        total_part1, total_part2 = 0, 0
        enabled = True  # Stan aktywności dla części 2

        # Przetwarzanie danych
        for token in re.split(control_pattern, data):
            token = token.strip()
            
            # Obsługa instrukcji sterujących
            if token == "do()":
                enabled = True
            elif token == "don't()":
                enabled = False
            else:
                # Wyszukiwanie wszystkich mul(X,Y)
                for match in re.finditer(mul_pattern, token):
                    x, y = map(int, match.groups())
                    result = x * y
                    total_part1 += result  # Zawsze dodajemy dla części 1
                    if enabled:
                        total_part2 += result  # Dodajemy tylko jeśli aktywne dla części 2
        
        return total_part1, total_part2

    # Główna logika
    url = "https://adventofcode.com/2024/day/3"
    requester = Requester(url, token)

    try:
        # Pobranie danych
        input_data = requester.fetch_input_data()

        # Wyodrębnienie wyników dla obu części
        part1_sum, part2_sum = extract_sums(input_data)
        
        star = requester.check_day_success()

        if auto_send:
            return Auto(requester, part1_sum, part2_sum, star)
        return [part1_sum, part2_sum, star, False]

    except Exception as e:
        return ["Error", e]
