import requests

def calculate_distance_from_url(url, token):
    """
    Pobiera dane z URL z autoryzacją TOKEN, oblicza całkowitą odległość
    """
    def calculate_total_distance(left_list, right_list):
        # Sort both lists in ascending order
        left_list.sort()
        right_list.sort()

        # Calculate the total distance
        total_distance = sum(abs(left - right) for left, right in zip(left_list, right_list))
        return total_distance

    def read_input(url, token):
        # Pobranie danych z URL z TOKEN w nagłówku Cookie
        headers = {"Cookie": f"session={token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Wyrzuca błąd dla statusu != 200
        
        left_list = []
        right_list = []
        for line in response.text.strip().split("\n"):
            left, right = map(int, line.split())
            left_list.append(left)
            right_list.append(right)
        
        return left_list, right_list

    # Główna logika
    try:
        left_list, right_list = read_input(url, token)
        result = calculate_total_distance(left_list, right_list)
        print("Total Distance:", result)
        return result
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return None
