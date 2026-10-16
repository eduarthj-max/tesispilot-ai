# TesisPilot - Versión final (v1.0.0)

Esta es la versión final del MVP "TesisPilot AI" — un asistente para planificar, investigar, redactar y exportar una tesis con soporte de IA.

Repositorio: https://github.com/eduarthj-max/tesispilot-ai

Resumen rápido
- Backend: FastAPI (Python)
- Frontend: Next.js + TypeScript + Tailwind (UI minimal pero funcional)
- DB: PostgreSQL
- IA: integración con OpenAI (configurable vía OPENAI_API_KEY)
- Autenticación: JWT (registro, login, /api/auth/me)
- Funcionalidades principales:
  - gestión de tesis y capítulos
  - subida de documentos y referencias (esquema)
  - generación y revisión por IA (prompts controlados)
  - versiones de capítulos con historial
  - exportación final a Markdown / DOCX / PDF (TOC, numeración, referencias APA/IEEE, anexos)
  - protección por usuario: cada tesis asociada a su creador
  - frontend con flujo completo: registro, login, dashboard, editor, panel IA, export

Archivos añadidos en esta versión
- README.md (actualizado con instrucciones finales)
- RELEASE_NOTES.md (este archivo)
- DEPLOY.md (guía de despliegue a Vercel / Render / Docker)

Cómo arrancar localmente (rápido)
1. Clona el repo

```bash
git clone https://github.com/eduarthj-max/tesispilot-ai.git
cd tesispilot-ai
```

2. Copia variables de entorno y ajusta

```bash
cp .env.example .env
# Edita .env: SECRET_KEY, DATABASE_URL (si cambias), OPENAI_API_KEY (opcional)
```

3. Levanta servicios con Docker Compose

```bash
docker-compose up --build
```

Esto crea los servicios:
- Postgres en localhost:5432
- Backend FastAPI en localhost:8000

4. Frontend (dev)

```bash
cd frontend
npm install
npm run dev
# abre http://localhost:3000
```

Notas importantes
- Si cambias el esquema en producción, usa Alembic (hay migraciones iniciales en backend/alembic).
- OpenAI: para usar IA real rellena OPENAI_API_KEY y reinicia el backend.
- Persistencia de archivos export: actualmente /tmp/tesispilot_exports (en producción usar S3 y presigned URLs).

Pruebas recomendadas
- Registro de usuario -> Login -> Crear tesis -> Añadir capítulos -> Probar IA -> Exportar PDF
- Validar permisos: crear tesis con user A y verificar que user B no puede editar ni exportar

Siguientes pasos sugeridos
- Poner frontend en Vercel y backend en Render/Railway (guía en DEPLOY.md)
- Cambiar almacenamiento de export a S3
- Añadir integración con Zotero para referencias
- Añadir pruebas e2e (Playwright/Cypress)

---

Gracias — si quieres, puedo desplegar la demo en una instancia (por ejemplo Render/Vercel) y darte la URL pública. ¿Lo despliego ahora?