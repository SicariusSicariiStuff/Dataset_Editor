import os
import subprocess
import sys

def convert_xhtml_to_plain_text(input_dir):
    # Check if the provided directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' not found.")
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_dir = os.path.join(input_dir, "plain_text_output")
    os.makedirs(output_dir, exist_ok=True)

    # Loop through XHTML files and perform conversion
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".xhtml"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.txt")

            # Run ebook-convert command using subprocess
            subprocess.run(["ebook-convert", input_path, output_path, "--txt-output-formatting=plain"])

            print(f"Converted: {file_name} -> {os.path.basename(output_path)}")

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python convert_xhtml_to_plain_text.py <input_directory>")
        sys.exit(1)

    input_directory = sys.argv[1]
    convert_xhtml_to_plain_text(input_directory)
