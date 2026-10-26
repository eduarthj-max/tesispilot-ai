from app.core.config import settings
from app.services import zotero_service

try:
    import anthropic
except Exception:  # pragma: no cover
    anthropic = None

try:
    import openai
    if settings.OPENAI_API_KEY:
        openai.api_key = settings.OPENAI_API_KEY
except Exception:  # pragma: no cover
    openai = None

PROMPT_SUMMARIZE = """
Resume este texto académico en 6-8 frases claras y separadas en párrafos breves. Indica objetivos, metodología y hallazgos principales cuando sea posible.
Texto:
{txt}
"""

PROMPT_PROBLEM = """
Eres un asesor académico experto en metodologías de investigación.
Basado en el tema de la tesis, genera:
1. problema de investigación
2. justificación
3. preguntas de investigación
4. objetivos generales
5. objetivos específicos
6. hipótesis provisional

Usa un estilo formal y académico.
No inventes referencias.
Si falta información, haz preguntas antes de concluir.
Tema: {topic}
Contexto extra: {context}
"""

PROMPT_REVIEW = """
Revisa este capítulo en estilo académico.
Evalúa: claridad, coherencia, gramática, flujo lógico, citas y referencias, consistencia con objetivos, posibles contradicciones.
Devuelve: resumen ejecutivo, errores detectados, sugerencias de redacción, propuestas de mejora por párrafo y observaciones de método o evidencia.
Texto:
{txt}
"""


def _claude_client():
    if anthropic is None or not settings.ANTHROPIC_API_KEY:
        return None
    return anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


def _format_zotero_items(items: list[dict]) -> str:
    if not items:
        return "No se encontraron referencias."

    lines = []
    for index, item in enumerate(items, start=1):
        authors = ", ".join(author.get("name", "Autor") for author in item.get("authors", [])[:3])
        title = item.get("title", "Sin título")
        year = item.get("publication_year") or "s.f."
        source = item.get("source") or "Sin fuente"
        doi = item.get("doi") or ""
        url = item.get("url") or ""
        lines.append(f"{index}. {authors} ({year}). {title}. {source}. {('DOI: ' + doi) if doi else ''} {url}".strip())
    return "\n".join(lines)


def summarize_text(text: str) -> dict:
    prompt = PROMPT_SUMMARIZE.format(txt=text[:3000])

    if _claude_client():
        client = _claude_client()
        response = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}],
        )
        return {"raw": response, "text": response.content[0].text}

    if not openai:
        return {"error": "openai not configured", "prompt": prompt}

    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente que resume artículos académicos."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.2,
    )
    return {"raw": resp, "text": resp.choices[0].message.content}


def generate_problem(topic: str, context: str = "") -> dict:
    prompt = PROMPT_PROBLEM.format(topic=topic or "Tema no especificado", context=context or "")

    if _claude_client():
        client = _claude_client()
        response = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}],
        )
        return {"text": response.content[0].text, "provider": "claude"}

    if not openai:
        return {"error": "no ai provider configured", "prompt": prompt}

    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200,
        temperature=0.3,
    )
    return {"text": resp.choices[0].message.content, "provider": "openai"}


def review_chapter_text(text: str) -> dict:
    prompt = PROMPT_REVIEW.format(txt=text[:8000])

    if _claude_client():
        client = _claude_client()
        response = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=1400,
            messages=[{"role": "user", "content": prompt}],
        )
        return {"text": response.content[0].text, "provider": "claude"}

    if not openai:
        return {"error": "no ai provider configured", "prompt": prompt}

    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1400,
        temperature=0.2,
    )
    return {"text": resp.choices[0].message.content, "provider": "openai"}


def recommend_literature(topic: str, limit: int = 5) -> dict:
    try:
        refs = zotero_service.search_references(topic, limit=limit)
    except Exception as exc:  # pragma: no cover - depends on external service
        return {"error": f"Zotero error: {exc}", "references": []}

    if not refs:
        return {"error": "No se encontraron referencias en Zotero para ese tema.", "references": []}

    context = _format_zotero_items(refs)

    if _claude_client():
        client = _claude_client()
        prompt = f"""
Eres un asistente académico.
Tema de tesis: {topic}

Bibliografía disponible desde Zotero:
{context}

Tareas:
1. Selecciona las referencias más relevantes para este tema.
2. Explica por qué cada una sirve para la tesis.
3. Identifica brechas o lagunas de literatura.
4. Devuelve una respuesta breve, clara y académica en español.
"""
        response = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=1400,
            messages=[{"role": "user", "content": prompt}],
        )
        return {
            "references": refs,
            "analysis": response.content[0].text,
            "provider": "claude",
        }

    if not openai:
        return {"error": "OpenAI and Anthropic are not configured", "references": refs, "context": context}

    prompt = f"Eres un asistente académico. Tema: {topic}\n\nBibliografía\n{context}\n\nSelecciona las referencias más relevantes y explica por qué sirven para la tesis."
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1400,
        temperature=0.2,
    )
    return {
        "references": refs,
        "analysis": resp.choices[0].message.content,
        "provider": "openai",
    }


__all__ = [
    "summarize_text",
    "generate_problem",
    "review_chapter_text",
    "recommend_literature",
]
