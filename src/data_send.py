import os
import sys
sys.path.append('..')
sys.path.append('../utils')

from utils import config_reader
import time
import urequests
import umqtt.simple as mqtt
import ssl
import json

config = config_reader.load_config()
IOT_HUB_HOSTNAME = config.get('IOT_HUB_HOSTNAME', 'your-iot-hub.azure-devices.net')
DEVICE_ID = config.get('DEVICE_ID', 'your-device-id')


def get_IsoTimestamp():

    """Get the current time in ISO 8601 format."""
    t=time.localtime()
    return "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(t[0], t[1], t[2], t[3], t[4], t[5])

def configure_azure_sas() -> None:


    """Configure Azure IoT Hub connection using SAS token."""
    global URL, HEADERS

        # Azure IoT Hub connection settings

    SAS_TOKEN = config.get('SAS_TOKEN', 'your-sas-token')

    print("Azure IoT Hub Hostname:", IOT_HUB_HOSTNAME)
    print("Device ID:", DEVICE_ID)
    print("SAS Token:", SAS_TOKEN)

    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'SharedAccessSignature {SAS_TOKEN}'
    }

    URL=f"https://{IOT_HUB_HOSTNAME}.azure-devices.net/devices/{DEVICE_ID}/messages/events?api-version=2020-09-30"

def send_data_to_azure_sas(temperature: float, humidity: float) -> None:




    print("Preparing to send data to Azure IoT Hub using SAS token...")
    payload = {
        "deviceId": DEVICE_ID,
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": get_IsoTimestamp()
    }
    print("Azure IoT Hub URL:", URL)
    print("Azure IoT Hub Headers:", HEADERS)
    print("Prepared payload for Azure IoT Hub:", payload)
    # Here you would add the code to send the HTTP request to Azure IoT Hub
    # For example, using the 'urequests' library on MicroPython:
    try:
        response = urequests.post(URL, json=payload, headers=HEADERS)
        print("Response from Azure IoT Hub:", response.text)
        response.close()

    except Exception as e:
        print("Failed to send data to Azure IoT Hub:", e)


##
#
# Data sending with X509 certificate is not implemented in this example.
#
# ##
def load_certificates(file_path: str):
    """Load X.509 certificate from a file."""
    print("Root contents:", os.listdir('/'))
    try:
        with open(file_path, 'rb') as cert_file:
            certificate = cert_file.read()
        cert_file.close()
        return certificate
    except Exception as e:
        print("Failed to load certificate from", file_path, ":", e)
        return ""

def intialize_azure_x509() -> None:
    """Placeholder function for initializing Azure IoT Hub connection using X.509 certificates."""
    print("X.509 certificate-based authentication is implemented in this example.")
    # MQTT configuration
    MQTT_BROKER = f"{IOT_HUB_HOSTNAME}.azure-devices.net"
    MQTT_PORT = 8883
    MQTT_CLIENT_ID = DEVICE_ID
    MQTT_USERNAME = f"{MQTT_BROKER}/{DEVICE_ID}/?api-version=2021-04-12"
    MQTT_PASSWORD = "" # Empty for x509 authentication

    print("MQTT Broker:", MQTT_BROKER)
    print("MQTT Client ID:", MQTT_CLIENT_ID)
    print("MQTT Username:", MQTT_USERNAME)

    try:
        CERT_FILE_PATH = config.get('CERT_FILE_PATH', 'path/to/certificate.pem')
        certificate = load_certificates(CERT_FILE_PATH)
        print("Loaded X.509 certificate from:", CERT_FILE_PATH)
        print("Certificate contents:", certificate)
        KEY_FILE_PATH = config.get('KEY_FILE_PATH', 'path/to/private_key.pem')
        private_key = load_certificates(KEY_FILE_PATH)
        print("Loaded private key from:", KEY_FILE_PATH)
        print("Private key contents:", private_key)

        CA_FILE_PATH = config.get('CA_FILE_PATH', 'path/to/ca_certificate.pem')
        ca_certificate = load_certificates(CA_FILE_PATH)
        print("Loaded CA certificate from:", CA_FILE_PATH)
        print("CA Certificate contents:", ca_certificate)

       

        print("Connecting to Azure IOT Hub..")
        client= mqtt.MQTTClient(
            client_id=MQTT_CLIENT_ID,
            server=MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USERNAME,
            password=MQTT_PASSWORD,
            ssl=True,
            ssl_params={
                "cert": certificate,
                "key": private_key,
                "server_hostname": MQTT_BROKER,
               
            }
        )
        client.connect()
        print("Connected to Azure IoT Hub using X.509 certificates.")
        return client
    except Exception as e:
        print("Failed to connect to Azure IoT Hub", e )
        sys.print_exception(e)
        return None



def send_data_to_azure_x509(client,temperature: float, humidity: float) -> None:
    """Placeholder function for sending data to Azure IoT Hub using X.509 certificates."""
    print("X.509 certificate-based authentication is implemented in this example.")
    payload = {
        "deviceId": DEVICE_ID,
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": get_IsoTimestamp()
    }
    json_payload = json.dumps(payload)
    print("Prepared payload for Azure IoT Hub:", json_payload)
    topic = f"devices/{DEVICE_ID}/messages/events"
    try:

        client.publish(topic, json_payload.encode('utf-8'))
        print("Data sent to Azure IoT Hub using X.509 certificates.")
    except Exception as e:
        print("Failed to send data to Azure IoT Hub:", e)