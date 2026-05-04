# app/services/llm_service.py

from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def evaluate_solution(question: str, solution: str, criteria: str):
    print("Solution", solution)
    prompt = f"""
                You are a strict technical evaluator. Evaluate the student solution based on the question and criteria given. 

                Question:
                {question}

                Student Solution:
                {solution}

                Evaluation Criteria:
                {criteria}

                Feedback format - include these sections:
                - Summary of the student's design
                - Strengths of the design
                - Weaknesses and design issues
                - Suggested improved design structure
                - Concrete improvement suggestions
                
                Tone: Constructive, educational, and encouraging. Explain clearly why a design decision is good or problematic so the student can learn.

                Passing rule: passed is TRUE if the student demonstrates they understand the core concept being tested, even if the solution is incomplete, suboptimal, or has minor mistakes. Only set passed to FALSE if the student has fundamentally misunderstood or completely ignored the main principle. Give benefit of the doubt — a partially correct solution that shows awareness of the principle should pass.

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
