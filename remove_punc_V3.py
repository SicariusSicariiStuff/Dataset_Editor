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

def process_file(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
            cleaned_text = remove_punctuation(text)
    except Exception as e:
        print("Error:", e)
        return

    try:
        # Save cleaned text to a temporary file
        with open(input_file + '_temp.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(cleaned_text)
    except Exception as e:
        print("Error:", e)
        return

    # Remove double spaces from the temporary file
    try:
        with open(input_file + '_temp.txt', 'r', encoding='utf-8') as file:
            text = file.read()
            cleaned_text = remove_double_spaces(text)
    except Exception as e:
        print("Error:", e)
        return

    # Overwrite original file with the cleaned text
    try:
        with open(input_file, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)
    except Exception as e:
        print("Error:", e)
        return

    print("Punctuation, numbers, double spaces, and double new lines removed successfully. Cleaned text saved to", input_file)

    # Clean up temporary file
    os.remove(input_file + '_temp.txt')

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_or_directory>")
        sys.exit(1)

    input_path = sys.argv[1]
    if os.path.isfile(input_path):
        process_file(input_path)
    elif os.path.isdir(input_path):
        for file_name in os.listdir(input_path):
            file_path = os.path.join(input_path, file_name)
            if os.path.isfile(file_path):
                process_file(file_path)
    else:
        print("Error: Input is neither a file nor a directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()
