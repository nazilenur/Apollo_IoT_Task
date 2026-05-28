# Apollo IoT Task

A real-time IoT data pipeline that simulates an industrial energy meter. 
Sensor readings are transmitted using MQTT and Modbus, then stored in a PostgreSQL database.

---

## How It Works

A publisher reads energy data from a CSV file row by row and sends each reading 
to an MQTT broker — just like a real IoT device would stream live sensor data. 
A subscriber listens to that stream and saves every incoming message into a 
PostgreSQL database. At the same time, a Modbus server runs in the background 
simulating a physical device register, which the publisher reads and attaches 
to each message.
```
dataset.csv
|
mqtt_publisher.py  -->  MQTT Broker  -->  mqtt_subscriber.py
|                                         |
modbus_server.py                          PostgreSQL Database
(device status)                           (sensor_data table)
```
---

## Tech Stack
```
| Tool | Purpose |
|------|---------|
| Python | Core language |
| MQTT (paho-mqtt) | Streaming sensor data |
| Modbus (pymodbus) | Industrial device simulation |
| PostgreSQL | Persistent data storage |
| Docker & Docker Compose | Running all services together |
```
---

## Why These Protocols?

**MQTT** — Lightweight and built for sensor data. The publish/subscribe model 
means the publisher doesn't need to know who's listening, which makes it 
ideal for IoT streaming.

**Modbus/TCP** — The most widely used protocol in industrial environments 
(energy meters, PLCs, SCADA systems). Used here to simulate reading a 
device status register alongside live sensor data.

---

## Database Schema

```sql
CREATE TABLE sensor_data (
    id                    SERIAL PRIMARY KEY,
    timestamp             TIMESTAMP,
    voltage               NUMERIC,
    current               NUMERIC,
    power                 NUMERIC,
    temperature           NUMERIC,
    device_status_modbus  INTEGER
);
```

---

## Getting Started

**Requirements:** Docker, Docker Compose

```bash
git clone https://github.com/nazilenur/Apollo_IoT_Task.git
cd Apollo_IoT_Task

docker-compose up --build
```

All four services start automatically — database, Modbus server, publisher, and subscriber.

To verify data is being saved:

```bash
docker exec -it apollo_postgres psql -U apollo_admin -d apollo_task \
  -c "SELECT * FROM sensor_data LIMIT 5;"
```

---

## Project Structure
```
Apollo_IoT_Task/
├── mqtt_publisher.py     # Reads CSV, sends data via MQTT, reads Modbus status
├── mqtt_subscriber.py    # Listens to MQTT, saves readings to PostgreSQL
├── modbus_server.py      # Simulates an industrial device register
├── docker-compose.yml    # Orchestrates all services
├── Dockerfile            # Python environment setup
├── requirements.txt      # Dependencies
├── data/
│   └── dataset.csv       # Sample energy meter dataset
└── db/
└── init.sql          # Creates the sensor_data table
```




