import gradio as gr
from .content_processing import gradio_interface


def create_gradio_ui():
    with gr.Blocks() as demo:
        paragraph = gr.Textbox(label="Enter Paragraph", placeholder="Enter your content here...")
        num_questions = gr.Number(label="Number of Questions")
        output = gr.Textbox(label="Generated Questions", placeholder="Questions will appear here...")

        with gr.Row():
            submit_btn = gr.Button("Submit")
            cancel_btn = gr.Button("Cancel")
        user_answers = [gr.Textbox(label=f"Answer {i+1}", placeholder="Enter your answer here...", visible=False) for i in range(5)]
        feedback_output = gr.Textbox(label="Feedback", placeholder="Feedback will appear here...", visible=False)

        submit_btn.click(fn=gradio_interface, inputs=[paragraph, num_questions], outputs=[output] + user_answers + [feedback_output])
        cancel_btn.click(fn=lambda: ("",) + tuple(gr.update(visible=False) for _ in range(6)), inputs=None, outputs=[output] + user_answers + [feedback_output])

    return demo