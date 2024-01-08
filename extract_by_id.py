import json
import sys
from tqdm import tqdm

def filter_and_recount(json_file, min_id, max_id):
    # Read the input JSON file
    with open(json_file, 'r', encoding='utf-8') as input_file:
        dataset = json.load(input_file)

    # Convert min_id and max_id to integers
    min_id = int(min_id)
    max_id = int(max_id)

    # Filter entries based on id
    filtered_dataset = [
        entry for entry in dataset
        if min_id <= int(entry['id']) <= max_id
    ]

    # Assign new ascending IDs
    for index, entry in enumerate(filtered_dataset, start=1):
        entry['id'] = str(index)

    # Update the "id" field during writing
    output_file_path = json_file.replace('.json', '_filtered.json')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(filtered_dataset, output_file, indent=2, ensure_ascii=False)

    print(f"Filtered and renumbered dataset saved to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py json_file min_id max_id")
    else:
        json_file = sys.argv[1]
        min_id = sys.argv[2]
        max_id = sys.argv[3]
        filter_and_recount(json_file, min_id, max_id)
