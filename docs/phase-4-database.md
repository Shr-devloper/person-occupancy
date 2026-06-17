# Phase 4: Database Integration

## Goal

Create PostgreSQL tables for users, cameras, seats, occupancy logs, notifications, and mobile device tokens.

## Folder structure

```text
database/schema.sql
database/er-diagram.md
backend/alembic/versions/0001_initial_schema.py
```

## Commands

```bash
docker compose -f infra/docker-compose.yml up -d postgres
cd backend
alembic upgrade head
psql postgresql://smartseat:smartseat@localhost:5432/smartseat -f ../database/schema.sql # only for manual SQL setup on an empty DB
```

## Configuration files

Use Alembic in application deployments. Use `database/schema.sql` for review, documentation, or manual provisioning.

## Testing instructions

Run `psql` and list tables with `\dt`. Insert sample camera and seat through the API instead of direct SQL.

## Expected output

Tables and indexes exist, and foreign keys cascade seat data when cameras are removed.

## Common errors and fixes

| Error | Cause | Fix |
| --- | --- | --- |
| Command not found | Tool is not installed or virtual environment is inactive | Re-run the install commands and activate the environment |
| Connection refused | Backend, database, or camera source is not running | Start the dependent service and check host/port values |
| Permission denied | Linux user cannot access camera, service, or Docker socket | Add the user to the correct group or run the setup command with sudo |
