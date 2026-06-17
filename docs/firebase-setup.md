# Firebase Cloud Messaging Setup

## Backend

1. Open Firebase Console.
2. Create or select a project.
3. Go to Project Settings > Service accounts.
4. Generate a new private key.
5. Save it outside git, for example:

```text
backend/secrets/firebase-service-account.json
```

6. Set:

```bash
FCM_CREDENTIALS_PATH=backend/secrets/firebase-service-account.json
```

For Docker, mount the file and set the container path.

## Flutter

1. Install FlutterFire CLI.
2. Run from `flutter_app`:

```bash
dart pub global activate flutterfire_cli
flutterfire configure
```

3. This generates Firebase options files.
4. Run:

```bash
flutter pub get
flutter run
```

## Notification triggers

Implemented storage notifications:

- seat becomes occupied
- seat becomes available

Production extension points:

- scheduled job checks seats occupied longer than `NOTIFICATION_OCCUPIED_HOURS`
- camera heartbeat marks cameras offline
- analytics job sends high occupancy alerts
