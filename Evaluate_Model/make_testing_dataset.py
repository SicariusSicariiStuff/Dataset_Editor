import json
import sys
import os

def create_json_structure(file1_lines, Correct_Answers):
    json_structure = []

    for i, human_text in enumerate(file1_lines, start=1):
        Correct_Answer = Correct_Answers[i - 1].strip()
        conversation = [
            {"from": "human", "value": human_text.strip()},
            {"from": "gpt", "value": human_text.strip()}
        ]

        pair = {"id": i, "Correct_Answer": Correct_Answer, "conversations": conversation}
        json_structure.append(pair)

    return json_structure

def main():
    if len(sys.argv) != 2:
        print("Usage: app.py <file1>")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = os.path.join(os.path.dirname(__file__), "TESTING_ANSWERS.txt")

    try:
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            file1_lines = file1.readlines()
            Correct_Answers = file2.readlines()

            if len(file1_lines) != len(Correct_Answers):
                print("Error: Number of lines in file1 and TESTING_ANSWERS.txt are not equal.")
                sys.exit(1)

            json_structure = create_json_structure(file1_lines, Correct_Answers)

            with open("TESTING_DATASET.json", 'w', encoding='utf-8') as output_file:
                json.dump(json_structure, output_file, indent=2, ensure_ascii=False)

            print("Exported to TESTING_DATASET.json")

    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
