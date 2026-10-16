from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from pathlib import Path

from app.db.session import get_db
from app import models
from app.core.security import get_current_user

router = APIRouter()

class ExportRequest(BaseModel):
    format: str = "pdf"


def ensure_export_dir() -> Path:
    p = Path('/tmp/tesispilot_exports')
    p.mkdir(parents=True, exist_ok=True)
    return p


@router.post('/theses/{thesis_id}/export')
def export_thesis(thesis_id: str, payload: ExportRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    thesis = db.query(models.Thesis).filter(models.Thesis.id == thesis_id).first()
    if not thesis:
        raise HTTPException(status_code=404, detail='Thesis not found')
    if thesis.user_id != current_user.id:
        raise HTTPException(status_code=403, detail='Forbidden')

    chapters = db.query(models.Chapter).filter(models.Chapter.thesis_id == thesis_id).order_by(models.Chapter.order_index).all()

    content = f"# {thesis.title}\n\n"
    content += f"## Resumen\n{thesis.abstract or 'Sin resumen.'}\n\n"
    content += f"## Problema de investigación\n{thesis.problem_statement or 'Sin problema de investigación definido.'}\n\n"
    content += f"## Objetivos\n{thesis.objectives or 'Sin objetivos definidos.'}\n\n"

    for ch in chapters:
        content += f"## {ch.title}\n{ch.content or ''}\n\n"

    export_dir = ensure_export_dir()
    safe_name = ''.join(c if c.isalnum() or c in ('-', '_') else '_' for c in thesis.title.lower())[:80]
    out_path = export_dir / f"{safe_name}.{payload.format}"

    if payload.format == 'md':
        out_path.write_text(content, encoding='utf-8')
    elif payload.format == 'docx':
        try:
            from docx import Document
            doc = Document()
            doc.add_heading(thesis.title, level=1)
            doc.add_paragraph(thesis.abstract or 'Sin resumen.')
            for ch in chapters:
                doc.add_heading(ch.title, level=2)
                doc.add_paragraph(ch.content or '')
            doc.save(str(out_path))
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f'Could not generate DOCX: {exc}')
    elif payload.format == 'pdf':
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
            styles = getSampleStyleSheet()
            doc = SimpleDocTemplate(str(out_path), pagesize=letter)
            story = []
            story.append(Paragraph(thesis.title, styles['Title']))
            story.append(Spacer(1, 0.25 * inch))
            story.append(Paragraph(f"Resumen: {thesis.abstract or 'Sin resumen.'}", styles['BodyText']))
            story.append(Spacer(1, 0.20 * inch))
            for ch in chapters:
                story.append(Paragraph(ch.title, styles['Heading2']))
                story.append(Paragraph(ch.content or '', styles['BodyText']))
                story.append(Spacer(1, 0.15 * inch))
            doc.build(story)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f'Could not generate PDF: {exc}')
    else:
        raise HTTPException(status_code=400, detail='Unsupported format. Use md, docx, or pdf')

    return {'filename': out_path.name, 'download_url': f'/api/download/{out_path.name}'}


@router.get('/download/{filename}')
def download_file(filename: str):
    file_path = Path('/tmp/tesispilot_exports') / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail='File not found')
    return FileResponse(file_path, filename=filename)
