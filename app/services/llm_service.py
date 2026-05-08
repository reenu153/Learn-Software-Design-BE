# app/services/llm_service.py

from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def evaluate_solution(question: str, solution: str, criteria: str):
    print("Solution", solution)
    prompt = prompt_2.format(question=question, solution=solution, criteria=criteria)

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


prompt_1= """
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


prompt_2 = """
You are an expert software design educator evaluating a student's solution to a design problem.
Your job is NOT to check for a perfect solution — it is to identify exactly where the student's 
thinking is right, where it breaks down, and give them the smallest actionable steps to improve.

---

QUESTION:
{question}

STUDENT SOLUTION:
{solution}

EVALUATION CRITERIA:
{criteria}

---

EVALUATION INSTRUCTIONS:

Step 1 — Read charitably.
Before finding faults, identify what the student clearly understands. 
A solution can be incomplete or imperfect but still show genuine understanding of the core concept.

Step 2 — Check must-haves one by one.
For each must-have criterion, decide: fully met / partially met / missing.
Explain what you see in the student's solution that led to your decision.

Step 3 — Check must-not-haves one by one.
For each must-not-have, decide: present (problem) / absent (good).
If present, quote or reference the specific part of the student's solution that violates it.

Step 4 — Match against common mistakes.
Identify which (if any) common mistakes the student has made.
Do NOT mention mistakes that are not present — only flag what actually applies.

Step 5 — Write targeted feedback using this structure:

  a) WHAT YOU GOT RIGHT (1–3 sentences)
     Be specific. Reference actual elements of their solution.

  b) WHAT TO FIX (up to 3 numbered items, prioritised by importance)
     Each item must follow this pattern:
       - State the specific problem visible in their solution
       - Explain WHY it is a problem (what principle it violates)
       - Give a concrete, minimal fix (what to change/add, not a full redesign)

  c) SELF-CHECK QUESTIONS (2 questions the student can ask themselves)
     These should be derived from the must-have criteria and test whether the 
     student's solution actually solves the brief — not generic questions.

  d) NEXT STEP (1–2 sentences)
     The single smallest change that would most improve this solution right now.

Step 6 — Pass/fail decision.
passed = TRUE if the student demonstrates awareness of the core concept being tested,
even if implementation is incomplete or has minor errors.
passed = FALSE only if the student has fundamentally misunderstood or completely 
ignored the primary design principle. Give benefit of the doubt.

---

TONE RULES:
- Write as a knowledgeable teacher, not a judge.
- Never say "you forgot", "you failed to", or "you missed". 
  Say "X is not yet shown in the diagram" or "the next step is to add Y".
- Be specific — reference actual elements of the student's solution by name.
- Do not praise things that are wrong just to be nice.
- Do not mention criteria the student has already met as problems.
- Do not suggest a full redesign if small additions would fix the issues.

---

Respond in this exact JSON format:
{{
  "feedback":{{"what you got right": "...",
  "what to fix": [
    {{
      "issue": "...",
      "why it matters": "...",
      "fix": "..."
    }}
  ],
  "self check questions": ["...", "..."],
  "next step": "...",}},
  "passed": true or false
}}
"""