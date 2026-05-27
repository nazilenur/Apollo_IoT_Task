import time
import json
import csv  # <-- CSV'yi okumak için bunu ekledik
import os
from dotenv import load_dotenv
from pymodbus.client import ModbusTcpClient
import paho.mqtt.client as mqtt


load_dotenv() 

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Ayarlar
MODBUS_IP = "modbus_server"  # Modbus sunucusunun IP'si (Docker'da servis adıyla erişim)
MODBUS_PORT = 5020
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "nazile/iot_task/data"

# MQTT kurulumu
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
mqttc.loop_start()

# Modbus istemcisi (adını modbus_client yaptık ki karışmasın)
modbus_client = ModbusTcpClient(MODBUS_IP, port=MODBUS_PORT)

print(" Starting MQTT Publisher")

try:
    # 1. Dosyayı aç
    with open('data/dataset.csv', 'r') as file:
        reader = csv.DictReader(file)
        
        # 2. Dosyadaki her bir satır için dönmeye başla
        for row in reader: 
            
            # 3. Aynı anda Modbus'tan da durumu (17) oku
            modbus_client.connect()
            result = modbus_client.read_holding_registers(address=0,count=1)
            
            # Eğer Modbus'ta sorun yoksa değeri al, varsa 0 kabul et
            if not result.isError():
                device_status = result.registers[0]
            else:
                device_status = 0
                
            modbus_client.close()
            
            # 4. Kargo paketini (Payload) hazırla
            payload = {
                "timestamp": row["timestamp"],            
                "voltage": float(row["voltage"]),         
                "current": float(row["current"]),         
                "power": float(row["power"]),             
                "temperature": float(row["temperature"]), 
                "device_status_modbus": device_status     
            }
            
            # 5. MQTT'ye gönder
            mqttc.publish(MQTT_TOPIC, json.dumps(payload))
            print(f" Sent : Voltage={payload['voltage']}V, Temperature={payload['temperature']}C")
            
            # Diğer satıra geçmeden 2 saniye bekle
            time.sleep(2) 

except FileNotFoundError:
    print("Error: Dataset file not found! Please ensure 'data/dataset.csv' exists.")
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    modbus_client.close()
    mqttc.loop_stop()
    mqttc.disconnect()