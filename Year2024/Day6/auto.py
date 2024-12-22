from utils.requester import Requester
from utils.auto_send import auto_send as Auto

def simulate_guard_patrol(token, auto_send):
    """
    Pobiera dane z URL z autoryzacją TOKEN, symuluje patrol strażnika na mapie,
    oblicza liczbę unikalnych pozycji odwiedzonych przez strażnika oraz możliwe pozycje dla przeszkód,
    które powodują zapętlenie strażnika.
    """
    def parse_map(data):
        """Parsuje mapę z danych wejściowych i zwraca mapę, pozycję początkową strażnika."""
        grid = [list(line) for line in data.strip().split("\n")]
        for row, line in enumerate(grid):
            if "^" in line:
                col = line.index("^")
                grid[row][col] = "."
                return grid, (row, col)

    def simulate(grid, start_pos):
        """Symuluje patrol strażnika i zwraca odwiedzone pozycje."""
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        direction = 0
        visited = set()
        row, col = start_pos

        while True:
            visited.add((row, col))
            next_row, next_col = row + directions[direction][0], col + directions[direction][1]

            if not (0 <= next_row < len(grid) and 0 <= next_col < len(grid[0])):
                break

            if grid[next_row][next_col] == "#":
                direction = (direction + 1) % 4
            else:
                row, col = next_row, next_col

        return visited

    def will_loop(grid, start_pos, block_row, block_col):
        """Sprawdza, czy strażnik zapętli się po dodaniu przeszkody."""
        if grid[block_row][block_col] == "#":
            return False

        grid[block_row][block_col] = "#"
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        direction = 0
        seen = set()
        row, col = start_pos

        while True:
            state = (row, col, direction)
            if state in seen:
                grid[block_row][block_col] = "."
                return True
            seen.add(state)

            next_row, next_col = row + directions[direction][0], col + directions[direction][1]

            if not (0 <= next_row < len(grid) and 0 <= next_col < len(grid[0])):
                grid[block_row][block_col] = "."
                return False

            if grid[next_row][next_col] == "#":
                direction = (direction + 1) % 4
            else:
                row, col = next_row, next_col

    # Główna logika
    url = "https://adventofcode.com/2024/day/6"
    requester = Requester(url, token)

    try:
        # Pobranie i przetworzenie danych
        input_data = requester.fetch_input_data()
        grid, start_pos = parse_map(input_data)

        # Symulacja ścieżki strażnika
        visited_positions = simulate(grid, start_pos)

        # Obliczenie możliwych pozycji dla przeszkód
        loop_count = sum(
            will_loop(grid, start_pos, row, col)
            for row, col in visited_positions
            if (row, col) != start_pos
        )

        star = requester.check_day_success()

        if auto_send:
            return Auto(requester, len(visited_positions), loop_count, star)
        return [len(visited_positions), loop_count, star, False]

    except Exception as e:
        return ["Error", e]