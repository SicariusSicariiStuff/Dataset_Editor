import argparse
import gradio as gr
import json
import os
import re

def decode_unicode_escape_sequences(data):
    # Define a regular expression pattern to match Unicode escape sequences
    escape_pattern = re.compile(r'\\u([0-9a-fA-F]{4})')

    def decode_line(line):
        # Replace escape sequences using a lambda function
        return escape_pattern.sub(lambda x: chr(int(x.group(1), 16)), line)

    # Replace "\\n" with actual newlines ("\n")
    data = data.replace('\\n', '\n')

    # Split the input data into lines
    lines = data.split('\n')

    # Process each line using the decode_line function
    decoded_lines = [decode_line(line) for line in lines]

    # Join the decoded lines back together
    decoded_data = '\n'.join(decoded_lines)

    return decoded_data

def process_hebrew_text(data):
    # Replace "\\n" with actual newlines ("\n")
    data = data.replace('\\n', '\n')

    # Split the input data into lines
    lines = data.split('\n')

    # Process each line using the decode_unicode_escape_sequences function
    decoded_lines = [decode_unicode_escape_sequences(line) for line in lines]

    # Join the decoded lines back together
    decoded_data = '\n'.join(decoded_lines)

    return decoded_data

def create_conversation_pair(question_text, answer_text):
    # Decode Unicode escape sequences in the input text using the updated function
    question_text_decoded = process_hebrew_text(question_text)
    answer_text_decoded = process_hebrew_text(answer_text)

    # Split multiline text using '\n' and replace newlines with '\\n'
    question_strings = question_text_decoded.strip().replace('\r', '').split('\n')
    answer_strings = answer_text_decoded.strip().replace('\r', '').split('\n')

    # Join the lines for both question and answer with '\n' separator
    concatenated_question = '\n'.join(question_strings)
    concatenated_answer = '\n'.join(answer_strings)

    # Create conversation pair
    conversation_pair = [
        {"from": "human", "value": concatenated_question},
        {"from": "gpt", "value": concatenated_answer}
    ]

    # Return the conversation pair as a single-item list
    return [conversation_pair]

# Initialize the counter
record_counter = [1]

def on_save_button_click(question_text, answer_text, filename_text, id_text):
    # Check if "datasets" folder exists, and create it if not
    datasets_folder = "./datasets_out"
    if not os.path.exists(datasets_folder):
        os.makedirs(datasets_folder)

    conversations = create_conversation_pair(question_text, answer_text)
    filename_text += ".json"
    # Create JSON structure
    json_structure = [{"id": int(id_text), "conversations": conversation} for i, conversation in enumerate(conversations, 1)]

    # Export to JSON file
    with open(os.path.join(datasets_folder, filename_text), 'w', encoding='utf-8') as json_file:
        json.dump(json_structure, json_file, indent=2, ensure_ascii=False)

    # Increment the counter
    record_counter[0] += 1

    # Return the updated counter value and filename
    return record_counter[0], output_filename.value + str(record_counter[0]), json.dumps(json_structure, indent=2, ensure_ascii=False)

# Gradio GUI
with gr.Blocks() as User_Interface_GUI:
    with gr.Row():
        with gr.Column():
            question_text_field = gr.components.Textbox(label="Question", lines=4, interactive=True)
            answer_text_field = gr.components.Textbox(label="Answer", lines=17, interactive=True)

            with gr.Row():
                conversation_id_record = gr.Number(label="Conversation ID:",
                                                   minimum=1, interactive=True, value=record_counter[0])
                output_filename = gr.components.Textbox(label=["Filename"],
                                                        value='shareGPT', interactive=True)
            with gr.Column():
                save_json_shareGPT = gr.components.Button(value="Save")

        with gr.Column():
            output_text_field = gr.components.Textbox(label="Output", lines=34)

            save_json_shareGPT.click(on_save_button_click, [question_text_field, answer_text_field, output_filename, conversation_id_record],
                                     [conversation_id_record, output_filename, output_text_field])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--share", action="store_true", help="Share the Gradio app")
    args = parser.parse_args()

    User_Interface_GUI.launch(share=args.share)
