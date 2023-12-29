import json
import os
import sys
import yaml
import re

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
    input_directory = "output"  # Change this to your input directory (output directory from the previous script)
    source_yml_path = "source.yml"  # Change this to the path of your source YAML file
    output_directory = "fuzed_output"  # Change this to your desired output directory for fuzed JSON files

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Fuze JSON files in the input directory
    fuze_json_files(input_directory, source_yml_path, output_directory)
