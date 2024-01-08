import json
import sys

def validate_json(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        print("JSON is valid.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print("JSON is invalid.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_json.py <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    validate_json(json_file_path)

