import pandas as pd
from tqdm import tqdm
import sys
import os

def convert_json_to_parquet(json_file):
    # Read JSON file into a pandas DataFrame
    df = pd.read_json(json_file)

    # Extract file name without extension
    base_name = os.path.splitext(json_file)[0]

    # Define the output Parquet file name
    parquet_file = f"{base_name}.parquet"

    # Use tqdm for showing the progress bar during the conversion
    with tqdm(total=100, desc="Converting", unit="%") as pbar:
        # Convert DataFrame to Parquet format
        df.to_parquet(parquet_file, index=False, compression='snappy', engine='pyarrow')
        pbar.update(100)

    print(f"Conversion complete. Parquet file saved as: {parquet_file}")

if __name__ == "__main__":
    # Check if the input file is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python app.py <input_json_file>")
        sys.exit(1)

    input_json = sys.argv[1]

    # Check if the input file exists
    if not os.path.exists(input_json):
        print(f"Error: Input file '{input_json}' not found.")
        sys.exit(1)

    # Perform the conversion
    convert_json_to_parquet(input_json)
