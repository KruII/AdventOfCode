from utils.requester import Requester
from utils.auto_send import auto_send as Auto

def is_report_safe(report):
    """
    Sprawdza, czy raport jest bezpieczny.
    Warunki:
    1. Wartości muszą być monotonicznie rosnące lub malejące.
    2. Różnice pomiędzy wartościami są w przedziale od 1 do 3.
    """
    increasing = True
    decreasing = True

    for i in range(1, len(report)):
        diff = report[i] - report[i - 1]
        if not (1 <= abs(diff) <= 3):
            return False  # Różnica nie mieści się w przedziale [1, 3]
        if diff > 0:
            decreasing = False
        elif diff < 0:
            increasing = False

    return increasing or decreasing  # Musi być monotonicznie rosnący lub malejący

def can_be_safe_with_removal(report):
    """
    Sprawdza, czy raport staje się bezpieczny po usunięciu jednego elementu.
    """
    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1:]
        if is_report_safe(modified_report):
            return True
    return False

def calculate_safe_reports(token, auto_send):
    """
    Pobiera dane z URL i analizuje liczbę bezpiecznych raportów.
    """
    url = "https://adventofcode.com/2024/day/2"  # Przykładowy URL
    requester = Requester(url, token)

    try:
        # Pobranie danych wejściowych
        input_data = requester.fetch_input_data()
        reports = [list(map(int, line.split())) for line in input_data.strip().split("\n")]
        
        # Analiza bezpiecznych raportów
        safe_reports_part1 = sum(1 for report in reports if is_report_safe(report))
        safe_reports_part2 = sum(1 for report in reports if is_report_safe(report) or can_be_safe_with_removal(report))
        
        # Opcjonalne wysłanie wyniku
        star = requester.check_day_success()

        if auto_send:
            return(Auto(requester, safe_reports_part1, safe_reports_part2, star))
        return [safe_reports_part1, safe_reports_part2, star, False]

    except Exception as e:
        return ["Error", str(e)]
