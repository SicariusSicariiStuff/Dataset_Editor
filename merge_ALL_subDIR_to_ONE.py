import json
import os

def merge_json_files(input_dir, output_file):
    merged_data = {"id": 1, "conversations": []}

    # Traverse through all subdirectories and collect JSON files
    for root, _, files in os.walk(input_dir):
        json_files = [f for f in files if f.endswith('.json')]
        for json_file in json_files:
            with open(os.path.join(root, json_file), 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        conversations = item.get("conversations", [])
                        merged_data["conversations"].extend(conversations)
                else:
                    conversations = data.get("conversations", [])
                    merged_data["conversations"].extend(conversations)

    # Sort conversations based on their id in ascending order
    merged_data["conversations"].sort(key=lambda x: x.get("id", float('inf')))

    # Write the merged data to the output file
    with open(output_file, 'w') as out_file:
        json.dump([merged_data], out_file, indent=2)

if __name__ == "__main__":
    input_directory = "."  # Change this to your input directory
    output_file = "merged_output.json"  # Change this to your desired output file

    merge_json_files(input_directory, output_file)
