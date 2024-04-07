import json
import os
import shutil

def create_json_structure(file1_lines, file2_lines):
    json_structure = []

    for i, (human_text, gpt_text) in enumerate(zip(file1_lines, file2_lines), start=1):
        conversation = [
            {"from": "human", "value": human_text.strip()},
            {"from": "gpt", "value": gpt_text.strip()}
        ]
        pair = {"id": i, "conversations": conversation}
        json_structure.append(pair)

    return json_structure

def create_and_modify_json():
    try:
        # Create output directory if it doesn't exist
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # ENG_2_HEB Section
        with open("eng_2_heb", 'r') as file1, open("heb_2_eng", 'r') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

        if len(file1_lines) != len(file2_lines):
            print("Error: Input files must have the same number of lines.")
            return

        json_structure = create_json_structure(file1_lines, file2_lines)

        # Export to eng_2_heb.json
        with open(os.path.join(output_dir, "eng_2_heb.json"), 'w', encoding='utf-8') as output_file:
            json.dump(json_structure, output_file, indent=2, ensure_ascii=False)

        print("Exported to eng_2_heb.json")

        # Reverse conversation
        file1_lines, file2_lines = file2_lines, file1_lines

        json_structure = create_json_structure(file1_lines, file2_lines)

        # Export to heb_2_eng.json
        with open(os.path.join(output_dir, "heb_2_eng.json"), 'w', encoding='utf-8') as output_file:
            json.dump(json_structure, output_file, indent=2, ensure_ascii=False)

        print("Exported to heb_2_eng.json")

        # Modify JSON
        modify_json()

        # Call the function from the second app
        merge_json_files("output_2", "translation_DATASET.json")

    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found.")

def modify_json():
    try:
        # ENG_2_HEB_SECTION
        eng_json_file = os.path.join("output", "eng_2_heb.json")
        eng_inst_file = os.path.join(os.path.dirname(__file__), "inst_eng_2_heb")

        with open(eng_json_file, 'r', encoding='utf-8') as file:
            eng_data = json.load(file)

        with open(eng_inst_file, 'r', encoding='utf-8') as file:
            eng_prefix = file.read().strip()

        # HEB_2_ENG_SECTION
        heb_json_file = os.path.join("output", "heb_2_eng.json")
        heb_inst_file = os.path.join(os.path.dirname(__file__), "inst_heb_2_eng")

        with open(heb_json_file, 'r', encoding='utf-8') as file:
            heb_data = json.load(file)

        with open(heb_inst_file, 'r', encoding='utf-8') as file:
            heb_prefix = file.read().strip()

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading files: {e}")
        return

    # ENG_2_HEB_SECTION
    for item in eng_data:
        for conversation in item['conversations']:
            if conversation['from'] == 'human':
                conversation['value'] = f"{eng_prefix}\n{conversation['value']}"

    eng_output_dir = "output_2"
    os.makedirs(eng_output_dir, exist_ok=True)
    eng_output_file = os.path.join(eng_output_dir, "ENG_2_HEB_Instructed.json")

    with open(eng_output_file, 'w', encoding='utf-8') as file:
        json.dump(eng_data, file, indent=2, ensure_ascii=False)

    print(f"Modified ENG data saved to {eng_output_file}")

    # HEB_2_ENG_SECTION
    for item in heb_data:
        for conversation in item['conversations']:
            if conversation['from'] == 'human':
                conversation['value'] = f"{heb_prefix}\n{conversation['value']}"

    heb_output_file = os.path.join(eng_output_dir, "HEB_2_ENG_Instructed.json")

    with open(heb_output_file, 'w', encoding='utf-8') as file:
        json.dump(heb_data, file, indent=2, ensure_ascii=False)

    print(f"Modified HEB data saved to {heb_output_file}")

def merge_json_files(input_dir, output_file):
    merged_data = []
    current_id = 1

    # Get a list of all JSON files in the input directory
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    # Read each file and collect data
    for json_file in json_files:
        with open(os.path.join(input_dir, json_file), 'r', encoding='utf-8') as f:
            # Use json.loads to handle Unicode escape sequences during decoding
            data = json.loads(f.read())

            # Ensure data is a list
            if isinstance(data, list):
                conversations = data
            else:
                conversations = data.get("conversations", [])

            # Assign a unique ID to each conversation entry and calculate length
            for conversation in conversations:
                # Initialize lengths for human and gpt texts
                human_length = 0
                gpt_length = 0

                # Calculate length for human and gpt texts separately
                for conv in conversation["conversations"]:
                    if conv["from"] == "human":
                        human_length += len(conv["value"])
                    elif conv["from"] == "gpt":
                        gpt_length += len(conv["value"])

                # Sum up lengths
                total_length = human_length + gpt_length

                # Define the structure of each conversation item
                conv_item = {
                    "id": current_id,
                    "length": total_length,
                    "conversations": conversation["conversations"]
                }

                current_id += 1

                # Append each conversation to the merged_data list
                merged_data.append(conv_item)

    # Write the merged data to the output file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        json.dump(merged_data, out_file, ensure_ascii=False, indent=2)

    # Delete temporary directories
    shutil.rmtree('output')
    shutil.rmtree('output_2')


if __name__ == "__main__":
    create_and_modify_json()
