"""
Siau, Jacob 

DSC510-T303 Week 8 Assignment 8.1

Description: This script defines a program that does the following:
1. Reads the gettysburg.txt file and counts the number of times each word appears.
2. Writes the word count dictionary to a user-specified output file.
3. Writes the length of the word count dictionary to the output file.
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


def process_file(word_count_dict, file_name):
    """
    Write the word count dictionary to a file instead of printing it to the screen.

    Args:
        word_count_dict (dict): The dictionary to write to file.
        file_name (str): The name of the file to write to.

    Returns: None
    """
    try:
        with open(file_name, 'a') as file:  # append mode since main already wrote to it
            file.write(f"{'Word':<15} {'Count':>10}\n")
            file.write("-" * 25 + "\n")
            # Sort the word count dictionary by count in descending order and write it
            for word, count in sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True):
                file.write(f"{word:<15} {count:>10}\n")
    except Exception as e:
        print(f"An error occurred while writing to output file: {e}")


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
        output_file_name = input("Enter the filename for the output file: ")
    except Exception as e:
        print(f"An error occurred while getting output file name: {e}")
        exit()

    
    try:
        with open("./gettysburg.txt", "r") as file:
            for line in file:
                process_line(line, word_count_dict)
        
        # Write dictionary length to file (opening file first time)
        try:
            with open(output_file_name, "w") as file:
                file.write(f"Length of word count dictionary: {len(word_count_dict)}\n\n")
        except Exception as e:
            print(f"An error occurred while writing to output file: {e}")
            return
        
        # Call process_file to write the formatted word count (opening file second time)
        process_file(word_count_dict, output_file_name)
        
        print(f"Word count analysis has been written to {output_file_name}")
        
    except FileNotFoundError:
        print("Error: The file './gettysburg.txt' was not found.")
    except Exception as e:
        print(f"An error occurred while reading input file: {e}")


if __name__ == "__main__":
    main()