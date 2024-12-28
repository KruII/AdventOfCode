from utils.requester import Requester
from utils.auto_send import auto_send as Auto
from collections import defaultdict

def process_stones_once(stones):
    """Procesuje jedną iterację zmiany kamieni."""
    next_stones = []
    for stone in stones:
        if stone == 0:
            next_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            half = len(str(stone)) // 2
            left_part = int(str(stone)[:half])
            right_part = int(str(stone)[half:])
            next_stones.extend([left_part, right_part])
        else:
            next_stones.append(stone * 2024)
    return next_stones

def optimized_process_stones(stones, iterations):
    """Procesuje iteracje zmian kamieni w sposób zoptymalizowany."""
    stone_count = defaultdict(int)
    for stone in stones:
        stone_count[stone] += 1

    for _ in range(iterations):
        new_stone_count = defaultdict(int)
        for stone, count in stone_count.items():
            if stone == 0:
                new_stone_count[1] += count
            elif len(str(stone)) % 2 == 0:
                half = len(str(stone)) // 2
                left_part = int(str(stone)[:half])
                right_part = int(str(stone)[half:])
                new_stone_count[left_part] += count
                new_stone_count[right_part] += count
            else:
                new_stone_count[stone * 2024] += count
        stone_count = new_stone_count

    return sum(stone_count.values())

def Day_11(token, auto_send):
    url = "https://adventofcode.com/2024/day/11"
    requester = Requester(url, token)

    try:
        # Pobranie danych wejściowych
        input_data = requester.fetch_input_data()
        stones = list(map(int, input_data.strip().split()))

        # Odpowiedź pierwsza: po 25 iteracjach (prosty sposób)
        simple_stones = stones[:]
        for _ in range(25):
            simple_stones = process_stones_once(simple_stones)
        first_answer = len(simple_stones)

        # Odpowiedź druga: po 75 iteracjach (zoptymalizowany sposób)
        second_answer = optimized_process_stones(stones, 75)

        # Wysłanie odpowiedzi
        star = requester.check_day_success()

        if auto_send:
            return Auto(requester, first_answer, second_answer, star)
        return [first_answer, second_answer, star, False]

    except Exception as e:
        return ["Error", e]
