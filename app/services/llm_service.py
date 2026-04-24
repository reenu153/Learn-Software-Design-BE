# app/services/llm_service.py

from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def evaluate_solution(question: str, solution: str, criteria: str):
    prompt = f"""
                You are a strict technical evaluator.

                Question:
                {question}

                Student Solution:
                {solution}

                Evaluation Criteria:
                {criteria}

                 "feedback_format": 
    "required_sections": [
      "Summary of the student's design",
      "Strengths of the design",
      "Weaknesses and design issues",
      "SOLID principle analysis",
      "Suggested improved design structure",
      "Concrete improvement suggestions"
    ],
    "tone": Constructive, educational, and encouraging. Explain clearly why a design decision is good or problematic so the student can learn.
    passed is true if thge solution meets some or most of the criterias, even if not stritly fully correct. if it seems like student understudnet the principle concept pass, else failed. be lenient but do not pass if it seems liek solution is not good or underlying principle is wrong.

                Respond in JSON format:
                {{
                "feedback": "...",
                "passed": true or false,
                }}
                """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert software design evaluator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    result = json.loads(response.choices[0].message.content)

    return result
