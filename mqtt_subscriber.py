import sys
print("SUBSCRIBER STARTING...", flush=True)
import paho.mqtt.client as mqtt
import json
import psycopg2

DB_HOST = "apollo_postgres"
DB_PORT = "5432"
DB_NAME = "apollo_task"
DB_USER = "apollo_admin"
DB_PASS = "apollo_iot_pass"

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "nazile/iot_task/data"

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected to broker. Subscribing to {MQTT_TOPIC}...")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}")
   
    payload = json.loads(msg.payload.decode())
    print(f"Data received, Voltage:{payload['voltage']}V, Current:{payload['current']}A, Power:{payload['power']}W, Temperature:{payload['temperature']}C, Status:{payload['device_status_modbus']}")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        
        insert_query = """
            INSERT INTO sensor_data (timestamp, voltage, current, power, temperature, device_status_modbus)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        datas = (
            payload['timestamp'], 
            payload['voltage'], 
            payload['current'], 
            payload['power'], 
            payload['temperature'], 
            payload['device_status_modbus']
        )
        
        cursor.execute(insert_query, datas)
        conn.commit() 
        
        cursor.close()
        conn.close()
        print("Saved to database successfully!")
        
    except Exception as e:
        print(f"Error saving to database: {e}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("Subscriber is waiting for data...")
client.loop_forever()