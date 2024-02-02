import json
import sys
import os

def combine_entries(input_file, group_size):
    with open(input_file, 'r') as f:
        data = json.load(f)

    combined_entries = []
    current_entry = None

    for entry in data:
        if current_entry is None:
            current_entry = entry
        else:
            current_entry['length'] += entry['length']
            current_entry['conversations'] += entry['conversations']

        if len(current_entry['conversations']) >= group_size * 2:
            combined_entries.append(current_entry)
            current_entry = None

    if current_entry is not None:
        combined_entries.append(current_entry)

    for i, entry in enumerate(combined_entries):
        entry['id'] = str(i + 1)

    base_name, extension = os.path.splitext(input_file)
    output_file = f"{base_name}_output{extension}"

    with open(output_file, 'w') as f:
        json.dump(combined_entries, f, indent=2)

    return output_file

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python app.py input_file.json group_size")
    else:
        input_file = sys.argv[1]
        group_size = int(sys.argv[2])

        output_file = combine_entries(input_file, group_size)
        print(f"Combined entries and saved to {output_file}")
