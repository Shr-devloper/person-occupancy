# Phase 2: Raspberry Pi Integration

## Goal

Run the CV engine reliably on Raspberry Pi 4 with auto-start, camera access, logs, and recovery after reboot.

## Folder structure

```text
cv_engine/systemd/smart-seat-cv.service
/opt/smart-seat/cv_engine
/var/log/smart-seat-cv.log
```

## Commands

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip libgl1 libglib2.0-0 git
sudo mkdir -p /opt/smart-seat
sudo cp -r cv_engine /opt/smart-seat/
cd /opt/smart-seat/cv_engine
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
sudo cp systemd/smart-seat-cv.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable smart-seat-cv
sudo systemctl start smart-seat-cv
sudo systemctl status smart-seat-cv
```

## Configuration files

The systemd service reads `/opt/smart-seat/cv_engine/.env`. Set `BACKEND_URL`, `CAMERA_SOURCE`, and `SEAT_CONFIG_PATH` before starting the service.

## Testing instructions

Use `libcamera-hello` for Pi camera modules or `v4l2-ctl --list-devices` for USB cameras. Then check `sudo journalctl -u smart-seat-cv -f`.

## Expected output

The service starts automatically and continuously sends occupancy events to the backend without recording video.

## Common errors and fixes

| Error | Cause | Fix |
| --- | --- | --- |
| Command not found | Tool is not installed or virtual environment is inactive | Re-run the install commands and activate the environment |
| Connection refused | Backend, database, or camera source is not running | Start the dependent service and check host/port values |
| Permission denied | Linux user cannot access camera, service, or Docker socket | Add the user to the correct group or run the setup command with sudo |
