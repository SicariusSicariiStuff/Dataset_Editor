import os
import json
import sys

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def extract_conversation_pair(conversations, question_folder, answer_folder):
    for conversation in conversations:
        conversation_id = conversation["id"]
        pairs = conversation["conversations"]

        # Separate questions and answers
        questions = [pair["value"] for pair in pairs if pair["from"] == "human"]
        answers = [pair["value"] for pair in pairs if pair["from"] == "gpt"]

        for i, (question, answer) in enumerate(zip(questions, answers), 1):
            # Save question to Q_extracted folder
            question_file_path = os.path.join(question_folder, f'{conversation_id}_Q{i}.txt')
            write_file(question_file_path, question)

            # Save answer to A_extracted folder
            answer_file_path = os.path.join(answer_folder, f'{conversation_id}_A{i}.txt')
            write_file(answer_file_path, answer)

def main():
    # Check if a filename argument is provided
    if len(sys.argv) != 2:
        print("Usage: python app.py <json_file>")
        sys.exit(1)

    json_filename = sys.argv[1]

    # Define the folder paths
    question_extracted_folder = './Q_extracted'
    answer_extracted_folder = './A_extracted'

    # Create folders if they don't exist
    os.makedirs(question_extracted_folder, exist_ok=True)
    os.makedirs(answer_extracted_folder, exist_ok=True)

    # Load JSON from the specified file
    try:
        with open(json_filename, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError:
        print(f"Error: File '{json_filename}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{json_filename}'.")
        sys.exit(1)

    # Extract conversation pairs
    extract_conversation_pair(json_data, question_extracted_folder, answer_extracted_folder)

if __name__ == "__main__":
    main()
