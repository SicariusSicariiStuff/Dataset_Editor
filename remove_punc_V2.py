import sys
import re
import os

def remove_punctuation(text):
    # Define Hebrew punctuation marks excluding dashes
    punctuation_marks = r'[\u0591-\u05BD\u05BF-\u05C7\u05F3\u05F4\u200f\u200e]+'

    # Remove punctuation marks from the text
    cleaned_text = re.sub(punctuation_marks, '', text)

    # Remove numbers
    cleaned_text = re.sub(r'\d+', '', cleaned_text)

    # Remove double new lines
    cleaned_text = re.sub(r'\n\n', '\n', cleaned_text)

    # Insert dot before each new line
    cleaned_text = re.sub(r'\n', '.\n', cleaned_text)

    # Remove spaces following a newline
    cleaned_text = re.sub(r'(?<=\n) +', '', cleaned_text)

    return cleaned_text

def remove_double_spaces(text):
    # Remove double spaces
    return re.sub(r'  +', ' ', text)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print("Error: Input file does not exist.")
        sys.exit(1)

    # Get the base name of the input file without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    output_file = f"{base_name}_cleaned.txt"
    temp_file = f"{base_name}_temp.txt"

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
            cleaned_text = remove_punctuation(text)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

    try:
        # Save cleaned text to a temporary file
        with open(temp_file, 'w', encoding='utf-8') as output_file:
            output_file.write(cleaned_text)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

    # Remove double spaces from the temporary file
    try:
        with open(temp_file, 'r', encoding='utf-8') as file:
            text = file.read()
            cleaned_text = remove_double_spaces(text)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

    # Overwrite original file with the cleaned text
    try:
        with open(input_file, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

    print("Punctuation, numbers, double spaces, and double new lines removed successfully. Cleaned text saved to", input_file)

    # Clean up temporary file
    os.remove(temp_file)

if __name__ == "__main__":
    main()
