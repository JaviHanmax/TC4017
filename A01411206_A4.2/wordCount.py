# pylint: disable=invalid-name,duplicate-code
"""Count distinct words and their frequency from a text file.

The script reads a text file passed through the command line, separates words,
normalizes them to lowercase, counts their frequency using basic algorithms,
prints the results on screen, and saves them to WordCountResults.txt.

Usage:
    python wordCount.py fileWithData.txt
"""

import sys
import time

OUTPUT_FILE = "WordCountResults.txt"
ALLOWED_EXTRA_CHARACTERS = "'-"


def clean_word(token):
    """Keep only alphanumeric characters plus selected inner characters."""
    cleaned_characters = []

    for character in token:
        if character.isalnum() or character in ALLOWED_EXTRA_CHARACTERS:
            cleaned_characters.append(character)

    cleaned = "".join(cleaned_characters).strip(ALLOWED_EXTRA_CHARACTERS)
    return cleaned.lower()


def load_words(file_path):
    """Read words from a file and report invalid tokens."""
    words = []
    invalid_count = 0

    try:
        with open(file_path, "r", encoding="utf-8") as input_file:
            for line_number, line in enumerate(input_file, start=1):
                for token in line.split():
                    cleaned = clean_word(token)
                    if cleaned:
                        words.append(cleaned)
                    else:
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

    return words, invalid_count


def sort_pairs(pairs):
    """Sort (word, frequency) pairs alphabetically by word."""
    if len(pairs) <= 1:
        return pairs[:]

    middle = len(pairs) // 2
    left = sort_pairs(pairs[:middle])
    right = sort_pairs(pairs[middle:])
    return merge_pairs(left, right)


def merge_pairs(left, right):
    """Merge two sorted lists of (word, frequency) pairs."""
    merged = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index][0] <= right[right_index][0]:
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


def count_frequencies(words):
    """Count how many times each distinct word appears."""
    frequencies = {}

    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1

    pairs = []
    for word, count in frequencies.items():
        pairs.append((word, count))

    return sort_pairs(pairs)


def build_results_text(words, invalid_count, elapsed_time):
    """Build the word count report."""
    word_counts = count_frequencies(words)

    lines = [
        "WORD COUNT RESULTS",
        "=" * 50,
        "Word\tFrequency",
    ]

    for word, count in word_counts:
        lines.append(f"{word}\t{count}")

    lines.append("=" * 50)
    lines.append(f"Total words processed: {len(words)}")
    lines.append(f"Distinct words: {len(word_counts)}")
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
    """Run the full word count workflow."""
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py fileWithData.txt")
        return

    start_time = time.perf_counter()
    file_path = sys.argv[1]
    words, invalid_count = load_words(file_path)

    if words is None:
        return

    if not words:
        print("Error: the file does not contain valid words.")
        return

    elapsed_time = time.perf_counter() - start_time
    results_text = build_results_text(words, invalid_count, elapsed_time)

    print(results_text)
    save_results(results_text)


if __name__ == "__main__":
    main()
