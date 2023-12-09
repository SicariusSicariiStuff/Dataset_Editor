import json
import sys

def convert_format(input_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    converted_data = []
    for index, item in enumerate(data, start=1):
        conversation = [
            {"from": "human", "value": item["instruction"]},
            {"from": "gpt", "value": item["output"]}
        ]

        converted_item = {"id": index, "conversations": conversation}
        converted_data.append(converted_item)

    output_file = input_file.replace(".json", "_sgpt.json")
    with open(output_file, 'w') as file:
        json.dump(converted_data, file, indent=2)

    print(f"Conversion completed. Output saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file.json")
    else:
        input_file = sys.argv[1]
        convert_format(input_file)

