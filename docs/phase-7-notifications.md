# Phase 7: Notifications

## Goal

Integrate Firebase Cloud Messaging so the backend can notify web/mobile clients when seats are occupied too long, become available, cameras go offline, or occupancy is high.

## Folder structure

```text
backend/app/services/notifications.py
backend/app/routers/notifications.py
flutter_app/lib/main.dart
web_dashboard/src/pages/Notifications.tsx
```

## Commands

```bash
firebase projects:create smart-seat-demo # or use Firebase console
# Download service-account.json to backend/secrets/firebase-service-account.json
export FCM_CREDENTIALS_PATH=/app/secrets/firebase-service-account.json
```

## Configuration files

Never commit Firebase service account JSON. Mount it as a Docker secret or private file and set `FCM_CREDENTIALS_PATH`.

## Testing instructions

Register a mobile device token through `POST /notifications/device-token`, then trigger a seat event and check the notification center.

## Expected output

Notification rows are stored in PostgreSQL. Push delivery is attempted only when Firebase credentials and device tokens exist.

## Common errors and fixes

| Error | Cause | Fix |
| --- | --- | --- |
| Command not found | Tool is not installed or virtual environment is inactive | Re-run the install commands and activate the environment |
| Connection refused | Backend, database, or camera source is not running | Start the dependent service and check host/port values |
| Permission denied | Linux user cannot access camera, service, or Docker socket | Add the user to the correct group or run the setup command with sudo |
