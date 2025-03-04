import os
import logging
from azure.iot.device import ProvisioningDeviceClient, exceptions, X509
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

load_dotenv()


PROVISIONING_HOST = os.getenv("PROVISIONING_HOST")
ID_SCOPE = os.getenv("ID_SCOPE")
REGISTRATION_ID = os.getenv("REGISTRATION_ID")
CERT_FILE = os.getenv("CERT_FILE")
KEY_FILE = os.getenv("KEY_FILE")


print("Creating X509 object")
x509_obj = X509(
    cert_file=CERT_FILE,
    key_file=KEY_FILE,
    pass_phrase='1234'
)

print("Creating client with X509 object")
provisioning_client = ProvisioningDeviceClient.create_from_x509_certificate(
    provisioning_host=PROVISIONING_HOST,
    registration_id=REGISTRATION_ID,
    id_scope=ID_SCOPE,
    x509=x509_obj
)

print("Started device register")
try:
    registration_result = provisioning_client.register()
    print("Registration Status:", registration_result.status)
    if registration_result.status == "assigned":
        print("IoT Hub:", registration_result.registration_state.assigned_hub)
        print("Device ID:", registration_result.registration_state.device_id)
    else:
        print("Failed to register device. Status:", registration_result.status)
except exceptions.ConnectionFailedError as e:
    print("Connection failed:", e)
except Exception as e:
    print("Unexpected error:", e)
