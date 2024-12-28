# functions.py
from Year2024.Day1.auto import calculate_distance_from_url
from Year2024.Day2.auto import calculate_safe_reports
from Year2024.Day3.auto import calculate_multiplication_sum
from Year2024.Day4.auto import count_xmas_and_x_mas
from Year2024.Day5.auto import process_updates
from Year2024.Day6.auto import simulate_guard_patrol
from Year2024.Day7.auto import calculate_calibration_totals
from Year2024.Day8.auto import process_grid
from Year2024.Day9.auto import solve_day_09
from Year2024.Day10.auto import day_10
from Year2024.Day11.auto import Day_11
# ... importy dla pozostałych plików

# Słownik mapujący dzień na funkcję
DAY_FUNCTIONS = {
    1: calculate_distance_from_url,
    2: calculate_safe_reports,
    3: calculate_multiplication_sum,
    4: count_xmas_and_x_mas,
    5: process_updates,
    6: simulate_guard_patrol,
    7: calculate_calibration_totals,
    8: process_grid,
    9: solve_day_09,
    10: day_10,
    11: Day_11,

    # ... dodawając mapy dla każdego kolejnego działu
}
