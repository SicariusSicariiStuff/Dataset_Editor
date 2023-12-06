import gradio as gr



#MAIN GUI
with gr.Blocks() as User_Interface_GUI:
    with gr.Row():
        with gr.Column():
            question_text_field=gr.components.Textbox(label="Question", scale=1)
            answer_text_field=gr.components.Textbox(label="Answer", scale=2)
            with gr.Row():
                index_write_decision=gr.components.Radio(choices=["Create new index", "Add to the last index"],
                                                         label="JSON Creation", value="Create new index", interactive=True)
                conversation_id_record=gr.Number(label="Conversation ID:",
                                                 value=1, minimum=1, interactive=True)
                output_filename=gr.components.Textbox(label=["Filename"],
                                                      value='shareGPT.json', interactive=True)
            with gr.Column():
                save_json_shareGPT=gr.components.Button(value="Save")

        with gr.Column():
            output_text_field=gr.components.Textbox(label="Output")
            #
            #============Functions start here============


User_Interface_GUI.launch()
