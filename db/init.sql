CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    voltage NUMERIC(5, 2),
    current NUMERIC(5, 2),
    power NUMERIC(6, 2),
    temperature NUMERIC(5, 2),
    device_status_modbus INTEGER
);