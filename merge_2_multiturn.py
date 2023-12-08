import json
import os

def extract_id(data):
    return data.get("id", float('inf'))

def merge_json_files(input_dir, output_file):
    merged_data = {"id": 1, "conversations": []}

    # Get a list of all JSON files in the input directory
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    # Read each file and collect data
    data_list = []
    for json_file in json_files:
        with open(os.path.join(input_dir, json_file), 'r') as f:
            data = json.load(f)
            data_list.append((extract_id(data[0]), data[0]["conversations"]))

    # Sort files based on their id in ascending order
    data_list.sort(key=lambda x: x[0])

    # Append each conversation from the sorted data to the merged data
    for _, conversations in data_list:
        merged_data["conversations"].extend(conversations)

    # Write the merged data to the output file
    with open(output_file, 'w') as out_file:
        json.dump([merged_data], out_file, indent=2)

if __name__ == "__main__":
    input_directory = "."  # Change this to your input directory
    output_file = "merged_output.json"  # Change this to your desired output file

    merge_json_files(input_directory, output_file)
