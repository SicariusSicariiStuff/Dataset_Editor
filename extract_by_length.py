import json
import sys
from tqdm import tqdm

def filter_and_recount(json_file, min_length, max_length):
    # Read the input JSON file
    with open(json_file, 'r', encoding='utf-8') as input_file:
        dataset = json.load(input_file)

    # Filter entries based on length
    filtered_dataset = [
        entry for entry in dataset
        if min_length <= entry['length'] <= max_length
    ]

    # Assign new ascending IDs
    for index, entry in enumerate(filtered_dataset, start=1):
        entry['id'] = str(index)

    # Update the "id" field during writing
    output_file_path = json_file.replace('.json', '_trimmed.json')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(filtered_dataset, output_file, indent=2, ensure_ascii=False)

    print(f"Filtered and renumbered dataset saved to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py json_file min_length max_length")
    else:
        json_file = sys.argv[1]
        min_length = int(sys.argv[2])
        max_length = int(sys.argv[3])
        filter_and_recount(json_file, min_length, max_length)
