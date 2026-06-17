# Phase 3: Backend Development

## Goal

Expose JWT-secured FastAPI endpoints for authentication, cameras, seats, occupancy logs, analytics, and notifications.

## Folder structure

```text
backend/
├── app/routers/
├── app/services/
├── app/models.py
├── app/schemas.py
├── alembic/
└── requirements.txt
```

## Commands

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## Configuration files

Set `DATABASE_URL`, `JWT_SECRET_KEY`, `CORS_ORIGINS`, and optionally `FCM_CREDENTIALS_PATH` in `backend/.env`.

## Testing instructions

Open `http://localhost:8000/docs`, call `POST /register`, `POST /login`, authorize with the token, then create a camera and seat.

## Expected output

API docs load, protected endpoints require JWT, and occupancy events create logs.

## Common errors and fixes

| Error | Cause | Fix |
| --- | --- | --- |
| Command not found | Tool is not installed or virtual environment is inactive | Re-run the install commands and activate the environment |
| Connection refused | Backend, database, or camera source is not running | Start the dependent service and check host/port values |
| Permission denied | Linux user cannot access camera, service, or Docker socket | Add the user to the correct group or run the setup command with sudo |
