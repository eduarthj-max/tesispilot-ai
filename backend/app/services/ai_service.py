# add summarize helper to ai_service
from app.core.config import settings

try:
    import openai
    openai.api_key = settings.OPENAI_API_KEY
except Exception:
    openai = None

PROMPT_SUMMARIZE = """
Resume este texto académico en 6-8 frases claras y separadas en párrafos breves. Indica objetivos, metodología y hallazgos principales cuando sea posible.
Texto:
{txt}
"""

from typing import Optional

def summarize_text(text: str) -> dict:
    prompt = PROMPT_SUMMARIZE.format(txt=text[:3000])
    if not openai:
        return {"error": "openai not configured", "prompt": prompt}
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Eres un asistente que resume artículos académicos."}, {"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.2,
    )
    return {"raw": resp, "text": resp.choices[0].message.content}
