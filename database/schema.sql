CREATE TYPE userrole AS ENUM ('admin', 'manager', 'viewer');
CREATE TYPE camerastatus AS ENUM ('online', 'offline', 'maintenance');
CREATE TYPE occupancystate AS ENUM ('occupied', 'empty');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role userrole NOT NULL DEFAULT 'viewer',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE cameras (
    id SERIAL PRIMARY KEY,
    camera_name VARCHAR(120) NOT NULL,
    location VARCHAR(255) NOT NULL,
    ip_address VARCHAR(255),
    stream_url VARCHAR(512),
    status camerastatus NOT NULL DEFAULT 'offline',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE seats (
    id SERIAL PRIMARY KEY,
    seat_name VARCHAR(120) NOT NULL,
    camera_id INTEGER NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
    region_x1 INTEGER NOT NULL DEFAULT 0,
    region_y1 INTEGER NOT NULL DEFAULT 0,
    region_x2 INTEGER NOT NULL DEFAULT 0,
    region_y2 INTEGER NOT NULL DEFAULT 0,
    current_state occupancystate NOT NULL DEFAULT 'empty',
    last_state_change TIMESTAMPTZ
);

CREATE TABLE occupancy_logs (
    id SERIAL PRIMARY KEY,
    seat_id INTEGER NOT NULL REFERENCES seats(id) ON DELETE CASCADE,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ,
    duration INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_occupancy_logs_seat_id ON occupancy_logs(seat_id);
CREATE INDEX idx_occupancy_logs_start_time ON occupancy_logs(start_time);
CREATE INDEX idx_occupancy_logs_end_time ON occupancy_logs(end_time);

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    severity VARCHAR(50) NOT NULL DEFAULT 'info',
    seat_id INTEGER REFERENCES seats(id) ON DELETE SET NULL,
    camera_id INTEGER REFERENCES cameras(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE device_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(512) UNIQUE NOT NULL,
    platform VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
