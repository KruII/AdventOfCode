from utils.requester import Requester
from utils.auto_send import auto_send as Auto

# Globalne struktury do star2:
poczatki_plikow = []
rozmiary_plikow = []

def solve_day_09(token, auto_send):
    """
    Skompaktowane rozwiązanie Day 9 (AoC) w dwóch wariantach (Star 1 i Star 2),
    z uproszczoną/powiązaną strukturą kodu.
    Zwraca listę [star1_result, star2_result, star, True].
    """

    # ------------- FUNKCJE WSPÓLNE ---------------

    def parse_lengths(puzzle_str):
        """
        Zwraca listę liczb (int), np. z "233313312141..." -> [2,3,3,3,1,3,...]
        Można raz sparsować, by nie robić int(ch) w kółko.
        """
        return [int(ch) for ch in puzzle_str]

    def build_filesystem(lengths, star2=False):
        """
        Tworzy listę bloków z naprzemiennych wartości:
          - liczba bloków pliku (ID rosnące od 0),
          - liczba wolnych bloków (None).
        Jeśli star2=True, dodatkowo wypełnia globalne tablice (poczatki_plikow, rozmiary_plikow).
        """
        blocks = []
        is_file = True
        file_id = 0

        if star2:
            # Przygotuj globalne tablice
            n = len(lengths)
            for _ in range(n):
                poczatki_plikow.append(0)
                rozmiary_plikow.append(0)

        for length in lengths:
            if is_file:
                if star2:
                    poczatki_plikow[file_id] = len(blocks)
                    rozmiary_plikow[file_id] = length
                blocks += [file_id] * length
                file_id += 1
                is_file = False
            else:
                blocks += [None] * length
                is_file = True

        return blocks

    def checksum(bloki):
        """
        Suma (i * val) po wszystkich i, gdzie bloki[i] != None.
        """
        ans = 0
        for i, val in enumerate(bloki):
            if val is not None:
                ans += i * val
        return ans

    # ------------- STAR1: METODA "ONE BY ONE" ---------------

    def move_one_by_one(bloki):
        """
        Przenosi JEDEN blok na raz: z ostatniego zajętego na pierwsze wolne od lewej,
        powtarzając aż brak dziur. Dokładnie jak w puzzle.
        """
        # 1. Znajdź pierwszy wolny od lewej
        first_free = 0
        while first_free < len(bloki) and bloki[first_free] is not None:
            first_free += 1

        # 2. Znajdź ostatni zajęty od prawej
        i = len(bloki) - 1
        while i >= 0 and bloki[i] is None:
            i -= 1

        # 3. Przenoś blok po bloku
        while i > first_free >= 0:
            bloki[first_free] = bloki[i]
            bloki[i] = None

            i -= 1
            while i >= 0 and bloki[i] is None:
                i -= 1

            first_free += 1
            while first_free < len(bloki) and bloki[first_free] is not None:
                first_free += 1
        return bloki

    # ------------- STAR2: METODA Z PLIKAMI (OD ID MAX DO 0) ---------------

    def przenies_pliki(bloki):
        """
        Metoda przenoszenia od najwyższego ID do najniższego,
        korzysta z globalnych poczatki_plikow i rozmiary_plikow.
        """
        # Znajdź najwyższe ID pliku
        max_id = 0
        while max_id < len(rozmiary_plikow) and rozmiary_plikow[max_id] > 0:
            max_id += 1
        max_id -= 1

        for plik_id in range(max_id, -1, -1):
            rozmiar = rozmiary_plikow[plik_id]
            start = poczatki_plikow[plik_id]

            wolny_index = 0
            wolnych_ciag = 0
            while (wolny_index < start) and (wolnych_ciag < rozmiar):
                wolny_index += wolnych_ciag
                wolnych_ciag = 0
                while wolny_index < len(bloki) and bloki[wolny_index] is not None:
                    wolny_index += 1
                while (wolny_index + wolnych_ciag < len(bloki)
                       and bloki[wolny_index + wolnych_ciag] is None):
                    wolnych_ciag += 1

            if wolny_index >= start:
                continue

            # Przeniesienie
            for i in range(rozmiar):
                bloki[wolny_index + i] = plik_id
            for i in range(start, start + rozmiar):
                bloki[i] = None

            poczatki_plikow[plik_id] = wolny_index
        return bloki

    # ------------- GŁÓWNA CZĘŚĆ ---------------

    try:
        # 1) Pobierz dane
        url = "https://adventofcode.com/2024/day/9"
        requester = Requester(url, token)
        puzzle_str = requester.fetch_input_data().strip()

        # 2) Sparsuj (raz), by nie wołać int(ch) za każdym razem
        lengths = parse_lengths(puzzle_str)

        # ---- STAR1 ----
        fs_star1 = build_filesystem(lengths, star2=False)
        move_one_by_one(fs_star1)
        star1_result = checksum(fs_star1)

        # ---- STAR2 ----
        # (Czyścimy globalne tablice, by nie nadpisać starych rzeczy)
        poczatki_plikow.clear()
        rozmiary_plikow.clear()

        fs_star2 = build_filesystem(lengths, star2=True)
        przenies_pliki(fs_star2)
        star2_result = checksum(fs_star2)

        # 3) Sprawdź gwiazdkę
        star = requester.check_day_success()

        # 4) Zwracamy 4 elementy
        if auto_send:
            return Auto(requester, star1_result, star2_result, star)
        else:
            return [star1_result, star2_result, star, False]

    except Exception as e:
        # Obsługa błędu
        return ["Error", str(e)]
