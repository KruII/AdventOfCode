from utils.requester import Requester
from utils.auto_send import auto_send as Auto

def compute_expression(values, operators):
    result = values[0]
    for i in range(1, len(values)):
        if operators[i - 1] == "+":
            result += values[i]
        elif operators[i - 1] == "*":
            result *= values[i]
        elif operators[i - 1] == "|":
            result = int(f"{result}{values[i]}")
    return result

def is_target_achievable(target, values, allowed_operators):
    num_operators = len(values) - 1
    stack = [["+"] * num_operators]
    while stack:
        current_operators = stack.pop()
        if compute_expression(values, current_operators) == target:
            return True
        for idx in range(num_operators - 1, -1, -1):
            if current_operators[idx] != allowed_operators[-1]:
                current_operators[idx] = allowed_operators[allowed_operators.index(current_operators[idx]) + 1]
                stack.append(current_operators[:])
                break
            current_operators[idx] = allowed_operators[0]
    return False

def calculate_calibration_totals(token, auto_send):
    url = "https://adventofcode.com/2024/day/7"
    requester = Requester(url, token)

    try:
        input_data = requester.fetch_input_data()
        sum_basic_ops, sum_all_ops = 0, 0

        for line in input_data.strip().split("\n"):
            target, numbers = line.split(": ")
            target_value = int(target)
            values = list(map(int, numbers.split()))

            if is_target_achievable(target_value, values, ["+", "*"]):
                sum_basic_ops += target_value
            if is_target_achievable(target_value, values, ["+", "*", "|"]):
                sum_all_ops += target_value

        star_status = requester.check_day_success()

        if auto_send:
            return Auto(requester, sum_basic_ops, sum_all_ops, star_status)
        return [sum_basic_ops, sum_all_ops, star_status, False]

    except Exception as e:
        return ["Error", str(e)]
