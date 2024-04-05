import argparse
import gradio as gr
import pyperclip

def process_text(text):
    # Replace consecutive spaces and newlines with a single space
    text = ' '.join(text.split())
    return text

# Gradio GUI
def on_text_change(input_text):
    output_text = process_text(input_text)
    pyperclip.copy(output_text)  # Copy the processed text to the clipboard
    return output_text

# Gradio GUI
with gr.Blocks() as User_Interface_GUI:
    with gr.Row():
        input_text_field = gr.components.Textbox(label="Text", lines=10, interactive=True)
        with gr.Column():
            output_text_field = gr.components.Textbox(label="Output", lines=10)

    input_text_field.change(on_text_change, inputs=[input_text_field], outputs=[output_text_field])

# Initial input text containing actual newlines
input_text = '''test1

test2'''
input_text_field.update(input_text)  # Update the input field with the initial text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--share", action="store_true", help="Share the Gradio app")
    args = parser.parse_args()
    User_Interface_GUI.launch(share=args.share)
