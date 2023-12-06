import os
import json
import sys

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def create_json_structure(question_folder, answer_folder):
    pairs = []

    # Get a list of file numbers for questions and answers
    question_files = sorted(os.listdir(question_folder))
    answer_files = sorted(os.listdir(answer_folder))

    for question_file, answer_file in zip(question_files, answer_files):
        # Extract conversation ID from the file name
        conversation_id = question_file.split('_')[0]

        # Generate corresponding answer file path
        answer_file_path = os.path.join(answer_folder, answer_file)

        # Create pair dictionary
        pair = {
            "id": conversation_id,
            "conversations": [
                {"from": "human", "value": read_file(os.path.join(question_folder, question_file))},
                {"from": "gpt", "value": read_file(answer_file_path)}
            ]
        }

        pairs.append(pair)

    # Organize pairs by conversation ID
    organized_pairs = {}
    for pair in pairs:
        conversation_id = pair["id"]
        if conversation_id not in organized_pairs:
            organized_pairs[conversation_id] = {"id": conversation_id, "conversations": []}
        organized_pairs[conversation_id]["conversations"].extend(pair["conversations"])

    # Convert organized pairs to a list and sort by ID
    sorted_json_structure = sorted(list(organized_pairs.values()), key=lambda x: int(x["id"]))

    return sorted_json_structure

def main():
    # Check if a filename argument is provided
    if len(sys.argv) != 2:
        print("Usage: python app.py <json_file>")
        sys.exit(1)

    json_filename = sys.argv[1]

    # Define the folder paths
    question_extracted_folder = './Q_extracted'
    answer_extracted_folder = './A_extracted'

    # Create JSON structure
    json_structure = create_json_structure(question_extracted_folder, answer_extracted_folder)

    # Export to the specified JSON file
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(json_structure, json_file, indent=2)

if __name__ == "__main__":
    main()
