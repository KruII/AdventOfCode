from utils.requester import Requester
from utils.auto_send import auto_send as Auto

def Day_13(token, auto_send):
    """
    Rozwiązanie dla Dnia 13, zwracające dwa wyniki:
     - first_answer: koszt Part One (naiwny brute force do 100 naciśnięć).
     - second_answer: koszt Part Two (rozwiązanie układu równań z przesunięciem).
    """

    url = "https://adventofcode.com/2024/day/13"
    requester = Requester(url, token)

    try:
        input_data = requester.fetch_input_data()
        star = requester.check_day_success()

        # -------------------- PARSOWANIE --------------------
        # Wejście to bloki rozdzielone pustą linią.
        # Każdy blok ma 3 linie:
        # 1) "Button A: X+..., Y+..."
        # 2) "Button B: X+..., Y+..."
        # 3) "Prize: X=..., Y=..."
        blocks = input_data.strip().split("\n\n")

        machines = []
        for block in blocks:
            lines = block.strip().split("\n")
            # lines[0] -> "Button A: X+94, Y+34"
            # lines[1] -> "Button B: X+22, Y+67"
            # lines[2] -> "Prize: X=8400, Y=5400"

            # --- Button A ---
            a_part = lines[0].split(":")[1].strip()  # "X+94, Y+34"
            ax_str, ay_str = a_part.split(",")
            ax = int(ax_str.strip().replace("X+", ""))
            ay = int(ay_str.strip().replace("Y+", ""))

            # --- Button B ---
            b_part = lines[1].split(":")[1].strip()  # "X+22, Y+67"
            bx_str, by_str = b_part.split(",")
            bx = int(bx_str.strip().replace("X+", ""))
            by = int(by_str.strip().replace("Y+", ""))

            # --- Prize ---
            p_part = lines[2].split(":")[1].strip()  # "X=8400, Y=5400"
            px_str, py_str = p_part.split(",")
            px = int(px_str.strip().replace("X=", ""))
            py = int(py_str.strip().replace("Y=", ""))

            machines.append((ax, ay, bx, by, px, py))

        # -------------------- PART ONE (NAIWNE ROZWIĄZANIE) --------------------
        # Zakładamy do 100 naciśnięć. Sprawdzamy wszystkie pary (i,j) w [0..100].
        # Koszt = 3*i + j (A kosztuje 3, B kosztuje 1).
        # Sumujemy minimalny koszt dla każdej maszyny, o ile istnieje.

        total_cost_part1 = 0
        for (ax, ay, bx, by, px, py) in machines:
            min_cost = None
            for i in range(101):
                # Jeśli ax*i już przekracza px o duży margines, można by teoretycznie zrobić break
                # (opcjonalna optymalizacja). Zostawmy pętlę w prostym kształcie:
                for j in range(101):
                    x_pos = ax*i + bx*j
                    y_pos = ay*i + by*j
                    if x_pos == px and y_pos == py:
                        cost = 3*i + j
                        if min_cost is None or cost < min_cost:
                            min_cost = cost
            if min_cost is not None:
                total_cost_part1 += min_cost

        first_answer = total_cost_part1

        # -------------------- PART TWO (DUŻE PRZESUNIĘCIE i UKŁAD RÓWNAŃ) --------------------
        # Teraz do Prize dodajemy 10^13 i sprawdzamy, czy da się rozwiązać:
        #   ax*i + bx*j = px
        #   ay*i + by*j = py
        # przy i, j >= 0, i, j całkowite. Koszt = 3*i + j.
        # Sumujemy koszty wyłącznie dla maszyn, w których to się da.

        big_shift = 10**13
        total_cost_part2 = 0

        for (ax, ay, bx, by, px_orig, py_orig) in machines:
            px = px_orig + big_shift
            py = py_orig + big_shift

            # Wyznacznik:
            det = ax*by - bx*ay
            if det == 0:
                # Wektory A i B są liniowo zależne, brak jednoznacznego rozwiązania
                continue

            # i = (px*by - bx*py) / det   (musi być całkowity)
            numerator_i = px*by - bx*py
            if numerator_i % det != 0:
                continue
            i_candidate = numerator_i // det

            # j = (py - ay*i) / by       (musi być całkowity)
            if by == 0:
                continue
            numerator_j = py - ay*i_candidate
            if numerator_j % by != 0:
                continue
            j_candidate = numerator_j // by

            # Sprawdzamy nieujemność
            if i_candidate < 0 or j_candidate < 0:
                continue

            # Weryfikacja obliczeń (opcjonalna, ale bezpieczna)
            x_check = ax*i_candidate + bx*j_candidate
            y_check = ay*i_candidate + by*j_candidate
            if x_check == px and y_check == py:
                cost = 3*i_candidate + j_candidate
                total_cost_part2 += cost

        second_answer = total_cost_part2

        # -------------------- ZWRACANIE / AUTO-WYSYŁKA --------------------
        if auto_send:
            return Auto(requester, first_answer, second_answer, star)
        else:
            return [first_answer, second_answer, star, False]

    except Exception as e:
        return ["Error", e]
