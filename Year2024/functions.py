# functions.py
from Year2024.Day1.auto import calculate_distance_from_url
from Year2024.Day2.auto import calculate_safe_reports
from Year2024.Day3.auto import calculate_multiplication_sum
# ... importy dla pozostałych plików

# Słownik mapujący dzień na funkcję
DAY_FUNCTIONS = {
    1: calculate_distance_from_url,
    2: calculate_safe_reports,
    3: calculate_multiplication_sum,
}
