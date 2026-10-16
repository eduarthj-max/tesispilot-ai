# Guía de despliegue (TesisPilot AI) — DEPLOY.md

Este documento explica opciones para desplegar la versión final del proyecto.

Variables necesarias (.env)
- DATABASE_URL (postgres://USER:PASS@HOST:PORT/DB)
- SECRET_KEY (string largo y secreto)
- OPENAI_API_KEY (opcional, para IA)
- NEXT_PUBLIC_API_URL (para el frontend apuntar al backend)

Opción A — Frontend en Vercel, Backend en Render (recomendado para demo rápida)

1) Backend (Render)
- Crea un servicio web en Render (o Railway)
- Conecta repo y selecciona la carpeta `backend` como root o usa comando de arranque:
  - Build Command: `pip install -r backend/requirements.txt`
  - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Añade variables de entorno en Render: DATABASE_URL, SECRET_KEY, OPENAI_API_KEY (si aplica)
- Asegúrate de usar una base Postgres administrada por el proveedor o un Add-on

2) Frontend (Vercel)
- Conecta repo en Vercel
- Configura proyecto apuntando a `frontend` como root
- Env vars en Vercel: NEXT_PUBLIC_API_URL = https://<tu-backend>
- Deploy automático desde main

Opción B — Todo con Docker Compose (servidor VPS)
- Copia `docker-compose.yml` y construye imágenes
- Asegura subir los servicios a systemd o usar Docker Swarm / k8s
- Monta un volumen para `/tmp/tesispilot_exports` o cambia export path a un volumen o S3

Opción C — Producción con S3 para export y RDS para DB
- Backend: configurar AWS RDS Postgres, S3 bucket para exports
- Frontend: build estático en Vercel
- Cambios mínimos: ajustar backend para subir archivos a S3 y devolver presigned URLs (recomendado)

Tareas previas al despliegue
- Generar SECRET_KEY seguro
- Crear y aplicar migraciones Alembic
- Probar export en entorno de staging
- Revisar límites de OpenAI / costes si se usa IA intensiva

SSL / Seguridad
- Usa HTTPS en frontend y backend
- Protege tokens y usa cookies HttpOnly para producción si quieres mayor seguridad

Monitoreo y logs
- Configura logging centralizado (Papertrail / LogDNA / Datadog)
- Métricas: requests, uso de tokens IA, errores en generación de export

Backups
- Respaldos periódicos de la base de datos
- Guardado de exportaciones en S3 para persistencia

Si quieres, te preparo los scripts de despliegue para Render/Vercel y/o la integración S3 para export. ¿Cuál prefieres que automatice?