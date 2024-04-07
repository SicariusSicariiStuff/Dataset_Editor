import json
import sys

def format_text(text):
    # Replace escape characters
    text = text.replace("\\n", "\n")
    text = text.replace("\\\"", "\"")
    return text

def extract_answers(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    output_file = json_file.replace(".json", ".txt")

    with open(output_file, 'w') as f:
        for item in data:
            f.write('"id": {}\n'.format(item['id']))
            f.write("=====================\n")
            for conv in item['conversations']:
                if conv['from'] == 'human':
                    f.write("QUESTION:\n")
                    f.write(format_text(conv['value']) + '\n------------')
                elif conv['from'] == 'gpt':
                    f.write("ANSWER:------------\n")
                    f.write(format_text(conv['value']) + '\n')
            f.write("\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file.json")
        sys.exit(1)

    json_file = sys.argv[1]
    extract_answers(json_file)
    print("Extraction complete. Results saved in text file.")

