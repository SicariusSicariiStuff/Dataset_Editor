import json
import sys
import yaml
import re

def extract_user_entries(json_data):
    user_entries = []
    for entry in json_data:
        for conv in entry['conversations']:
            if conv['from'] == 'human':
                user_entries.append(conv['value'])
                break  # Stop after finding the human entry
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

def main():
    if len(sys.argv) != 3:
        print("Usage: python app.py source.json source.yml")
        sys.exit(1)

    source_json_path = sys.argv[1]
    source_yml_path = sys.argv[2]

    with open(source_json_path, 'r') as json_file:
        source_json = json.load(json_file)

    with open(source_yml_path, 'r') as yml_file:
        source_yml = yml_file.read()

    # Extract greeting and context from the yml file
    greeting_yml, context_yml = extract_greeting_and_context(source_yml)

    user_entries = extract_user_entries(source_json)
    merge_yaml_into_json(source_json, greeting_yml, context_yml, user_entries)

    output_json_path = "fuzed.json"

    with open(output_json_path, 'w') as output_json_file:
        json.dump(source_json, output_json_file, indent=2)

    print(f"Output written to {output_json_path}")

def extract_greeting_and_context(yml_data):
    yml_data = yaml.safe_load(yml_data)

    # Extract greeting and context
    greeting_yml = yml_data.get('greeting', '')
    context_yml = yml_data.get('context', '')

    return greeting_yml, context_yml

if __name__ == "__main__":
    main()
