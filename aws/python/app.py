import time
import json
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from get_sensor_data import get_sensor_data
import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("ENDPOINT")  
CLIENT_ID = os.getenv("CLIENT_ID") #device id in cert (common name)

PATH_TO_CERT = os.getenv("PATH_TO_CERT")
PATH_TO_KEY = os.getenv("PATH_TO_KEY")
PATH_TO_ROOT_CA = os.getenv("PATH_TO_ROOT_CA")

TOPIC = os.getenv("TOPIC")  

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    ca_filepath=PATH_TO_ROOT_CA,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30
)

print("Connecting with AWS IoT")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected")

try:
    while True:
        temperature, humidity = get_sensor_data()
        telemetry_data = {
            "temperature": temperature,
            "humidity": humidity
        }
        message = json.dumps(telemetry_data)
        mqtt_connection.publish(
            topic=TOPIC,
            payload=message,
            qos=mqtt.QoS.AT_LEAST_ONCE
        )
        print(f"Data: {message}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopped")
finally:
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconencted")

