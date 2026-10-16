# AI service: stubs to call OpenAI ChatCompletion. Fill OPENAI_API_KEY in .env to use.
import os
from app.core.config import settings

try:
    import openai
    openai.api_key = settings.OPENAI_API_KEY
except Exception:
    openai = None

PROMPT_PROBLEM = """
Eres un asesor académico. Genera: problema, justificación, preguntas de investigación, objetivos y una hipótesis provisional
Tema: {topic}
Contexto: {context}
"""


def generate_problem(topic: str, context: str = "") -> dict:
    prompt = PROMPT_PROBLEM.format(topic=topic, context=context)
    if not openai:
        return {"error": "openai not configured", "prompt": prompt}
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asesor académico experto."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=800,
        temperature=0.2,
    )
    return {"raw": resp, "text": resp.choices[0].message.content}


def review_chapter_text(chapter_text: str) -> dict:
    prompt = f"Revisa este capítulo en estilo académico y propone mejoras:\n\n{chapter_text}"
    if not openai:
        return {"error": "openai not configured", "prompt": prompt}
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un corrector académico."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=800,
        temperature=0.2,
    )
    return {"raw": resp, "text": resp.choices[0].message.content}
