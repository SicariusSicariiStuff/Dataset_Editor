import os
import re
from tqdm import tqdm

def extract_text_from_subtitle(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    subtitle_text = ''
    for line in lines:
        line = line.strip()
        if not re.match(r'^\d+$', line) and not re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', line):
            subtitle_text += line + '\n'

    return subtitle_text.strip()

def process_subtitle_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    subtitle_files = [f for f in os.listdir(input_dir) if f.endswith('.srt')]

    for subtitle_file in tqdm(subtitle_files, desc="Processing files"):
        input_path = os.path.join(input_dir, subtitle_file)
        output_path = os.path.join(output_dir, os.path.splitext(subtitle_file)[0] + ".txt")
        extracted_text = extract_text_from_subtitle(input_path)

        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(extracted_text)

if __name__ == "__main__":
    input_directory = "."  # Change this to the directory containing your subtitle files
    output_directory = "./output"

    process_subtitle_files(input_directory, output_directory)
