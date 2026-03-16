# pylint: disable=invalid-name,duplicate-code
"""Convert integer values from a text file to binary and hexadecimal.

The script reads a file passed through the command line, converts each valid
integer to binary and hexadecimal using manual algorithms, reports invalid
items to the console, and saves the results to ConvertionResults.txt.

Usage:
    python convertNumbers.py fileWithData.txt
"""

import sys
import time

OUTPUT_FILE = "ConvertionResults.txt"
HEX_DIGITS = "0123456789ABCDEF"


def load_integers(file_path):
    """Read integer values from a file and print invalid tokens."""
    numbers = []
    invalid_count = 0

    try:
        with open(file_path, "r", encoding="utf-8") as input_file:
            for line_number, line in enumerate(input_file, start=1):
                normalized_line = line.replace(",", " ").replace(";", " ")
                for token in normalized_line.split():
                    try:
                        numbers.append(int(token))
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


def decimal_to_binary(number):
    """Convert an integer to binary without using bin()."""
    if number == 0:
        return "0"

    negative = number < 0
    value = -number if negative else number
    digits = []

    while value > 0:
        remainder = value % 2
        digits.append(str(remainder))
        value //= 2

    digits.reverse()
    result = "".join(digits)
    if negative:
        return f"-{result}"
    return result


def decimal_to_hexadecimal(number):
    """Convert an integer to hexadecimal without using hex()."""
    if number == 0:
        return "0"

    negative = number < 0
    value = -number if negative else number
    digits = []

    while value > 0:
        remainder = value % 16
        digits.append(HEX_DIGITS[remainder])
        value //= 16

    digits.reverse()
    result = "".join(digits)
    if negative:
        return f"-{result}"
    return result


def build_results_text(numbers, invalid_count, elapsed_time):
    """Build the conversion report."""
    lines = [
        "NUMBER CONVERSION RESULTS",
        "=" * 60,
        "Decimal\tBinary\tHexadecimal",
    ]

    for number in numbers:
        binary_value = decimal_to_binary(number)
        hex_value = decimal_to_hexadecimal(number)
        lines.append(f"{number}\t{binary_value}\t{hex_value}")

    lines.append("=" * 60)
    lines.append(f"Valid integers: {len(numbers)}")
    lines.append(f"Invalid tokens ignored: {invalid_count}")
    lines.append(f"Elapsed time (seconds): {elapsed_time:.6f}")

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
    """Run the full converter workflow."""
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        return

    start_time = time.perf_counter()
    file_path = sys.argv[1]
    numbers, invalid_count = load_integers(file_path)

    if numbers is None:
        return

    if not numbers:
        print("Error: the file does not contain valid integer data.")
        return

    elapsed_time = time.perf_counter() - start_time
    results_text = build_results_text(numbers, invalid_count, elapsed_time)

    print(results_text)
    save_results(results_text)


if __name__ == "__main__":
    main()
