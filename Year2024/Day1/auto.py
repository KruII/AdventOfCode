from collections import Counter
from utils.requester import Requester
import time

def calculate_distance_from_url(token, auto_send):
    """
    Pobiera dane z URL z autoryzacją TOKEN, oblicza całkowitą odległość
    i similarity score, a następnie wysyła je POST-em.
    """
    def calculate_total_distance(left_list, right_list):
        """Oblicza sumę odległości dla posortowanych list."""
        return sum(abs(left - right) for left, right in zip(left_list, right_list))

    def calculate_similarity_score(left_list, right_list):
        """Oblicza similarity score."""
        right_count = Counter(right_list)
        return sum(left * right_count[left] for left in left_list)

    def parse_input_data(data):
        """Parsuje dane wejściowe i zwraca listy."""
        left_list, right_list = [], []
        for line in data.strip().split("\n"):
            left, right = map(int, line.split())
            left_list.append(left)
            right_list.append(right)
        return left_list, right_list

    # Główna logika
    url = "https://adventofcode.com/2024/day/1"
    requester = Requester(url, token)

    try:
        # Pobranie i przetworzenie danych
        input_data = requester.fetch_input_data()
        left_list, right_list = parse_input_data(input_data)

        # Sortowanie list
        left_list.sort()
        right_list.sort()

        # Obliczenia
        total_distance = calculate_total_distance(left_list, right_list)
        similarity_score = calculate_similarity_score(left_list, right_list)
        
        star=requester.check_day_success()
        
        if auto_send:
            star_results = [0,0]
            
            if (star == 0):
                star_results[0]=requester.send_result("1", total_distance)
                star=requester.check_day_success()
                time.sleep(5)
            if (star == 1):
                star_results[1]=requester.send_result("2", similarity_score)
            if (star == 2):
                star_results[0]={1:"Completed"}
            return [total_distance, similarity_score, star, star_results]
        star = requester.check_day_success()
        return [total_distance, similarity_score, star, False]

    except Exception as e:
        return ["Error", e]
