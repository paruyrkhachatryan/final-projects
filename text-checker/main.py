"""Spell Checker using TextBlob.

This module provides a command-line utility to check and correct spelling in a text file.
It uses TextBlob library to identify and suggest corrections for misspelled words.
"""

import argparse
from textblob import TextBlob

def check_spelling(input_file_path, output_file_path):
    """Check and correct spelling in the given text file.

    Args:
        input_file_path (str): The path to the input file.
        output_file_path (str): The path to the output file where corrected text will be saved.
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except (FileNotFoundError, IOError) as error:
        print(f"Error: {error}")
        return

    blob = TextBlob(text)
    corrected_text = []
    
    for word in blob.words:
        corrected_word = word.correct()
        if corrected_word != word:
            print(f"Original: {word} -> Suggested: {corrected_word}")
            choice = input("Choose (s)uggested or (o)riginal: ").lower()
            corrected_text.append(corrected_word if choice == 's' else word)
        else:
            corrected_text.append(word)
    
    corrected_text_str = ' '.join(corrected_text)
    
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(corrected_text_str)
        print(f"Corrected text saved to {output_file_path}")
    except IOError as error:
        print(f"Error: {error}")

def main():
    """Main function that parses arguments and calls the spell checker."""
    parser = argparse.ArgumentParser(description='Check and correct spelling in a text file.')
    parser.add_argument('-f', '--file', required=True, help='Input file containing text to check')
    parser.add_argument('-o', '--output', required=True, help='Output file to save the corrected text')

    args = parser.parse_args()
    check_spelling(args.file, args.output)

if __name__ == "__main__":
    main()
