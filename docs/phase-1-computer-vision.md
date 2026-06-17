# Phase 1: Computer Vision Module

## Goal

Detect people with YOLOv8 Nano, compare detections with a manually configured seat rectangle, and emit occupied/empty transitions only.

## Folder structure

```text
cv_engine/
├── app/
│   ├── main.py
│   ├── detection.py
│   ├── occupancy.py
│   ├── seat_region.py
│   └── backend_client.py
├── requirements.txt
└── seat_config.example.json
```

## Commands

```bash
cd cv_engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

## Configuration files

Edit `cv_engine/.env` to choose the camera. Use `CAMERA_SOURCE=0` for the first USB camera or an RTSP URL for an IP camera. Edit `seat_config.example.json` and set `x1,y1,x2,y2` around the chair in the image.

## Testing instructions

Run the engine with a person moving in and out of the seat. Watch logs for `Sent occupancy event` after the configured debounce frame threshold.

## Expected output

When the seat changes from empty to occupied, the engine posts `state=occupied`; when it changes back, it posts `state=empty`.

## Common errors and fixes

| Error | Cause | Fix |
| --- | --- | --- |
| Command not found | Tool is not installed or virtual environment is inactive | Re-run the install commands and activate the environment |
| Connection refused | Backend, database, or camera source is not running | Start the dependent service and check host/port values |
| Permission denied | Linux user cannot access camera, service, or Docker socket | Add the user to the correct group or run the setup command with sudo |
