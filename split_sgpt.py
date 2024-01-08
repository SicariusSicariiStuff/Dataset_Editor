import sys
import json

def split_json(input_file, num_files):
    with open(input_file, 'r') as f:
        data = json.load(f)

    entries_per_file = len(data) // num_files

    for i in range(num_files):
        start_index = i * entries_per_file
        end_index = (i + 1) * entries_per_file if i < num_files - 1 else None

        output_data = data[start_index:end_index]

        output_file = f"{input_file.split('.')[0]}_out{i + 1}.json"

        with open(output_file, 'w') as out_file:
            json.dump(output_data, out_file, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python app.py <input_json_file> <num_files>")
        sys.exit(1)

    input_file = sys.argv[1]
    num_files = int(sys.argv[2])

    split_json(input_file, num_files)
    print(f"Split {input_file} into {num_files} files.")
