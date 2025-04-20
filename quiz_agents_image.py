from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from openai import OpenAI
import os
import re
import random

# LangChain for text-based agents
llm = ChatOpenAI(
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# OpenAI client for DALL·E 3 image generation
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Agent 1: Quiz Generator
def generate_question(previous_questions):
    previous_text = "Avoid repeating these questions:\n" + "\n".join(previous_questions) if previous_questions else ""
    prompt = PromptTemplate.from_template(
        "Generate a fun and unique multiple-choice quiz question about vehicle brands.  "
        "Avoid these questions if provided:\n{previous_text}\n"
        "Include only 4 options labeled A to D. And do not repeat the options"
        "Format:\n"
        "Question: <text>\n"
        "A) <option1>\n"
        "B) <option2>\n"
        "C) <option3>\n"
        "D) <option4>\n"
        "Correct Answer: <A/B/C/D>"
    )
    response = llm.invoke(prompt.format(previous_text=previous_text))
    raw = response.content.strip()

    try:
        question_text = re.search(r"Question:\s*(.*)", raw).group(1)
        options = re.findall(r"[A-D]\)\s*(.*)", raw)
        correct_letter = re.search(r"Correct Answer:\s*([A-D])", raw).group(1)
        correct_option = options[ord(correct_letter) - ord('A')]

        return {
            "question": question_text.strip(),
            "options": options,
            "correct_answer": correct_option.strip()
        }
    except Exception as e:
        print("Parsing failed:", e)
        return {
            "question": "Which brand makes the Mustang?",
            "options": ["Ford", "Chevrolet", "Toyota", "BMW"],
            "correct_answer": "Ford"
        }

# Agent 2: Answer Validator
def validate_answer(question, user_answer):
    prompt = PromptTemplate.from_template(
        "You are validating a multiple-choice quiz answer."
        "Only use the options provided in the question. Do not introduce new options."
        "Start the response with 'Result: Correct\n' or 'Result: Incorrect\n'.\n\n"
        "Question: {question}\n"
        "User Answer: {answer}\n"
        "If the answer is incorrect, clearly mention what the correct answer is and give a short explanation.\n"
    )
    response = llm([HumanMessage(content=prompt.format(question=question, answer=user_answer))])
    return response.content

# Agent 3: Generate Vehicle Brand Image (DALL·E 3)
def generate_vehicle_image(correct_answer: str) -> str:
    prompt_text = "Basic resolution image of a {correct_answer} vehicle brand on white background."
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_text,
            size="512x512", # Basic resolution for faster load
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        # fallback image URL
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png"
