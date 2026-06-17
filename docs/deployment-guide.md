# Production Deployment Guide

## 1. Prepare secrets

Create strong values:

```bash
openssl rand -hex 32
```

Use the generated value for `JWT_SECRET_KEY`. Use a different strong password for PostgreSQL.

## 2. Configure HTTPS

Place certificates in:

```text
infra/nginx/certs/fullchain.pem
infra/nginx/certs/privkey.pem
```

Uncomment the HTTPS server block in `infra/nginx/conf.d/default.conf` and set `server_name`.

## 3. Start services

```bash
docker compose -f infra/docker-compose.yml up -d --build
```

## 4. Verify

```bash
docker compose -f infra/docker-compose.yml ps
curl http://localhost:8080/api/health
```

## 5. Backups

Back up PostgreSQL daily:

```bash
docker exec infra-postgres-1 pg_dump -U smartseat smartseat > smartseat-backup.sql
```

## 6. Privacy checklist

- Inform employees that occupancy analytics are being collected.
- Do not store video unless legal approval exists.
- Restrict dashboard access by role.
- Put Raspberry Pis and backend on a trusted network or VPN.
- Rotate JWT and database secrets when staff changes require it.
