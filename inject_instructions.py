import sys
import json

def modify_json(json_file, text_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)

    with open(text_file, 'r', encoding='utf-8') as file:
        prefix = file.read().strip()

    for item in data:
        for conversation in item['conversations']:
            if conversation['from'] == 'human':
                conversation['value'] = f"{prefix}\n{conversation['value']}"

    output_file = "modified_data.json"
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"Modified data saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python app.py <json_file> <text_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    text_file = sys.argv[2]
    modify_json(json_file, text_file)
