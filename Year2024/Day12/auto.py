from utils.requester import Requester
from utils.auto_send import auto_send as Auto

def _solve_first(input_data):
    """
    Pierwsze rozwiązanie:
    - Szuka spójnych obszarów (DFS/stack).
    - Liczy obwód metodą zliczania "wolnych krawędzi" w odniesieniu do sąsiadów.
    - Wynikiem jest suma (perim * area) dla każdego obszaru.
    """
    grid = input_data.strip().split('\n')
    n = len(grid)      # Zakładamy, że mapa jest kwadratowa
    if n == 0:
        return 0
    
    # Ruchy w górę, prawo, dół, lewo
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def is_in_grid(r, c):
        return 0 <= r < n and 0 <= c < n
    
    visited = set()
    regions = []
    
    # DFS aby wyodrębnić regiony
    for row in range(n):
        for col in range(n):
            if (row, col) in visited:
                continue
            # Nowy region
            stack = [(row, col)]
            regions.append((grid[row][col], []))  # (typ_plantu, lista_kratkek)

            while stack:
                r, c = stack.pop()
                if (r, c) in visited:
                    continue
                if not is_in_grid(r, c):
                    continue
                if grid[r][c] != grid[row][col]:
                    continue
                visited.add((r, c))

                regions[-1][1].append((r, c))

                for dr, dc in directions:
                    stack.append((r + dr, c + dc))
    
    # Funkcja do liczenia, ile "wolnych boków" ma dana kratka
    def count_free_sides(r, c):
        free = 0
        for dr, dc in directions:
            rr, cc = r + dr, c + dc
            if not is_in_grid(rr, cc) or grid[rr][cc] != grid[r][c]:
                free += 1
        return free
    
    def compute_perimeter(cells):
        perimeter_sum = 0
        for (r, c) in cells:
            perimeter_sum += count_free_sides(r, c)
        return perimeter_sum
    
    total_price = 0
    for plant_type, cells in regions:
        area = len(cells)
        perimeter = compute_perimeter(cells)
        total_price += area * perimeter

    return total_price


def _solve_second(input_data):
    """
    Drugie rozwiązanie:
    - Wydziela regiony jak poprzednio (DFS).
    - Obwód liczony przez analizę 2x2 sub-krat (metoda "has_corner"/"has_double_corner").
    - Również zwraca sumę (obwód * pole) dla każdego regionu.
    """
    grid = input_data.strip().split('\n')
    n = len(grid)
    if n == 0:
        return 0

    # Ruchy: góra, prawo, dół, lewo
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    def is_in_grid(r, c):
        return 0 <= r < n and 0 <= c < n

    visited = set()
    regions = []

    # DFS aby wyodrębnić regiony
    for row in range(n):
        for col in range(n):
            if (row, col) in visited:
                continue
            stack = [(row, col)]
            regions.append((grid[row][col], []))

            while stack:
                r, c = stack.pop()
                if (r, c) in visited:
                    continue
                if not is_in_grid(r, c):
                    continue
                if grid[r][c] != grid[row][col]:
                    continue
                visited.add((r, c))
                regions[-1][1].append((r, c))
                for dr, dc in directions:
                    stack.append((r + dr, c + dc))

    def compute_perimeter(cells):
        # Zamieniamy listę komórek w zbiór dla szybszego "in"
        cell_set = set(cells)

        # Wyznaczamy minimalne i maksymalne indeksy, by nie iterować poza obszarem
        min_r = min(cell[0] for cell in cells)
        max_r = max(cell[0] for cell in cells)
        min_c = min(cell[1] for cell in cells)
        max_c = max(cell[1] for cell in cells)

        # Dodatkowo warto uwzględnić -1 i +1, bo analizujemy 2x2 "okienka"
        total_perim = 0
        
        def is_in_region(r, c):
            return (r, c) in cell_set

        for r in range(min_r - 1, max_r + 1):
            for c in range(min_c - 1, max_c + 1):
                # Sprawdzamy 2x2 "okienko": (r,c), (r,c+1), (r+1,c), (r+1,c+1)
                square = [
                    is_in_region(r, c),
                    is_in_region(r, c + 1),
                    is_in_region(r + 1, c),
                    is_in_region(r + 1, c + 1),
                ]
                # Z listy bool => listę intów
                pattern = list(map(int, square))

                # Wzorce tzw. "narożnika" (has_corner):
                has_corner = pattern in [
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                    [1, 1, 1, 0],
                    [1, 1, 0, 1],
                    [1, 0, 1, 1],
                    [0, 1, 1, 1],
                ]
                # Wzorce tzw. "podwójnego narożnika" (has_double_corner):
                has_double_corner = pattern in [
                    [1, 0, 0, 1],
                    [0, 1, 1, 0],
                ]
                total_perim += has_corner
                if has_double_corner:
                    total_perim += 2

        return total_perim

    total_price = 0
    for plant_type, cells in regions:
        area = len(cells)
        perimeter = compute_perimeter(cells)
        total_price += area * perimeter

    return total_price


def Day_12(token, auto_send):
    """
    Funkcja główna do rozwiązania zadania (Dzień 12).
    Pobiera dane z AoC za pomocą Requester, liczy odpowiedzi dwoma metodami
    i odsyła rozwiązania automatycznie (jeśli auto_send jest True).
    """
    url = "https://adventofcode.com/2024/day/12"
    requester = Requester(url, token)

    try:
        # Pobranie i przetworzenie danych (zamiast pliku ./day_12.in)
        input_data = requester.fetch_input_data()

        # Obliczamy dwie odpowiedzi:
        first_answer = _solve_first(input_data)
        second_answer = _solve_second(input_data)

        # Gwiazdka (czy mamy już "gwiazdkę" za ten dzień)
        star = requester.check_day_success()

        # Jeśli auto_send = True, to wysyłamy
        if auto_send:
            return Auto(requester, first_answer, second_answer, star)
        
        # W przeciwnym razie zwracamy wyniki i informację o braku auto-wysyłania
        return [first_answer, second_answer, star, False]
    
    except Exception as e:
        # Obsługa błędów
        return ["Error", str(e)]
