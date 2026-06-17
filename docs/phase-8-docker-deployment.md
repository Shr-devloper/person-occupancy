# Phase 8: Docker Deployment

## Goal

Run PostgreSQL, backend, web dashboard, and Nginx reverse proxy as containers with production-ready environment separation.

## Folder structure

```text
infra/docker-compose.yml
infra/nginx/conf.d/default.conf
backend/Dockerfile
web_dashboard/Dockerfile
cv_engine/Dockerfile
```

## Commands

```bash
cp backend/.env.example backend/.env
docker compose -f infra/docker-compose.yml up --build
docker compose -f infra/docker-compose.yml ps
```

## Configuration files

For production, use strong passwords, a long JWT secret, HTTPS certificates in `infra/nginx/certs`, and a restricted CORS allowlist.

## Testing instructions

Open `http://localhost:8080` for the dashboard and `http://localhost:8080/api/health` for the backend through Nginx.

## Expected output

All containers become healthy/running and the backend applies migrations on startup.

## Common errors and fixes

| Error | Cause | Fix |
| --- | --- | --- |
| Command not found | Tool is not installed or virtual environment is inactive | Re-run the install commands and activate the environment |
| Connection refused | Backend, database, or camera source is not running | Start the dependent service and check host/port values |
| Permission denied | Linux user cannot access camera, service, or Docker socket | Add the user to the correct group or run the setup command with sudo |
