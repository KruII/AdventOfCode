from utils.requester import Requester
from utils.auto_send import auto_send as Auto
from collections import defaultdict

def process_grid(token, auto_send):
    """
    Procesuje siatkę, obliczając liczbę węzłów (antinodes) dla dwóch podejść: pierwszego i drugiego.
    """

    def in_bounds(x, y, size):
        """Sprawdza, czy współrzędne mieszczą się w granicach siatki."""
        return 0 <= x < size and 0 <= y < size

    def get_nodes_approach_one(p1, p2, size):
        """Oblicza węzły dla pierwszej odpowiedzi."""
        x1, y1 = p1
        x2, y2 = p2

        x3, y3 = x1 - (x2 - x1), y1 - (y2 - y1)
        x4, y4 = x2 + (x2 - x1), y2 + (y2 - y1)

        nodes = []
        if in_bounds(x3, y3, size):
            nodes.append((x3, y3))
        if in_bounds(x4, y4, size):
            nodes.append((x4, y4))
        return nodes

    def get_nodes_approach_two(p1, p2, size):
        """Oblicza węzły dla drugiej odpowiedzi."""
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1

        nodes = []
        i = 0
        while True:
            nx, ny = x1 - dx * i, y1 - dy * i
            if in_bounds(nx, ny, size):
                nodes.append((nx, ny))
            else:
                break
            i += 1

        i = 0
        while True:
            nx, ny = x2 + dx * i, y2 + dy * i
            if in_bounds(nx, ny, size):
                nodes.append((nx, ny))
            else:
                break
            i += 1

        return nodes

    def calculate_results(grid, size):
        """Oblicza wyniki dla obu podejść."""
        locations = defaultdict(list)
        for row in range(size):
            for col in range(size):
                if grid[row][col] != ".":
                    locations[grid[row][col]].append((row, col))

        nodes_one = set()
        nodes_two = set()

        for key in locations:
            points = locations[key]
            for i in range(len(points)):
                for j in range(i + 1, len(points)):
                    p1, p2 = points[i], points[j]
                    nodes_one.update(get_nodes_approach_one(p1, p2, size))
                    nodes_two.update(get_nodes_approach_two(p1, p2, size))

        return len(nodes_one), len(nodes_two)

    # Główna logika
    url = "https://adventofcode.com/2024/day/8"
    requester = Requester(url, token)

    try:
        # Pobranie i przetworzenie danych
        input_data = requester.fetch_input_data()
        grid = input_data.strip().split("\n")
        size = len(grid)

        # Obliczanie wyników
        result_one, result_two = calculate_results(grid, size)

        # Sprawdzenie sukcesu i wysyłanie wyników
        star_status = requester.check_day_success()

        if auto_send:
            return Auto(requester, result_one, result_two, star_status)
        return [result_one, result_two, star_status, False]

    except Exception as e:
        return ["Error", str(e)]
