# Phase 5: Web Dashboard

## Goal

Provide a React TypeScript dashboard with login, camera management, seat management, live view placeholder, analytics charts, notifications, and profile pages.

## Folder structure

```text
web_dashboard/
├── src/pages/
├── src/api/client.ts
├── package.json
└── Dockerfile
```

## Commands

```bash
cd web_dashboard
npm install
npm run dev
```

## Configuration files

Set `VITE_API_URL=http://localhost:8000` for direct local API access. Docker uses `/api` through Nginx.

## Testing instructions

Register/login through the backend, paste credentials into the login page, create cameras/seats, and view analytics charts.

## Expected output

Dashboard widgets show total seats, occupied seats, available seats, occupancy percentage, and camera status.

## Common errors and fixes

| Error | Cause | Fix |
| --- | --- | --- |
| Command not found | Tool is not installed or virtual environment is inactive | Re-run the install commands and activate the environment |
| Connection refused | Backend, database, or camera source is not running | Start the dependent service and check host/port values |
| Permission denied | Linux user cannot access camera, service, or Docker socket | Add the user to the correct group or run the setup command with sudo |
