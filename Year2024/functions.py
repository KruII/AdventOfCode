# functions.py
from Year2024.Day1.auto import calculate_distance_from_url
from Year2024.Day2.auto import calculate_safe_reports
from Year2024.Day3.auto import calculate_multiplication_sum
from Year2024.Day4.auto import count_xmas_and_x_mas
from Year2024.Day5.auto import process_updates
# ... importy dla pozostałych plików

# Słownik mapujący dzień na funkcję
DAY_FUNCTIONS = {
    1: calculate_distance_from_url,
    2: calculate_safe_reports,
    3: calculate_multiplication_sum,
    4: count_xmas_and_x_mas,
    5: process_updates
}
