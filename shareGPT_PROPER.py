import json
import sys
import os

def process_json(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    output_file = input_file.replace('.json', '_ShareGPT_PROPER.json')
    with open(output_file, 'w', encoding='utf-8') as file:
        for item in data:
            output = {"id": str(item["id"]), "conversations": item["conversations"]}
            file.write(json.dumps(output, ensure_ascii=False) + '\n')

    print(f"File successfully processed and exported to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py input_file.json")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    process_json(input_file)
