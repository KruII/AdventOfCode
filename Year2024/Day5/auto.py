from utils.requester import Requester
from utils.auto_send import auto_send as Auto
from collections import defaultdict

def process_updates(token, auto_send):
    """
    Pobiera dane z URL z autoryzacją TOKEN, przetwarza reguły i aktualizacje,
    a następnie oblicza wynik dla dwóch odpowiedzi: pierwszej i drugiej (optymalnej).
    """

    def parse_input_data(raw_data):
        """Parsuje dane wejściowe na reguły i aktualizacje."""
        raw_rules, raw_updates = raw_data.strip().split("\n\n")
        rules_list = []
        for rule_line in raw_rules.split("\n"):
            rule_start, rule_end = rule_line.split("|")
            rules_list.append((int(rule_start), int(rule_end)))
        updates_list = [list(map(int, update_line.split(","))) for update_line in raw_updates.split("\n")]
        return rules_list, updates_list

    def validate_update(update_sequence, rules_list):
        """Sprawdza, czy aktualizacja spełnia reguły."""
        element_indices = {element: index for index, element in enumerate(update_sequence)}
        for rule_start, rule_end in rules_list:
            if rule_start in element_indices and rule_end in element_indices and not element_indices[rule_start] < element_indices[rule_end]:
                return False, 0
        return True, update_sequence[len(update_sequence) // 2]

    def calculate_results(updates_list, rules_list):
        """Oblicza wyniki dla obu odpowiedzi: bez sortowania i z sortowaniem."""
        first_result = 0
        second_result = 0

        for update_sequence in updates_list:
            is_valid, middle_value = validate_update(update_sequence, rules_list)
            if is_valid:
                first_result += middle_value
            else:
                sorted_sequence = sort_topologically(update_sequence, rules_list)
                second_result += sorted_sequence[len(sorted_sequence) // 2]

        return first_result, second_result

    def sort_topologically(update_sequence, rules_list):
        """Sortowanie topologiczne elementów aktualizacji zgodnie z regułami."""
        applicable_rules = [(rule_start, rule_end) for rule_start, rule_end in rules_list if rule_start in update_sequence and rule_end in update_sequence]

        in_degree = defaultdict(int)
        for rule_start, rule_end in applicable_rules:
            in_degree[rule_end] += 1

        sorted_sequence = []
        while len(sorted_sequence) < len(update_sequence):
            for element in update_sequence:
                if element in sorted_sequence:
                    continue
                if in_degree[element] <= 0:
                    sorted_sequence.append(element)
                    for rule_start, rule_end in applicable_rules:
                        if rule_start == element:
                            in_degree[rule_end] -= 1
        return sorted_sequence

    # Główna logika
    url = "https://adventofcode.com/2024/day/5"
    requester = Requester(url, token)

    try:
        # Pobranie i przetworzenie danych
        input_data = requester.fetch_input_data()
        rules_list, updates_list = parse_input_data(input_data)

        # Obliczanie wyników
        first_answer, second_answer = calculate_results(updates_list, rules_list)

        # Sprawdzenie sukcesu i wysyłanie wyników
        star_status = requester.check_day_success()

        if auto_send:
            return Auto(requester, first_answer, second_answer, star_status)
        return [first_answer, second_answer, star_status, False]

    except Exception as e:
        return ["Error", str(e)]
