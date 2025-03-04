import os
import time
import json
from azure.iot.device import IoTHubDeviceClient, X509
from dotenv import load_dotenv
from get_sensor_data import get_sensor_data

load_dotenv()


HOSTNAME = os.getenv("HOSTNAME")  
DEVICE_ID = os.getenv("DEVICE_ID")                       
CERT_FILE = os.getenv("CERT_FILE")
KEY_FILE = os.getenv("KEY_FILE")
PASS_PHRASE = os.getenv("PASS_PHRASE")                         


x509 = X509(
    cert_file=CERT_FILE,
    key_file=KEY_FILE,
    pass_phrase=PASS_PHRASE
)


device_client = IoTHubDeviceClient.create_from_x509_certificate(
    hostname=HOSTNAME,
    device_id=DEVICE_ID,
    x509=x509
)

try:
    print("Connect to IoT Hub")
    device_client.connect()
    print("Connected")

    while True:

        temperature, humidity = get_sensor_data()

        telemetry_data = {
            "temperature": temperature,
            "humidity": humidity
        }
        message = json.dumps(telemetry_data)
        device_client.send_message(message)
        print(f"Sending data: {message}")
        time.sleep(5)

except KeyboardInterrupt:
    print("Stopped")
finally:
    device_client.disconnect()
    print("Disconnected from IoT Hub")
