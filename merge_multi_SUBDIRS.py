import json
import os

def extract_id(data):
    return data.get("id", float('inf'))

def merge_json_files(subdir_path, output_file):
    merged_data = {"id": 1, "conversations": []}

    # Get a list of all JSON files in the current subdirectory
    json_files = [f for f in os.listdir(subdir_path) if f.endswith('.json')]

    # Read each file and collect data
    data_list = []
    for json_file in json_files:
        with open(os.path.join(subdir_path, json_file), 'r') as f:
            data = json.load(f)
            data_list.append((extract_id(data[0]), data[0]["conversations"]))

    # Sort files based on their id in ascending order
    data_list.sort(key=lambda x: x[0])

    # Append each conversation from the sorted data to the merged data
    for _, conversations in data_list:
        merged_data["conversations"].extend(conversations)

    # Write the merged data to the output file for the current subdirectory
    with open(output_file, 'w') as out_file:
        json.dump([merged_data], out_file, indent=2)

if __name__ == "__main__":
    input_directory = "."  # Change this to your input directory
    output_directory = "output"  # Change this to your desired output directory

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Get a list of all subdirectories in the input directory
    subdirs = [d for d in os.listdir(input_directory) if os.path.isdir(os.path.join(input_directory, d))]

    # Iterate over each subdirectory
    for subdir in subdirs:
        subdir_path = os.path.join(input_directory, subdir)

        # Skip the current subdirectory if there are no JSON files
        if not any(f.endswith('.json') for f in os.listdir(subdir_path)):
            continue

        # Create output file path for the current subdirectory
        sub_output_file = os.path.join(output_directory, f"{subdir}_merged_output.json")

        # Merge JSON files for the current subdirectory
        merge_json_files(subdir_path, sub_output_file)
