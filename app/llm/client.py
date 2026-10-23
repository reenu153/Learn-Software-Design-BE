import json
from openai import AsyncOpenAI
from app.core.config import settings
from app.prompts.strategy_3 import prompt_without_crieria

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY, timeout=60.0)


async def evaluate_solution(question: str, solution: str, criteria: str) -> dict:
    prompt = prompt_without_crieria.format(question=question, solution=solution, criteria=criteria)

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are an expert software design evaluator."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)