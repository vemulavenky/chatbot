import json
from fastapi import HTTPException
import gradio as gr
from .llm_model import create_prompt, fetch_response, parse_questions_and_answers, format_questions

def get_questions_and_answers_from_paragraph(paragraph, num_questions):
    try:
        prompt = create_prompt(paragraph, num_questions)
        response_text = fetch_response(prompt)
        questions_and_answers = parse_questions_and_answers(response_text)
        formatted_qa = format_questions(questions_and_answers, num_questions)
        return formatted_qa, True
    except (KeyError, IndexError, json.JSONDecodeError, HTTPException) as e:
        return f"Error processing response: {e}", False


def gradio_interface(paragraph, num_questions):
    questions_output, success = get_questions_and_answers_from_paragraph(paragraph, num_questions)
    visibility_updates = [gr.update(visible=success) for _ in range(5)]
    return [questions_output] + visibility_updates + [gr.update(visible=success)]
