# app/services/llm_service.py

from openai import OpenAI
import os
import json
from app.prompts.strategy_3 import prompt_without_crieria

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def evaluate_solution(question: str, solution: str, criteria: str):
    print("Solution", solution)
    prompt = prompt_without_crieria.format(question=question, solution=solution, criteria=criteria)

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You are an expert software design evaluator."},
            {"role": "user", "content": prompt}
        ],
        # temperature=0.2,
        response_format={"type": "json_object"},
    )
    result = json.loads(response.choices[0].message.content)

    return result






