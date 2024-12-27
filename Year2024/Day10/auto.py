from utils.requester import Requester
from utils.auto_send import auto_send as Auto


def calculate_results(updates_list):
    """
    Funkcja oblicza dwa wyniki:
      - first_answer: Metoda iteracyjna (stos) 
      - second_answer: Metoda rekurencyjna (memo)
    
    Parametry:
      updates_list: nasza siatka (mapa) w postaci listy wierszy
      rules_list: niewykorzystywane (None), do kompatybilności z szablonem
    Zwraca krotkę (first_answer, second_answer).
    """
    grid = updates_list
    n = len(grid)           # liczba wierszy
    if n == 0:
        return 0, 0         # w razie pustego wejścia
    m = len(grid[0])        # liczba kolumn (zakładamy, że każdy wiersz ma tyle samo znaków)

    # Pomocnicza funkcja sprawdzająca, czy (r, c) mieści się w granicach
    def in_bounds(r, c):
        return 0 <= r < n and 0 <= c < m

    # ---- [1] Metoda iteracyjna z użyciem stosu ----
    def get_score_iterative(r_start, c_start):
        """
        Zwraca liczbę pól o wartości '9', 
        do których można dotrzeć z pola (r_start, c_start) mającego '0',
        poruszając się wyłącznie po ścieżkach rosnących o dokładnie 1.
        """
        if grid[r_start][c_start] != '0':
            return 0

        visited = set()
        stack = [(r_start, c_start)]
        visited.add((r_start, c_start))
        found_nines = 0

        while stack:
            r, c = stack.pop()
            current_val = int(grid[r][c])

            # Jeśli dotarliśmy do 9, dodajemy 1 do wyniku i nie rozchodzimy się dalej
            if current_val == 9:
                found_nines += 1
                continue

            # Sprawdzamy czterech sąsiadów
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                rr, cc = r + dr, c + dc
                if in_bounds(rr, cc) and (rr, cc) not in visited:
                    if int(grid[rr][cc]) == current_val + 1:
                        visited.add((rr, cc))
                        stack.append((rr, cc))

        return found_nines

    # Sumujemy wyniki dla wszystkich pól '0' w siatce
    first_answer = 0
    for r in range(n):
        for c in range(m):
            if grid[r][c] == '0':
                first_answer += get_score_iterative(r, c)

    # ---- [2] Metoda rekurencyjna z memoizacją ----
    memo = {}
    def get_score_recursive(r, c):
        """
        Zwraca liczbę pól '9', do których można dotrzeć rekurencyjnie z pola (r, c),
        jeśli kolejne pola mają wartość (poprzednia + 1). 
        Stosujemy memoizację, aby uniknąć wielokrotnych obliczeń.
        """
        if (r, c) in memo:
            return memo[(r, c)]

        if grid[r][c] == '9':
            memo[(r, c)] = 1
            return 1

        current_val = int(grid[r][c])
        total = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            rr, cc = r + dr, c + dc
            if in_bounds(rr, cc):
                if int(grid[rr][cc]) == current_val + 1:
                    total += get_score_recursive(rr, cc)

        memo[(r, c)] = total
        return total

    second_answer = 0
    for r in range(n):
        for c in range(m):
            if grid[r][c] == '0':
                second_answer += get_score_recursive(r, c)

    return first_answer, second_answer

def day_10(token, auto_send):
    """
    Funkcja zgodna z Twoim szablonem:
      - pobiera dane z AdventOfCode (dzień 10),
      - parsuje je,
      - oblicza dwa wyniki,
      - zwraca je wraz ze statusem gwiazdki lub wysyła, jeśli auto_send.
    """
    url = "https://adventofcode.com/2024/day/10"
    requester = Requester(url, token)

    try:
        # 1) Pobranie i przetworzenie danych
        input_data = requester.fetch_input_data()
        updates_list = input_data.strip().split("\n")

        # 2) Obliczanie wyników
        first_answer, second_answer = calculate_results(updates_list)

        # 3) Sprawdzenie sukcesu (gwiazdki)
        star_status = requester.check_day_success()

        # 4) Zwracanie lub wysyłanie
        if auto_send:
            return Auto(requester, first_answer, second_answer, star_status)
        return [first_answer, second_answer, star_status, False]

    except Exception as e:
        return ["Error", str(e)]
