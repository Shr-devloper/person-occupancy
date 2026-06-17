# REST API Request and Response Examples

Set a token after login:

```bash
TOKEN="paste-access-token-here"
```

## POST /register

Request:

```json
{"name":"Admin User","email":"admin@example.com","password":"StrongPass123","role":"admin"}
```

Response:

```json
{"id":1,"name":"Admin User","email":"admin@example.com","role":"admin","is_active":true}
```

## POST /login

Request:

```json
{"email":"admin@example.com","password":"StrongPass123"}
```

Response:

```json
{"access_token":"eyJ...","token_type":"bearer"}
```

## GET /cameras

```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/cameras
```

## POST /camera

```bash
curl -X POST http://localhost:8000/camera \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"camera_name":"Cabin A Camera","location":"Floor 1 Cabin A","ip_address":"192.168.1.40","status":"online"}'
```

## PUT /camera/{camera_id}

```bash
curl -X PUT http://localhost:8000/camera/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"maintenance"}'
```

## DELETE /camera/{camera_id}

```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" http://localhost:8000/camera/1
```

## GET /seats

```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/seats
```

## POST /seat

```bash
curl -X POST http://localhost:8000/seat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"seat_name":"Cabin A Chair","camera_id":1,"region_x1":220,"region_y1":160,"region_x2":520,"region_y2":460}'
```

## POST /occupancy/events

Called by Raspberry Pi:

```json
{"seat_id":1,"camera_id":1,"state":"occupied","event_time":"2026-06-17T09:00:00Z","confidence":0.91}
```

Then when empty:

```json
{"seat_id":1,"camera_id":1,"state":"empty","event_time":"2026-06-17T11:30:00Z","confidence":null}
```

The backend stores duration as seconds: `9000` seconds = `2.5` hours.

## GET /occupancy/daily

```bash
curl -H "Authorization: Bearer $TOKEN" 'http://localhost:8000/occupancy/daily?day=2026-06-17'
```

Response:

```json
{"label":"2026-06-17","occupied_seconds":9000,"occupancy_percentage":10.42}
```

## GET /occupancy/weekly

Returns seven daily points for the selected week.

## GET /occupancy/monthly

Returns one point per day in the selected month.

## GET /analytics/dashboard

Response includes total seats, occupied seats, available seats, occupancy percentage, camera status, daily/weekly/monthly charts, peak usage hours, most used seats, and least used seats.
