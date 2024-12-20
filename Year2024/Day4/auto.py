from utils.requester import Requester
from utils.auto_send import auto_send as Auto

def count_xmas_and_x_mas(token, auto_send):
    """
    Pobiera dane z URL, liczy wystąpienia XMAS (Część 1) oraz X-MAS (Część 2),
    a następnie wysyła wyniki POST-em.
    """
    def count_xmas(grid, word):
        """
        Liczy wystąpienia słowa we wszystkich ośmiu kierunkach.
        """
        rows, cols = len(grid), len(grid[0])
        word_len = len(word)
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # poziomo i pionowo
            (1, 1), (1, -1), (-1, 1), (-1, -1) # na skos
        ]

        count = 0
        for i in range(rows):
            for j in range(cols):
                for dx, dy in directions:
                    x, y = i, j
                    match = True
                    for k in range(word_len):
                        if not (0 <= x < rows and 0 <= y < cols) or grid[x][y] != word[k]:
                            match = False
                            break
                        x += dx
                        y += dy
                    if match:
                        count += 1
        return count

    def find_x_mas(grid):
        directions = [[-1, -1], [-1, 1], [1, 1], [1, -1]]  # Góra i dół
        count = 0

        for x in range(1, len(grid) - 1):
            for y in range(1, len(grid[0]) - 1):
                if grid[x][y] == 'A':  # Znaleziono A
                    pairs = sum(
                        grid[x + dx][y + dy] == 'M' and grid[x - dx][y - dy] == 'S'
                        for dx, dy in directions
                    )
                    if pairs >= 2:
                        count += 1
        return count

    # Główna logika
    url = "https://adventofcode.com/2024/day/4"
    requester = Requester(url, token)

    try:
        # Pobranie danych
        input_data = requester.fetch_input_data()
        grid = [list(line.strip()) for line in input_data.strip().split("\n")]

        # Część 1: Liczenie XMAS
        xmas_count = count_xmas(grid, "XMAS")
        
        # Część 2: Liczenie X-MAS
        x_mas_count = find_x_mas(grid)

        star = requester.check_day_success()

        if auto_send:
            return Auto(requester, xmas_count, x_mas_count, star)
        return [xmas_count, x_mas_count, star, False]

    except Exception as e:
        return ["Error", e]
