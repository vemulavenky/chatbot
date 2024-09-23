import os
import requests
import json
from fastapi import HTTPException
from constants import ANSWER, QUESTION
from dotenv import load_dotenv
load_dotenv()

model_url = os.getenv("MODEL_URL")
model_name =  os.getenv("MODEL_NAME")

def create_prompt(paragraph: str, num_questions: int):
    prompt = (
        "You are an AI that generates questions and answers for educational purposes. Based on the following content, create a list of insightful and relevant questions along with their corresponding answers that could be used for a quiz or discussion.\n\n"
        "Example Paragraph:\n"
        "The water cycle is a continuous process by which water circulates throughout the Earth and its atmosphere. It involves processes such as evaporation, condensation, precipitation, and collection.\n"
        "Example Questions and Answers:\n"
        "1. What are the main processes involved in the water cycle?\n"
        "Answer: The main processes involved in the water cycle are evaporation, condensation, precipitation, and collection.\n"
        "2. How does evaporation contribute to the water cycle?\n"
        "Answer: Evaporation is the process where water is converted from liquid to vapor and rises into the atmosphere, playing a crucial role in the water cycle.\n"
        "3. What happens during the condensation phase of the water cycle?\n"
        "Answer: During condensation, water vapor in the air cools down and changes back into liquid form, forming clouds.\n"
        "4. How is precipitation formed in the water cycle?\n"
        "Answer: Precipitation occurs when water in the form of rain, snow, sleet, or hail falls from clouds to the Earth's surface.\n"
        "5. Where does the water go during the collection process of the water cycle?\n"
        "Answer: During the collection process, water gathers in large bodies such as rivers, lakes, and oceans, from where it can eventually evaporate again.\n\n"
        "Content Paragraph:\n"
        f"{paragraph}\n\n"
        f"Generate the {num_questions} most important questions and answers based on the above content:"
    )
    return prompt

def fetch_response(prompt: str):
    headers = {'Content-Type': 'application/json'}
    data = {"model": model_name, "prompt": prompt, "stream": False}
    
    response = requests.post(model_url, headers=headers, data=json.dumps(data))
    response.raise_for_status()

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text) #display error in frontend code
    
    return response.json().get("response", "").strip()

def parse_questions_and_answers(response_text: str):
    lines = response_text.split("\n")
    questions_and_answers = []
    question, answer = None, None

    for line in lines:
        if line.lower().startswith(QUESTION):
            if question and answer:
                questions_and_answers.append((question, answer))
                answer = None
            question = line.strip()
        elif line.lower().startswith(ANSWER):
            answer = line.strip()
        else:
            if answer is not None:
                answer += " " + line.strip()
            elif question is not None:
                question += " " + line.strip()

    if question and answer:
        questions_and_answers.append((question, answer))

    return questions_and_answers

def format_questions(questions_and_answers: list[(str, str)], num_questions: int):
    formatted_qa = ["Here are the questions:\n"]

    for q, _ in questions_and_answers[: num_questions]:
        formatted_qa.append(f"{q}\n")

    return "\n".join(formatted_qa)
