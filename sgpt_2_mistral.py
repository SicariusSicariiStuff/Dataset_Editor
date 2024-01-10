import json
import os
import sys

def convert_typeA_to_typeB(typeA_json):
    typeB_json = []

    for item in typeA_json:
        conversations = item["conversations"]
        length = sum(len(conv["value"]) for conv in conversations if conv["from"] == "gpt")  # Count characters in "value" under "gpt"
        typeB_item = {
            "id": item["id"],
            "length": length,
            "conversations": []
        }

        first_human_added = False  # To track whether the first "value" under "human" has been processed

        for conv in conversations:
            if conv["from"] == "human":
                if not first_human_added:
                    typeB_item["conversations"].append({
                        "from": "human",
                        "value": "<s>[INST]{}[/INST]".format(conv["value"])
                    })
                    first_human_added = True
                else:
                    typeB_item["conversations"].append({
                        "from": "human",
                        "value": "[INST]{}[/INST]".format(conv["value"])
                    })
            else:
                typeB_item["conversations"].append({
                    "from": "gpt",
                    "value": "{}</s>".format(conv["value"])
                })

        typeB_json.append(typeB_item)

    return typeB_json

def save_typeB_json(typeB_json, output_filename):
    with open(output_filename, 'w') as output_file:
        json.dump(typeB_json, output_file, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py source_json")
        sys.exit(1)

    source_json_filename = sys.argv[1]
    with open(source_json_filename, 'r') as source_file:
        typeA_json = json.load(source_file)

    typeB_json = convert_typeA_to_typeB(typeA_json)

    base_name = os.path.splitext(os.path.basename(source_json_filename))[0]
    output_filename = f"{base_name}_mistraled.json"

    save_typeB_json(typeB_json, output_filename)
    print(f"Conversion complete. Result saved to {output_filename}")
