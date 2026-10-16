from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import theses, chapters, ai
from app.db.session import engine, Base

# Create DB tables (for dev). For production use Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TesisPilot API - MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(theses.router, prefix="/api/theses", tags=["theses"])
app.include_router(chapters.router, prefix="/api/chapters", tags=["chapters"])
# AI endpoints (generate problem, review chapter)
app.include_router(ai.router, prefix="/api", tags=["ai"])


@app.get("/")
def root():
    return {"message": "TesisPilot API running"}
