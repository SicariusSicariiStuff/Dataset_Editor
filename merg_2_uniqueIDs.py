import json
import os

def merge_json_files(input_dir, output_file):
    merged_data = []
    current_id = 1

    # Get a list of all JSON files in the input directory
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    # Read each file and collect data
    for json_file in json_files:
        with open(os.path.join(input_dir, json_file), 'r') as f:
            data = json.load(f)

            # Ensure data is a list
            if isinstance(data, list):
                conversations = data
            else:
                conversations = data.get("conversations", [])

            # Assign a unique ID to each conversation entry
            for conversation in conversations:
                conversation["id"] = current_id
                current_id += 1

            # Append each conversation to the merged_data list
            merged_data.extend(conversations)

    # Write the merged data to the output file
    with open(output_file, 'w') as out_file:
        json.dump(merged_data, out_file, indent=2)

if __name__ == "__main__":
    input_directory = "."  # Change this to your input directory
    output_file = "merged_output.json"  # Change this to your desired output file

    merge_json_files(input_directory, output_file)
