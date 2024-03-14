import json
import os
import sys
from tqdm import tqdm

def merge_json_files(input_file, min_length, output_file):
    merged_data = []
    current_id = 1

    # Read the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        # Use json.loads to handle Unicode escape sequences during decoding
        data = json.loads(f.read())

        # Ensure data is a list
        if isinstance(data, list):
            conversations = data
        else:
            conversations = data.get("conversations", [])

        # Assign a unique ID to each conversation entry and calculate length
        for conversation in tqdm(conversations, desc="Processing conversations"):
            length = sum(len(conv["value"]) for conv in conversation["conversations"] if conv["from"] == "gpt")
            if length >= min_length:
                conversation["id"] = current_id
                current_id += 1
                conversation["length"] = length

                # Define the structure of each conversation item
                conv_item = {
                    "id": conversation["id"],
                    "length": conversation["length"],
                    "conversations": conversation["conversations"]
                }

                # Append each conversation to the merged_data list
                merged_data.append(conv_item)

    # Write the corresponding text file
    with open(output_file[:-5] + "_corresponding.txt", 'w', encoding='utf-8') as txt_file:
        for conversation in tqdm(merged_data, desc="Writing corresponding text file"):
            txt_file.write("ID: " + str(conversation["id"]) + '\n')
            txt_file.write("Length: " + str(conversation["length"]) + '\n')

    # Read data from the corresponding text file and sort by length
    sorted_data = []
    with open(output_file[:-5] + "_corresponding.txt", 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()
        id_length_pairs = [(int(lines[i].split(": ")[1]), int(lines[i + 1].split(": ")[1])) for i in range(0, len(lines), 2)]
        sorted_data = sorted(id_length_pairs, key=lambda x: x[1])

    # Create a mapping from original IDs to new IDs starting from ID 1
    id_mapping = {}
    new_id = 1
    for original_id, _ in sorted_data:
        id_mapping[original_id] = new_id
        new_id += 1

    # Write the sorted mapping to a text file
    with open(output_file[:-5] + "_sorted_mapping.txt", 'w', encoding='utf-8') as sorted_txt_file:
        for original_id, length in tqdm(sorted_data, desc="Writing sorted mapping"):
            sorted_txt_file.write(f"ID: {id_mapping[original_id]}, Length: {length}\n")

    # Reorder conversations based on the sorted mapping
    new_merged_data = []
    for original_id, _ in tqdm(sorted_data, desc="Reordering conversations"):
        for conversation in merged_data:
            if conversation["id"] == original_id:
                new_merged_data.append({
                    "id": id_mapping[original_id],
                    "length": conversation["length"],
                    "conversations": conversation["conversations"]
                })
                break

    # Write the new merged data to the output JSON file
    with open(output_file[:-5] + "_sorted.json", 'w', encoding='utf-8') as out_file:
        json.dump(new_merged_data, out_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python app.py input_file.json min_length")
        sys.exit(1)

    input_file = sys.argv[1]
    min_length = int(sys.argv[2])
    output_file = "merged_output.json"  # Change this to your desired output file

    merge_json_files(input_file, min_length, output_file)
