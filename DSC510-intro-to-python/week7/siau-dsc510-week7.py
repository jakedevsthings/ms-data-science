"""
Siau, Jacob 

DSC510-T303 Week 7 Assignment 7.1

Description: This script defines a program that does the following:
1. Reads the gettysburg.txt file and counts the number of times each word appears.
2. Prints the word count dictionary.
3. Prints the length of the word count dictionary.
"""

import string


def pretty_print(word_count_dict):
    """
    Pretty print the word count dictionary.

    Args:
        word_count_dict (dict): The dictionary to pretty print.

    Returns: None
    """
    print(f"{'Word':<15} {'Count':>10}")
    print("-" * 25)
    # Sort the word count dictionary by count in descending order and print it
    for word, count in sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True):
        print(f"{word:<15} {count:>10}")


def add_word(word, word_count_dict):
    """
    Add a word to the word count dictionary.

    Args:
        word (str): The word to add to the word count dictionary.
        word_count_dict (dict): The dictionary to update with word counts.

    Returns: None
    """
    word_count_dict[word] = word_count_dict.get(word, 0) + 1


def process_line(line, word_count_dict):
    """
    Process a line of text, updating the word count dictionary.

    Args:
        line (str): The line of text to process.
        word_count_dict (dict): The dictionary to update with word counts.

    Returns: None
    """
    words = line.split()
    for word in words:
        word = word.lower()
        # remove all punctuation
        word = word.translate(str.maketrans('', '', string.punctuation))
        # don't add word that doesn't contain any alphanumeric characters
        # they can contain non-alphanumeric characters, but they must contain at least one alphanumeric character
        if any(char.isalnum() for char in word):
            add_word(word, word_count_dict)


def main():
    """
    Main function that runs the program.
    """
    word_count_dict = {}
    try:
        with open("./gettysburg.txt", "r") as file:
            for line in file:
                process_line(line, word_count_dict)
        print(f"Length of word count dictionary: {len(word_count_dict)}")
        pretty_print(word_count_dict)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()