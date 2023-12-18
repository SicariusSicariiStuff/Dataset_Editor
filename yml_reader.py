import sys
import yaml

def extract_greeting_and_context(yaml_file_path):
    try:
        # Load YAML content from file
        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)

        # Extract greeting and context
        greeting_yml = data.get('greeting', '')
        context_yml = data.get('context', '')

        # Concatenate greeting_yml with a newline
        output_text = greeting_yml + '\n' + context_yml

        # Write to a file named "testing.txt"
        with open('testing.txt', 'w') as file:
            file.write(output_text)

        print("Extraction and writing to 'testing.txt' completed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_greeting_and_context.py <yaml_file_path>")
        sys.exit(1)

    yaml_file_path = sys.argv[1]
    extract_greeting_and_context(yaml_file_path)
