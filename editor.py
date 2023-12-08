
import argparse
import gradio as gr
import json
import os


# Initialize the counter
record_counter = [1]

def create_conversation_pair(question_text, answer_text):
    # Split multiline text using '\n' and replace newlines with '\\n'
    question_strings = question_text.strip().replace('\r', '').split('\n')
    answer_strings = answer_text.strip().replace('\r', '').split('\n')

    # Split the strings into lines assuming each line is a separate question or answer
    question_strings = question_text.strip().split('\\n')
    answer_strings = answer_text.strip().split('\\n')

    # Ensure the lengths of question_strings and answer_strings are the same
    min_length = min(len(question_strings), len(answer_strings))

    # Create conversation pairs
    conversations = []

    for i in range(min_length):
        # Create conversation pair
        conversation_pair = [
            {"from": "human", "value": question_strings[i]},
            {"from": "gpt", "value": answer_strings[i]}
        ]
        conversations.append(conversation_pair)
    return conversations

def on_save_button_click(question_text,answer_text,filename_text,id_text):
                # Check if "datasets" folder exists, and create it if not
    datasets_folder = "./datasets_out"
    if not os.path.exists(datasets_folder):
        os.makedirs(datasets_folder)

    conversations = create_conversation_pair(question_text, answer_text)
    filename_text+=".json"
                # Create JSON structure
    json_structure = [{"id": int(id_text), "conversations": conversation} for i, conversation in enumerate(conversations, 1)]

                # Export to JSON file
    with open(os.path.join(datasets_folder, filename_text), 'w', encoding='utf-8') as json_file:
        json.dump(json_structure, json_file, indent=2)

                # Increment the counter
        record_counter[0] += 1

                # Return the updated counter value and filename
        return record_counter[0], output_filename.value+str(record_counter[0]), json.dumps(json_structure, indent=2)


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

            save_json_shareGPT.click(on_save_button_click,[question_text_field,answer_text_field,output_filename,conversation_id_record],[conversation_id_record, output_filename,output_text_field])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--share", action="store_true", help="Share the Gradio app")
    args = parser.parse_args()

    User_Interface_GUI.launch(share=args.share)
