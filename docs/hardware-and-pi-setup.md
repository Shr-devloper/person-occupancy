# Hardware, Wiring, Raspberry Pi OS, and Camera Setup

## Hardware list

1. Raspberry Pi 4 Model B, 4GB RAM or higher.
2. Official 5V 3A USB-C power supply.
3. 32GB or larger Class 10 microSD card.
4. USB camera or RTSP/IP camera.
5. Ethernet cable or stable Wi-Fi.
6. Camera mount or tripod.
7. Optional fan/heatsink for long-running YOLO inference.

## Wiring diagram

```text
+-------------------+       USB cable        +------------------+
| USB Camera        | ---------------------> | Raspberry Pi 4   |
+-------------------+                        |                  |
                                             | Ethernet/Wi-Fi   | ---> Backend API
+-------------------+       USB-C power      |                  |
| 5V 3A Adapter     | ---------------------> | Power Port       |
+-------------------+                        +------------------+
```

For an IP camera:

```text
IP Camera ---> Office Network Router/Switch ---> Raspberry Pi ---> Backend API
```

## Install Raspberry Pi OS

1. Install Raspberry Pi Imager on your laptop.
2. Select Raspberry Pi OS 64-bit Lite for headless deployment.
3. Choose the microSD card.
4. In advanced options, set hostname, username, password, Wi-Fi, locale, and SSH.
5. Flash the card, insert it into the Pi, and power on.
6. SSH into the Pi:

```bash
ssh pi@smart-seat-pi.local
```

## Configure a USB camera

```bash
sudo apt update
sudo apt install -y v4l-utils
v4l2-ctl --list-devices
```

If the device is `/dev/video0`, set:

```bash
CAMERA_SOURCE=0
```

## Configure an IP camera

Find the RTSP URL in the camera admin page. Common examples:

```text
rtsp://user:password@192.168.1.50:554/stream1
rtsp://192.168.1.50/live/ch0
```

Set:

```bash
CAMERA_SOURCE=rtsp://user:password@192.168.1.50:554/stream1
```

## Manual seat region setup

1. Temporarily display a frame from the camera.
2. Note pixel coordinates around the chair:
   - `x1,y1`: top-left corner
   - `x2,y2`: bottom-right corner
3. Edit `cv_engine/seat_config.example.json`.

Example:

```json
{"region": {"x1": 220, "y1": 160, "x2": 520, "y2": 460}}
```

## Logging and error handling

The systemd service writes logs to:

```text
/var/log/smart-seat-cv.log
/var/log/smart-seat-cv-error.log
```

The CV engine:

- validates that the camera opens
- logs failed backend calls
- debounces detection with frame thresholds
- restarts automatically through systemd
