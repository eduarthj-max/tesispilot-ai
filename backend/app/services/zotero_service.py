import json
import urllib.parse
import urllib.request
from typing import Any

from app.core.config import settings


def _build_url(path: str, params: dict[str, Any] | None = None) -> str:
    base = (settings.ZOTERO_API_URL or "").rstrip("/")
    if not base:
        raise ValueError("ZOTERO_API_URL is not configured")
    url = f"{base}{path}"
    if params:
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        url = f"{url}?{query}"
    return url


def _headers() -> dict[str, str]:
    headers: dict[str, str] = {"Accept": "application/json"}
    if settings.ZOTERO_API_KEY:
        headers["Zotero-API-Key"] = settings.ZOTERO_API_KEY
    return headers


def _fetch_json(url: str) -> Any:
    request = urllib.request.Request(url, headers=_headers())
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read().decode("utf-8")
        return json.loads(body) if body else {}


def _normalize_item(raw_item: dict[str, Any]) -> dict[str, Any]:
    data = raw_item.get("data", {}) if isinstance(raw_item, dict) else {}
    creators = data.get("creators") or []
    author_names: list[dict[str, str]] = []

    for creator in creators:
        creator_type = creator.get("creatorType", "author")
        first = creator.get("firstName")
        last = creator.get("lastName")
        if first or last:
            full_name = " ".join(part for part in [first, last] if part).strip()
            if full_name:
                author_names.append({"name": full_name, "type": creator_type})

    title = data.get("title") or "Sin título"
    publication_year = None
    date_value = data.get("date") or data.get("year") or ""
    if isinstance(date_value, str):
        year_text = date_value[:4]
        if year_text.isdigit():
            publication_year = int(year_text)
    elif isinstance(date_value, int):
        publication_year = date_value

    return {
        "key": raw_item.get("key"),
        "title": title,
        "item_type": data.get("itemType"),
        "publication_year": publication_year,
        "authors": author_names,
        "url": data.get("url"),
        "doi": data.get("DOI"),
        "abstract": data.get("abstractNote"),
        "source": data.get("publicationTitle") or data.get("journalAbbreviation") or data.get("bookTitle"),
        "raw": raw_item,
    }


def get_status() -> dict[str, Any]:
    if not settings.ZOTERO_API_URL:
        return {"ok": False, "error": "ZOTERO_API_URL not configured"}
    if not settings.ZOTERO_USER_ID:
        return {"ok": False, "error": "ZOTERO_USER_ID not configured"}

    try:
        path = f"/{settings.ZOTERO_LIBRARY_TYPE}s/{settings.ZOTERO_USER_ID}/items"
        url = _build_url(path, {"limit": 1})
        _fetch_json(url)
        return {
            "ok": True,
            "library_type": settings.ZOTERO_LIBRARY_TYPE,
            "user_id": settings.ZOTERO_USER_ID,
            "api_url": settings.ZOTERO_API_URL,
        }
    except Exception as exc:  # pragma: no cover - depends on external service
        return {"ok": False, "error": str(exc)}


def search_references(query: str, limit: int = 10) -> list[dict[str, Any]]:
    if not query or not query.strip():
        return []
    if not settings.ZOTERO_USER_ID:
        raise ValueError("ZOTERO_USER_ID is not configured")

    library_type = settings.ZOTERO_LIBRARY_TYPE
    path = f"/{library_type}s/{settings.ZOTERO_USER_ID}/items"
    url = _build_url(path, {"q": query.strip(), "limit": max(1, min(limit, 50))})
    data = _fetch_json(url)

    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get("results") or []
    else:
        items = []

    return [_normalize_item(item) for item in items if isinstance(item, dict)]


def list_collection_items(collection_id: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
    if not settings.ZOTERO_USER_ID:
        raise ValueError("ZOTERO_USER_ID is not configured")

    library_type = settings.ZOTERO_LIBRARY_TYPE
    if collection_id:
        path = f"/{library_type}s/{settings.ZOTERO_USER_ID}/collections/{collection_id}/items"
    else:
        path = f"/{library_type}s/{settings.ZOTERO_USER_ID}/items"
    url = _build_url(path, {"limit": max(1, min(limit, 50))})
    data = _fetch_json(url)

    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get("results") or []
    else:
        items = []

    return [_normalize_item(item) for item in items if isinstance(item, dict)]


__all__ = ["get_status", "search_references", "list_collection_items"]
