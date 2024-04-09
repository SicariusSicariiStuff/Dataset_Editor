import os
import requests
import json
import yaml
from tqdm import tqdm
import difflib

# Function to calculate similarity percentage
def calculate_similarity_percentage(correct_answer, generated_answer):
    matcher = difflib.SequenceMatcher(None, correct_answer, generated_answer)
    similarity_ratio = matcher.ratio()
    similarity_percentage = similarity_ratio * 100
    return similarity_percentage

# Load generation parameters from config.yml
with open("config.yml", "r") as config_file:
    config_data = yaml.safe_load(config_file)

# Extract generation parameters
generation_params = config_data.get("generation", {})
character = config_data.get("character", {}).get("name", "")  # Extract character name

url = "http://tr:5000/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}

# Read human text from human.txt
with open("pre_instructions.txt", "r", encoding="utf-8") as pre_instructions_file:
    pre_instructions = pre_instructions_file.read()

# Create directory for exported JSONs if it doesn't exist
export_dir = "exported_JSONs"
os.makedirs(export_dir, exist_ok=True)

# Initialize a list to store IDs of entries with mismatches
error_ids = []

# Use tqdm to display a progress bar
# Read questions from TESTING_DATASET.json
with open("TESTING_DATASET.json", "r", encoding="utf-8") as questions_file:
    questions_data = json.load(questions_file)
    pbar = tqdm(total=len(questions_data), desc="Processing questions", unit="question") # Move tqdm here

    # Iterate over each question entry
    for question_entry in questions_data:
        question_id = question_entry["id"]
        Correct_Answer = question_entry.get("Correct_Answer", "")  # Read Correct_Answer from input JSON
        conversations = question_entry["conversations"]

        conversation_entries = []
        for conv in conversations:
            if conv["from"] == "human":
                human_question = conv["value"]
                concatenated_question = f"{pre_instructions} {human_question}"

            elif conv["from"] == "gpt":
                gpt_question = conv["value"]
                concatenated_question = f"{pre_instructions} {gpt_question}"

            # Prepare data for API request
            history = [{"role": "user", "content": concatenated_question}]
            data = {
                "mode": "chat",
                "character": character,
                "messages": history,
                "user_bio": "",
                **generation_params  # Include generation parameters
            }

            # Make API request
            response = requests.post(url, headers=headers, json=data, verify=False)

            # Check if 'choices' key is present in the response
            if 'choices' in response.json():
                assistant_answer = response.json()['choices'][0]['message']['content']

                # Append the conversation entry with Correct_Answer
                conversation_entries.append({
                    "from": conv["from"],
                    "value": assistant_answer,

                })

        # Append the output entry to the output_data list
        output_entry = {
            "id": question_id,
            "Correct_Answer": Correct_Answer,  # Include Correct_Answer in output entry
            "conversations": conversation_entries
        }

        # Save output_data to exported_JSONs directory with 2 spaces indentation and ensure proper encoding for Hebrew characters
        with open(os.path.join(export_dir, f"OUTPUT_DATA_{question_id}.json"), "w", encoding="utf-8") as output_file:
            json.dump([output_entry], output_file, indent=2, ensure_ascii=False)

        # Your logic for error checking on each exported JSON file
        gpt_answer = next((conv["value"] for conv in output_entry["conversations"] if conv["from"] == "gpt"), None)
        human_answer = next((conv["value"] for conv in output_entry["conversations"] if conv["from"] == "human"), None)
        if gpt_answer != human_answer or gpt_answer != output_entry["Correct_Answer"] or human_answer != output_entry["Correct_Answer"]:
            error_ids.append(question_id)  # Add ID to error list
            print(f"Mismatch detected for ID {question_id}:")
            print(f"GPT answer: {repr(gpt_answer)}")  # Use repr() here
            print(f"Human answer: {repr(human_answer)}")  # Use repr() here
            print(f"Correct answer: {repr(output_entry['Correct_Answer'])}")  # Use repr() here

            # Calculate similarity percentage between correct answer and GPT-generated answer
            similarity_percentage_gpt = calculate_similarity_percentage(output_entry['Correct_Answer'], gpt_answer)

            # Calculate similarity percentage between correct answer and human answer
            similarity_percentage_human = calculate_similarity_percentage(output_entry['Correct_Answer'], human_answer)

            # Print similarity percentage for GPT-generated answer
            print(f"Similarity percentage (GPT): {similarity_percentage_gpt:.2f}%")

            # Print similarity percentage for human answer
            print(f"Similarity percentage (Human): {similarity_percentage_human:.2f}%")

            # Append error details to Dataset_Errors.txt
            with open("Dataset_Errors.txt", "a", encoding="utf-8") as error_file:
                error_file.write(f"ID: {question_id}\n")
                error_file.write(f"GPT answer: {repr(gpt_answer)}\n")
                error_file.write(f"Human answer: {repr(human_answer)}\n")
                error_file.write(f"Correct answer: {repr(output_entry['Correct_Answer'])}\n")
                error_file.write(f"Similarity percentage (GPT): {similarity_percentage_gpt:.2f}%\n")
                error_file.write(f"Similarity percentage (Human): {similarity_percentage_human:.2f}%\n\n")

        # Update progress bar
        pbar.update(1)

# Close progress bar
pbar.close()

# Calculate summary statistics, this doesn't work, some of it if not all of it is redundant
total_ids_processed = len(questions_data)
num_errors = len(error_ids)
total_error_percentage = sum(200 - (similarity_percentage_gpt + similarity_percentage_human) for question_id in error_ids) / num_errors if num_errors > 0 else 0


# Append summary to Dataset_Errors.txt
with open("Dataset_Errors.txt", "a", encoding="utf-8") as error_file:
    error_file.write(f"Total IDs processed: {total_ids_processed}\n")
    error_file.write(f"Number of IDs with errors: {num_errors}\n")
    error_file.write(f"Percentage of IDs that contains any kind of errors: {num_errors}/{total_ids_processed} = {num_errors/total_ids_processed*100:.2f}%\n")

print("Questions and answers saved to 'exported_JSONs' directory.")
