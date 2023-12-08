import json
import sys

def is_valid_structure(data):
    # Check if the structure matches the expected format
    if not isinstance(data, list):
        return False

    for item in data:
        if not isinstance(item, dict) or "id" not in item or "conversations" not in item:
            return False

        conv = item["conversations"]
        if not isinstance(conv, list):
            return False

        for msg in conv:
            if not isinstance(msg, dict) or "from" not in msg or "value" not in msg:
                return False

    return True

def main(input_file):
    # Read JSON file
    with open(input_file, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file: {e}")
            return

    # Check if the structure is valid
    if is_valid_structure(data):
        print("JSON structure is valid.")
    else:
        print("Error: Invalid JSON structure.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_json.py <input_file.json>")
    else:
        main(sys.argv[1])
