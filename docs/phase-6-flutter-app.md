# Phase 6: Flutter App

## Goal

Provide a Flutter mobile app using Riverpod and Dio for splash, login, dashboard, live camera, analytics, notifications, and settings screens.

## Folder structure

```text
flutter_app/
├── pubspec.yaml
└── lib/main.dart
```

## Commands

```bash
cd flutter_app
flutter pub get
flutter run --dart-define=API_URL=http://10.0.2.2:8000
```

## Configuration files

Android emulator uses `10.0.2.2` to reach the host machine. Physical phones need your computer IP address and firewall access.

## Testing instructions

Login with a backend account, open dashboard, then send test occupancy events and refresh screens.

## Expected output

The dashboard displays occupancy metrics and notifications fetched from the FastAPI backend.

## Common errors and fixes

| Error | Cause | Fix |
| --- | --- | --- |
| Command not found | Tool is not installed or virtual environment is inactive | Re-run the install commands and activate the environment |
| Connection refused | Backend, database, or camera source is not running | Start the dependent service and check host/port values |
| Permission denied | Linux user cannot access camera, service, or Docker socket | Add the user to the correct group or run the setup command with sudo |
