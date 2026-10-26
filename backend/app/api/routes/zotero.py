from fastapi import APIRouter, HTTPException, Query

from app.services import zotero_service

router = APIRouter()


@router.get("/health")
def zotero_health():
    result = zotero_service.get_status()
    if not result.get("ok"):
        raise HTTPException(status_code=503, detail=result)
    return result


@router.get("/search")
def search_references(
    query: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
):
    try:
        items = zotero_service.search_references(query=query, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - depends on external service
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {"query": query, "count": len(items), "items": items}


@router.get("/items")
def list_items(collection_id: str | None = None, limit: int = Query(10, ge=1, le=50)):
    try:
        items = zotero_service.list_collection_items(collection_id=collection_id, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - depends on external service
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {"collection_id": collection_id, "count": len(items), "items": items}


__all__ = ["router"]
