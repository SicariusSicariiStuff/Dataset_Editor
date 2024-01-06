import json
import sys

def create_json_structure(file1_lines, file2_lines):
    json_structure = []

    for i, (human_text, gpt_text) in enumerate(zip(file1_lines, file2_lines), start=1):
        conversation = [
            {"from": "human", "value": human_text.strip()},
            {"from": "gpt", "value": gpt_text.strip()}
        ]

        pair = {"id": i, "conversations": conversation}
        json_structure.append(pair)

    return json_structure

def main():
    if len(sys.argv) != 3:
        print("Usage: app.py <file1> <file2>")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]

    try:
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

            if len(file1_lines) != len(file2_lines):
                print("Error: Input files must have the same number of lines.")
                sys.exit(1)

            json_structure = create_json_structure(file1_lines, file2_lines)

            with open("exported_pairs.json", 'w', encoding='utf-8') as output_file:
                json.dump(json_structure, output_file, indent=2, ensure_ascii=False)

            print("Exported to exported_pairs.json")

    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
