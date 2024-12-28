from utils.requester import Requester
from utils.auto_send import auto_send as Auto

def Day_14(token, auto_send):
    """
    Rozwiązanie do Part One i Part Two dnia 14.
    
    Zwraca listę [part_one_result, part_two_result, star, False] lub wywołuje Auto().
      - part_one_result: safety factor obliczony przy t = 100
      - part_two_result: najmniejsza liczba sekund t, przy której liczba komponentów <= 200
      - star           : status gwiazdki (czy zadanie ukończone)
      - False          : informacja dla systemu (czy mamy auto-wysyłać odpowiedzi)
    """

    # Ustal URL zadania (w razie potrzeby zmień "14" na inny dzień)
    url = "https://adventofcode.com/2024/day/14"
    requester = Requester(url, token)

    try:
        # Pobieramy treść wejściową
        input_data = requester.fetch_input_data()
        # Sprawdzamy, czy dzień zaliczony (gwiazdka)
        star = requester.check_day_success()

        # Rozbijamy dane na linie
        lines = input_data.strip().split("\n")

        # Rozmiary siatki (z treści zadania: 101 szer., 103 wys.)
        X = 101
        Y = 103

        # Wczytujemy roboty w formie (px, py, vx, vy)
        robots = []
        for line in lines:
            # Zakładamy format:  p=px,py  v=vx,vy
            part_pos, part_vel = line.strip().split()
            # "p=px,py" -> po '=' mamy px,py
            px_str, py_str = part_pos.split("=")[1].split(",")
            # "v=vx,vy" -> po '=' mamy vx,vy
            vx_str, vy_str = part_vel.split("=")[1].split(",")

            # Konwertujemy na int
            px, py = int(px_str), int(py_str)
            vx, vy = int(vx_str), int(vy_str)
            robots.append((px, py, vx, vy))

        # Wyniki
        part_one_result = 0
        part_two_result = 0

        # Kierunki do BFS (góra, prawo, dół, lewo)
        DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        # Symulacja do 10**6 kroków (możesz zmniejszyć, jeśli wiesz, że nie trzeba aż tyle)
        for t in range(1, 10**6 + 1):
            # Przygotuj siatkę (kropki)
            grid = [["." for _ in range(X)] for _ in range(Y)]

            # Jeśli to t == 100, liczymy safety factor w czterech ćwiartkach
            if t == 100:
                q1 = q2 = q3 = q4 = 0
                # Środki (granice) siatki
                mx = X // 2
                my = Y // 2

            # Przesuwamy roboty i stawiamy '#' w nowej pozycji
            for i in range(len(robots)):
                px, py, vx, vy = robots[i]
                px = (px + vx) % X
                py = (py + vy) % Y
                robots[i] = (px, py, vx, vy)
                grid[py][px] = "#"

                # Jeżeli to sekunda 100, sprawdzamy ćwiartki
                if t == 100:
                    # Uwaga na roboty na liniach podziału - te pomijamy (warunek w treści)
                    if px < mx and py < my:
                        q1 += 1
                    elif px > mx and py < my:
                        q2 += 1
                    elif px < mx and py > my:
                        q3 += 1
                    elif px > mx and py > my:
                        q4 += 1

            # Jeżeli to t == 100, mamy part_one_result:
            if t == 100:
                part_one_result = q1 * q2 * q3 * q4

            # Liczymy liczbę spójnych komponentów w gridzie
            visited = set()
            components = 0

            for row in range(Y):
                for col in range(X):
                    if grid[row][col] == "#" and (col, row) not in visited:
                        components += 1
                        # Własna implementacja BFS (bez deque)
                        bfs_queue = [(col, row)]
                        idx = 0
                        while idx < len(bfs_queue):
                            cx, cy = bfs_queue[idx]
                            idx += 1
                            if (cx, cy) in visited:
                                continue
                            visited.add((cx, cy))
                            # Sprawdź czterech sąsiadów
                            for dx, dy in DIRS:
                                nx, ny = cx + dx, cy + dy
                                if 0 <= nx < X and 0 <= ny < Y:
                                    if grid[ny][nx] == "#" and (nx, ny) not in visited:
                                        bfs_queue.append((nx, ny))

            # Jeśli znaleźliśmy <= 200 komponentów, uznajemy to za "choinkę"
            if components <= 200:
                part_two_result = t
                # Możesz tutaj wypisać siatkę, jeśli chcesz ją zobaczyć.
                # W oryginalnym przykładzie to jest moment 'break'.
                break

        # Czy wysyłamy automatycznie?
        if auto_send:
            return Auto(requester, part_one_result, part_two_result, star)

        # Zwracamy wyniki w standardowej formie
        return [part_one_result, part_two_result, star, False]

    except Exception as e:
        return ["Error", e]
