import argparse
from textblob import TextBlob

def check_spelling(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
        return
    except IOError:
        print(f"Error: Could not read the file {input_file}.")
        return

    blob = TextBlob(text)
    corrected_text = ""
    
    for word in blob.words:
        corrected_word = word.correct()
        if corrected_word != word:
            print(f"Original: {word} -> Suggested: {corrected_word}")
            choice = input("Choose (s)uggested or (o)riginal: ")
            if choice.lower() == 's':
                corrected_text += str(corrected_word) + " "
            else:
                corrected_text += str(word) + " "
        else:
            corrected_text += str(word) + " "
    
    try:
        with open(output_file, 'w') as file:
            file.write(corrected_text)
        print(f"Corrected text saved to {output_file}")
    except IOError:
        print(f"Error: Could not write to the file {output_file}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check and correct spelling in a text file.')
    parser.add_argument('-f', '--file', required=True, help='Input file containing text to check')
    parser.add_argument('-o', '--output', required=True, help='Output file to save the corrected text')

    args = parser.parse_args()
    check_spelling(args.file, args.output)
