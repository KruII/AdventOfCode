from utils.requester import Requester
from utils.auto_send import auto_send as Auto

def Day_16(token, auto_send):
    url = "https://adventofcode.com/2024/day/16"
    req = Requester(url, token)

    try:
        maze = req.fetch_input_data().strip().split("\n")
        star = req.check_day_success()

        # Szukamy S i E
        R = len(maze)
        S_r = S_c = 0
        for r in range(R):
            row = maze[r]
            for c in range(len(row)):
                if row[c] == "S":
                    S_r, S_c = r, c

        # Kierunki: 0=East,1=South,2=West,3=North
        D = [(0,1),(1,0),(0,-1),(-1,0)]

        # Prosty „kopiec”: lista sortowana po koszcie
        pq = []
        def pq_push(item): pq.append(item)
        def pq_pop():
            pq.sort(key=lambda x: x[0])
            return pq.pop(0) if pq else None

        # (koszt, dir, r, c, p_dir, p_r, p_c)
        pq_push((0, 0, S_r, S_c, -1, -1, -1))
        cost_map = {}
        deps = {}

        first_answer = None
        while pq:
            curr = pq_pop()
            if not curr: 
                break
            cst, d, r, c, pd, pr, pc = curr

            # Jeśli mamy już koszt dla (d, r, c)
            if (d, r, c) in cost_map:
                # Jeśli koszt ten sam – dopisujemy poprzednika
                if cost_map[(d, r, c)] == cst:
                    deps[(d, r, c)].append((pd, pr, pc))
                continue

            # Rejestracja kosztu i poprzedników
            cost_map[(d, r, c)] = cst
            deps[(d, r, c)] = [] if pd == -1 else [(pd, pr, pc)]

            # Ściana?
            if maze[r][c] == "#":
                continue

            # Koniec? – mamy minimalny koszt
            if maze[r][c] == "E":
                first_answer = cst
                end_state = (d, r, c)
                break

            # Ruch naprzód
            fr, fc = r + D[d][0], c + D[d][1]
            pq_push((cst+1, d, fr, fc, d, r, c))
            # Obrót w prawo
            pq_push((cst+1000, (d+1)%4, r, c, d, r, c))
            # Obrót w lewo
            pq_push((cst+1000, (d+3)%4, r, c, d, r, c))

        # Rekonstrukcja unikatowych pól w minimalnych ścieżkach
        stack = [end_state]
        visited_states = set()
        visited_positions = set()
        while stack:
            d, r, c = stack.pop()
            if (d, r, c) in visited_states:
                continue
            visited_states.add((d, r, c))
            visited_positions.add((r, c))

            for (pd, pr, pc) in deps.get((d, r, c), []):
                if (pd, pr, pc) in cost_map:
                    pcst = cost_map[(pd, pr, pc)]
                    ccst = cost_map[(d, r, c)]
                    # Ruch naprzód
                    if pd == d and (pr + D[d][0], pc + D[d][1]) == (r, c):
                        if pcst + 1 == ccst:
                            stack.append((pd, pr, pc))
                    # Obrót
                    elif (pr, pc) == (r, c) and ((pd+1)%4 == d or (pd+3)%4 == d):
                        if pcst + 1000 == ccst:
                            stack.append((pd, pr, pc))

        second_answer = len(visited_positions)

        if auto_send:
            return Auto(req, first_answer, second_answer, star)
        return [first_answer, second_answer, star, False]

    except Exception as e:
        return ["Error", e]
