from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import theses, chapters, ai, versions, export, zotero
from app.db.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title='TesisPilot API - MVP')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(theses.router, prefix='/api/theses', tags=['theses'])
app.include_router(chapters.router, prefix='/api/chapters', tags=['chapters'])
app.include_router(ai.router, prefix='/api', tags=['ai'])
app.include_router(versions.router, prefix='/api', tags=['versions'])
app.include_router(export.router, prefix='/api', tags=['export'])
app.include_router(zotero.router, prefix='/api/zotero', tags=['zotero'])


@app.get('/')
def root():
    return {'message': 'TesisPilot API running'}
