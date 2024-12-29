from utils.requester import Requester
from utils.auto_send import auto_send as Auto

def Day_15(token, auto_send):
    """
    Rozwiązanie zadania Day 15: Warehouse Woes.
    Zwraca [first_answer, second_answer, star, False]
    albo uruchamia automatyczne wysłanie odpowiedzi.
    """

    # Główna logika – ustawienia:
    url = "https://adventofcode.com/2024/day/15"
    requester = Requester(url, token)

    try:
        # Pobranie danych wejściowych z serwera AOC
        input_data = requester.fetch_input_data()
        # Sprawdzenie, czy dzień ma już gwiazdkę (jeśli ktoś robi w trybie autopilota)
        star = requester.check_day_success()

        # Podział inputu na: mapę (grid) i sekwencję ruchów (steps)
        parts = input_data.strip().split("\n\n")
        raw_grid = parts[0].split("\n")  # lub splitlines()
        steps = parts[1].replace("\n", "")

        # --- PART 1 ---
        first_answer = solve_part1(raw_grid, steps)

        # --- PART 2 ---
        second_answer = solve_part2(raw_grid, steps)

        # Zwróć w zależności od trybu
        if auto_send:
            return Auto(requester, first_answer, second_answer, star)
        else:
            return [first_answer, second_answer, star, False]

    except Exception as e:
        return ["Error", e]


def solve_part1(raw_grid, steps):
    """
    Prosta wersja przesuwania pudełek (Part 1),
    gdzie przesuwane jest tylko najbliższe pudełko w danym kierunku,
    jeśli jest miejsce.
    """

    # Zamiana listy stringów w listę list znaków
    grid = [list(row) for row in raw_grid]
    warehouse_size = len(grid)

    # Słownik kierunków
    directions = {
        '<': (0, -1),
        '>': (0,  1),
        '^': (-1, 0),
        'v': ( 1, 0),
    }

    # Znajdź pozycję robota @
    robot_row, robot_col = None, None
    for r in range(warehouse_size):
        for c in range(warehouse_size):
            if grid[r][c] == '@':
                robot_row, robot_col = r, c
                break
        if robot_row is not None:
            break

    def is_in_bounds(row, col):
        return 0 <= row < warehouse_size and 0 <= col < warehouse_size

    def attempt_move(direction):
        nonlocal robot_row, robot_col
        drow, dcol = direction

        # Potencjalne nowe położenie robota
        new_robot_row = robot_row + drow
        new_robot_col = robot_col + dcol

        # Jeżeli wykracza poza planszę, nic nie robimy
        if not is_in_bounds(new_robot_row, new_robot_col):
            return

        # Jeżeli to ściana, nic nie robimy
        if grid[new_robot_row][new_robot_col] == '#':
            return

        # Jeżeli to puste pole, po prostu się przesuwamy
        if grid[new_robot_row][new_robot_col] == '.':
            grid[robot_row][robot_col] = '.'  # stare miejsce staje się puste
            robot_row, robot_col = new_robot_row, new_robot_col
            grid[robot_row][robot_col] = '@'  # nowe miejsce
            return

        # Jeżeli to pudełko, trzeba zobaczyć, gdzie możemy je przesunąć
        if grid[new_robot_row][new_robot_col] == 'O':
            # Sprawdzamy łańcuchowo wzdłuż kierunku, gdzie można ustawić ostatnie pudełko
            check_row, check_col = new_robot_row, new_robot_col
            while True:
                next_r = check_row + drow
                next_c = check_col + dcol

                if not is_in_bounds(next_r, next_c):
                    # Wypadamy za planszę – nie możemy przesunąć, przerywamy
                    return

                if grid[next_r][next_c] == '#':
                    # Napotkaliśmy ścianę – nie przesuwamy
                    return

                if grid[next_r][next_c] == 'O':
                    # Kolejne pudełko – przesuwamy się dalej w pętli
                    check_row, check_col = next_r, next_c
                    continue

                if grid[next_r][next_c] == '.':
                    # Mamy puste miejsce, wstawiamy tam ostatnie pudełko
                    grid[next_r][next_c] = 'O'
                    # Wszystkie poprzednie miejsca (aż do robota) przesuwają się w tę stronę
                    # Ale w tej prostej wersji – przesuwamy tylko najbliższe pudełko.
                    # Więc robimy jednorazowe przesunięcie:
                    grid[new_robot_row][new_robot_col] = '.'
                    grid[robot_row][robot_col] = '.'
                    robot_row, robot_col = new_robot_row, new_robot_col
                    grid[robot_row][robot_col] = '@'
                    return

                # Jeśli to robot albo inny znak, raczej nic nie robimy
                return

    # Przetworzenie wszystkich ruchów
    for move_char in steps:
        attempt_move(directions[move_char])

    # Po wszystkich ruchach oblicz sumę współrzędnych boxów
    total_gps = 0
    for r in range(warehouse_size):
        for c in range(warehouse_size):
            if grid[r][c] == 'O':
                total_gps += 100*r + c

    return total_gps


def solve_part2(raw_grid, steps):
    """
    Druga wersja przesuwania pudełek (Part 2) z uwzględnieniem
    łańcuchów pudełek i podwajaniem szerokości planszy (jak w oryginale).
    """

    n = len(raw_grid)
    grid = [list(row) for row in raw_grid]

    directions = {
        '<': (0, -1),
        '>': (0,  1),
        '^': (-1, 0),
        'v': ( 1, 0),
    }

    # Listy pozycji: pudełek, ścian i robota
    boxes = []
    walls = []
    robot_row, robot_col = 0, 0

    # Mapujemy wiersz n, ale kolumny na 2*n
    # (w oryginale: j*2 i j*2+1 by odzwierciedlić szerokość znaków)
    for r in range(n):
        for c in range(n):
            if grid[r][c] == '@':
                # Robot ma współrzędną w "dwukrotnej" szerokości
                robot_row, robot_col = r, c*2
            elif grid[r][c] == 'O':
                boxes.append([r, c*2])
            elif grid[r][c] == '#':
                # Ściana zajmuje dwa pola w warstwie poziomej
                walls.append([r, c*2])
                walls.append([r, c*2 + 1])

    def is_in_bounds(r, c):
        return 0 <= r < n and 0 <= c < (2*n)

    def attempt_move(direction):
        nonlocal robot_row, robot_col
        drow, dcol = direction

        # Nowa pozycja robota
        new_row = robot_row + drow
        new_col = robot_col + dcol

        # Jeśli poza planszą lub ściana, w ogóle nie ruszamy
        if not is_in_bounds(new_row, new_col):
            return
        if [new_row, new_col] in walls:
            return

        # Szukamy, które pudełka są "zblokowane" (łączą się łańcuchowo)
        to_check = []
        # Jeżeli zaraz przed robotem jest pudełko – wrzucamy do stosu
        if [new_row, new_col] in boxes:
            to_check.append([new_row, new_col])
        # Czasem trzeba też sprawdzić to samo pole -1 w kolumnie, jeśli tam jest box
        if [new_row, new_col - 1] in boxes:
            to_check.append([new_row, new_col - 1])

        can_move = True
        visited = set()

        # DFS / BFS sprawdzający, czy wszystkie powiązane pudełka mają miejsce do przesunięcia
        while to_check:
            top_r, top_c = to_check.pop()
            next_r = top_r + drow
            next_c = top_c + dcol

            # Jeśli wychodzimy poza planszę, przerwij
            if not is_in_bounds(next_r, next_c):
                can_move = False
                break

            # Jeśli to ściana, przerwij
            # Uwaga: w oryginalnym kodzie sprawdzono też [next_r, next_c+1],
            # ale to zależne od tego, jak się interpretujemy ścianę w szerokości 2.
            # Zachowajmy oryginalne założenie:
            if [next_r, next_c] in walls or [next_r, next_c + 1] in walls:
                can_move = False
                break

            # Jeśli już sprawdziliśmy, nie dopisuj
            if (top_r, top_c) in visited:
                continue
            visited.add((top_r, top_c))

            # Jeśli w nowej pozycji też są boxy, dodajemy do stosu do sprawdzenia
            if [next_r, next_c] in boxes:
                to_check.append([next_r, next_c])
            if [next_r, next_c - 1] in boxes:
                to_check.append([next_r, next_c - 1])
            if [next_r, next_c + 1] in boxes:
                to_check.append([next_r, next_c + 1])

        # Jeśli nie można, kończymy
        if not can_move:
            return

        # Jeśli można, przesuwamy wszystkie odwiedzone pudełka
        for i, box in enumerate(boxes):
            if tuple(box) in visited:
                boxes[i][0] += drow
                boxes[i][1] += dcol

        # No i przesuwamy robota
        robot_row += drow
        robot_col += dcol

    # Przetworzenie wszystkich ruchów
    for step in steps:
        attempt_move(directions[step])

    # Zliczanie współrzędnych pudełek wg GPS
    total_gps = 0
    for (r, c) in boxes:
        total_gps += 100*r + c

    return total_gps
