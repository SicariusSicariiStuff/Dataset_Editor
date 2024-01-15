import argparse
from transformers import GPT2Tokenizer
from tqdm import tqdm

def format_tokens(token_count):
    if token_count < 1e6:
        return str(token_count)
    else:
        return f'{token_count / 1e6:.2f}M'

def count_tokens(file_path, chunk_size=128 * 1024):
    # Load the GPT-2 tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    # Initialize token count
    total_tokens = 0

    # Open the file in binary mode to handle large files
    with open(file_path, 'rb') as file:
        # Use tqdm for progress visualization
        with tqdm(total=file.seek(0, 2), unit="B", unit_scale=True, desc=f"Counting tokens in {file_path}") as pbar:
            # Move to the beginning of the file
            file.seek(0)

            while True:
                # Read a chunk of the file
                chunk = file.read(chunk_size)

                # Check if the chunk is empty (end of file)
                if not chunk:
                    break

                # Decode the chunk to text
                text = chunk.decode('utf-8', errors='ignore')

                # Tokenize the text
                tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(text)))

                # Update the total token count
                total_tokens += len(tokens)

                # Update tqdm progress bar
                pbar.update(len(chunk))

    # Display the total number of tokens in both formats
    formatted_tokens = format_tokens(total_tokens)
    print(f'\nNumber of tokens in {file_path}: {formatted_tokens} tokens ({total_tokens} tokens)')

if __name__ == "__main__":
    # Command-line argument parser
    parser = argparse.ArgumentParser(description="Count the number of tokens in a file using GPT-2 tokenizer.")
    parser.add_argument("file", help="Path to the input file.")

    # Parse command-line arguments
    args = parser.parse_args()

    # Count tokens in the specified file
    count_tokens(args.file)
