# README - Versión final

He actualizado y consolidado el README general con instrucciones para la versión final. Revisa `RELEASE_NOTES.md` y `DEPLOY.md` para detalle de despliegue.

Principales comandos:
- Levantar (Docker): `docker-compose up --build`
- Frontend dev: `cd frontend && npm install && npm run dev`
- Backend dev: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload`

Acceso a la API:
- Documentación básica en `/docs` (FastAPI) cuando el backend esté en marcha.

Contacto
- Si quieres que despliegue la demo pública o que haga una versión empaquetada para presentación te lo preparo y lo subo.