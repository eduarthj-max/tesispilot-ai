# TesisPilot - Backend MVP (FastAPI)

## Requisitos
- Docker
- Python 3.11+
- PostgreSQL

## 1) Variables de entorno
Copia `.env.example` a `.env` y cambia los valores.

```bash
cp .env.example .env
```

Añade tus credenciales de Zotero si deseas usar la integración con la biblioteca académica:

```env
ZOTERO_API_URL=https://api.zotero.org
ZOTERO_API_KEY=your_zotero_api_key_here
ZOTERO_USER_ID=your_zotero_user_id_here
ZOTERO_LIBRARY_TYPE=user
```

## 2) Levantar entorno local
```bash
docker-compose up --build
```

## 3) Instalar y correr manualmente (opcional)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints principales
- GET `/` 
- POST `/api/theses`
- GET `/api/theses`
- GET `/api/theses/{id}`
- PUT `/api/theses/{id}`
- DELETE `/api/theses/{id}`
- POST `/api/chapters`
- GET `/api/chapters/by-thesis/{thesis_id}`
- GET `/api/chapters/{chapter_id}`
- PUT `/api/chapters/{chapter_id}`
- DELETE `/api/chapters/{chapter_id}`
- GET `/api/zotero/health`
- GET `/api/zotero/search?query=...`
- GET `/api/zotero/items?collection_id=...`

## Siguientes pasos recomendados
1. Añadir autenticación JWT o Clerk.
2. Añadir Alembic.
3. Integrar subida de PDFs.
4. Crear frontend en Next.js.
5. Añadir tests y CI.
6. Conectar Zotero como biblioteca central de referencias académicas.


path":"README.md