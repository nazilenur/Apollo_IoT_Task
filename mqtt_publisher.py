import time
import json
import csv  
import os
from dotenv import load_dotenv
from pymodbus.client import ModbusTcpClient
import paho.mqtt.client as mqtt


load_dotenv() 

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Ayarlar
MODBUS_IP = "modbus_server" 
MODBUS_PORT = 5020
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "nazile/iot_task/data"


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
mqttc.loop_start()


modbus_client = ModbusTcpClient(MODBUS_IP, port=MODBUS_PORT)

print(" Starting MQTT Publisher")

try:
    
    with open('data/dataset.csv', 'r') as file:
        reader = csv.DictReader(file)
        
        
        for row in reader: 
            
            
            modbus_client.connect()
            result = modbus_client.read_holding_registers(address=0,count=1)
            
        
            if not result.isError():
                device_status = result.registers[0]
            else:
                device_status = 0
                
            modbus_client.close()
            
            
            payload = {
                "timestamp": row["timestamp"],            
                "voltage": float(row["voltage"]),         
                "current": float(row["current"]),         
                "power": float(row["power"]),             
                "temperature": float(row["temperature"]), 
                "device_status_modbus": device_status     
            }
            
            
            mqttc.publish(MQTT_TOPIC, json.dumps(payload))
            print(f" Sent : Voltage={payload['voltage']}V, Temperature={payload['temperature']}C")
            
            
            time.sleep(2) 

except FileNotFoundError:
    print("Error: Dataset file not found! Please ensure 'data/dataset.csv' exists.")
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    modbus_client.close()
    mqttc.loop_stop()
    mqttc.disconnect()