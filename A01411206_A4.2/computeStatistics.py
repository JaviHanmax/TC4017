# pylint: disable=invalid-name,duplicate-code
"""Compute descriptive statistics from a text file.

This script reads a file passed through the command line, extracts valid
numeric values, reports invalid tokens to the console, and calculates mean,
median, mode, variance, and standard deviation using basic algorithms.

Usage:
    python computeStatistics.py fileWithData.txt
"""

import sys
import time

OUTPUT_FILE = "StatisticsResults.txt"


def merge_sort(values):
    """Return a sorted copy of *values* using merge sort."""
    if len(values) <= 1:
        return values[:]

    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])

    return merge(left, right)


def merge(left, right):
    """Merge two sorted lists into one sorted list."""
    merged = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1

    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1

    return merged


def load_numbers(file_path):
    """Read numeric values from a file and print invalid tokens."""
    numbers = []
    invalid_count = 0

    try:
        with open(file_path, "r", encoding="utf-8") as input_file:
            for line_number, line in enumerate(input_file, start=1):
                normalized_line = line.replace(",", " ").replace(";", " ")
                for token in normalized_line.split():
                    try:
                        numbers.append(float(token))
                    except ValueError:
                        invalid_count += 1
                        print(
                            f"Invalid data at line {line_number}: '{token}' "
                            "was ignored."
                        )
    except FileNotFoundError:
        print(f"Error: file '{file_path}' was not found.")
        return None, None
    except OSError as error:
        print(f"Error while reading file '{file_path}': {error}")
        return None, None

    return numbers, invalid_count


def calculate_mean(values):
    """Calculate the arithmetic mean."""
    total = 0.0
    for value in values:
        total += value
    return total / len(values)


def calculate_median(sorted_values):
    """Calculate the median from a sorted list."""
    size = len(sorted_values)
    middle = size // 2

    if size % 2 == 1:
        return sorted_values[middle]

    return (sorted_values[middle - 1] + sorted_values[middle]) / 2


def calculate_mode(values):
    """Calculate the mode or modes."""
    frequencies = {}

    for value in values:
        if value in frequencies:
            frequencies[value] += 1
        else:
            frequencies[value] = 1

    max_frequency = 0
    for frequency in frequencies.values():
        max_frequency = max(max_frequency, frequency)

    modes = []
    for value, frequency in frequencies.items():
        if frequency == max_frequency:
            modes.append(value)

    return merge_sort(modes), max_frequency


def calculate_variance(values, mean_value):
    """Calculate the population variance."""
    squared_differences_sum = 0.0

    for value in values:
        difference = value - mean_value
        squared_differences_sum += difference * difference

    return squared_differences_sum / len(values)


def format_number(value):
    """Format a numeric value with six decimal places."""
    return f"{value:.6f}"


def build_results_text(values, invalid_count, elapsed_time):
    """Build the report text shown on screen and saved to a file."""
    sorted_values = merge_sort(values)
    mean_value = calculate_mean(values)
    median_value = calculate_median(sorted_values)
    modes, mode_frequency = calculate_mode(values)
    variance_value = calculate_variance(values, mean_value)
    standard_deviation_value = variance_value ** 0.5

    if mode_frequency == 1:
        mode_text = "No mode"
    elif len(modes) == 1:
        mode_text = format_number(modes[0])
    else:
        mode_items = []
        for mode_value in modes:
            mode_items.append(format_number(mode_value))
        mode_text = ", ".join(mode_items)

    lines = [
        "DESCRIPTIVE STATISTICS",
        "=" * 50,
        f"Valid numbers: {len(values)}",
        f"Invalid tokens ignored: {invalid_count}",
        f"Mean: {format_number(mean_value)}",
        f"Median: {format_number(median_value)}",
        f"Mode: {mode_text}",
        f"Mode frequency: {mode_frequency}",
        f"Variance (population): {format_number(variance_value)}",
        (
            "Standard deviation (population): "
            f"{format_number(standard_deviation_value)}"
        ),
        f"Elapsed time (seconds): {elapsed_time:.6f}",
    ]

    return "\n".join(lines)


def save_results(results_text):
    """Save the report to the required output file."""
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
            output_file.write(results_text)
            output_file.write("\n")
    except OSError as error:
        print(f"Error while writing '{OUTPUT_FILE}': {error}")


def main():
    """Run the full statistics workflow."""
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        return

    start_time = time.perf_counter()
    file_path = sys.argv[1]
    values, invalid_count = load_numbers(file_path)

    if values is None:
        return

    if not values:
        print("Error: the file does not contain valid numeric data.")
        return

    elapsed_time = time.perf_counter() - start_time
    results_text = build_results_text(values, invalid_count, elapsed_time)

    print(results_text)
    save_results(results_text)


if __name__ == "__main__":
    main()
