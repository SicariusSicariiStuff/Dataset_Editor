import os
import json
import argparse

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def create_conversation_pair(question_folder, answer_folder):
    conversations = []

    # Get a list of file numbers for questions and answers
    question_files = os.listdir(question_folder)
    answer_files = os.listdir(answer_folder)

    # Sort the file lists to ensure proper pairing
    question_files.sort()
    answer_files.sort()

    for question_file, answer_file in zip(question_files, answer_files):
        question_path = os.path.join(question_folder, question_file)
        answer_path = os.path.join(answer_folder, answer_file)

        # Create conversation pair
        conversation_pair = [
            {"from": "human", "value": read_file(question_path)},
            {"from": "gpt", "value": read_file(answer_path)}
        ]

        conversations.append(conversation_pair)

    return conversations

def main():
    # Define the folder paths
    question_folder = './Q_extracted'
    answer_folder = './A_extracted'

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Create conversation pairs and export to JSON.')
    parser.add_argument('--export', default='shareGPT_exported.json', help='Name of the JSON file to be saved.')

    args = parser.parse_args()

    # Create conversation pairs
    conversations = create_conversation_pair(question_folder, answer_folder)

    # Create JSON structure
    json_structure = [{"id": str(i), "conversations": conversation} for i, conversation in enumerate(conversations, 1)]

    # Export to specified or default JSON file
    with open(args.export, 'w', encoding='utf-8') as export:
        json.dump(json_structure, export, indent=2)

if __name__ == "__main__":
    main()
