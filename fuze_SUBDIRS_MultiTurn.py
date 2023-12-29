import json
import os
import sys
import yaml
import re

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

def extract_user_entries(json_data):
    user_entries = []
    for entry in json_data:
        for conv in entry['conversations']:
            if conv['from'] == 'human':
                user_entries.append(conv['value'])
                break  # Stop after finding the first human entry
    return user_entries

def merge_yaml_into_json(json_data, greeting_yml, context_yml, user_entries):
    context_yml = re.sub(r"{{char}}", "{{{{char}}}}", context_yml)
    greeting_yml = re.sub(r"{{char}}", "{{{{char}}}}", greeting_yml)
    greeting_yml = re.sub(r"{{user}}", "{{{{user}}}}", greeting_yml)

    for i, entry in enumerate(json_data):
        for j, conv in enumerate(entry['conversations']):
            if conv['from'] == 'human':
                user_entry = user_entries[i]
                json_data[i]['conversations'][j]['value'] = f"{context_yml}{{{{char}}}}: {greeting_yml}\n{{{{user}}}}: {user_entry}\n{{{{char}}}}:"
                break  # Stop after modifying the first human entry

def extract_greeting_and_context(yml_data):
    yml_data = yaml.safe_load(yml_data)

    # Extract greeting and context
    greeting_yml = yml_data.get('greeting', '')
    context_yml = yml_data.get('context', '')

    return greeting_yml, context_yml

def fuze_json_files(input_dir, source_yml_path, output_dir):
    # Read the source YAML file
    with open(source_yml_path, 'r') as yml_file:
        source_yml = yml_file.read()

    # Extract greeting and context from the source YAML
    greeting_yml, context_yml = extract_greeting_and_context(source_yml)

    # Get a list of all JSON files in the input directory
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    # Iterate over each JSON file in the input directory
    for json_file_name in json_files:
        input_json_path = os.path.join(input_dir, json_file_name)

        # Load the JSON data from the current file
        with open(input_json_path, 'r') as json_file:
            json_data = json.load(json_file)

        # Extract user entries from the JSON data
        user_entries = extract_user_entries(json_data)

        # Apply the YAML fuzer to the JSON data
        merge_yaml_into_json(json_data, greeting_yml, context_yml, user_entries)

        # Create the output file path for the fuze JSON
        output_json_path = os.path.join(output_dir, f"{os.path.splitext(json_file_name)[0]}_fuzed.json")

        # Write the fuze JSON data to the output file
        with open(output_json_path, 'w') as output_json_file:
            json.dump(json_data, output_json_file, indent=2)

if __name__ == "__main__":
    # scriptA logic
    input_directory_A = "."  # Change this to your input directory
    output_directory_A = "output"  # Change this to your desired output directory

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory_A, exist_ok=True)

    # Get a list of all subdirectories in the input directory
    subdirs_A = [d for d in os.listdir(input_directory_A) if os.path.isdir(os.path.join(input_directory_A, d))]

    # Iterate over each subdirectory
    for subdir_A in subdirs_A:
        subdir_path_A = os.path.join(input_directory_A, subdir_A)

        # Skip the current subdirectory if there are no JSON files
        if not any(f.endswith('.json') for f in os.listdir(subdir_path_A)):
            continue

        # Create output file path for the current subdirectory
        sub_output_file_A = os.path.join(output_directory_A, f"{subdir_A}_merged_output.json")

        # Merge JSON files for the current subdirectory
        merge_json_files(subdir_path_A, sub_output_file_A)

    # scriptB logic
    input_directory_B = "output"  # Change this to your input directory (output directory from the previous script)
    source_yml_path_B = "source.yml"  # Change this to the path of your source YAML file
    output_directory_B = "fuzed_output"  # Change this to your desired output directory for fuzed JSON files

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory_B, exist_ok=True)

    # Fuze JSON files in the input directory
    fuze_json_files(input_directory_B, source_yml_path_B, output_directory_B)

