import sys
sys.path.append('..')
sys.path.append('../utils')

from utils import config_reader
import time
import urequests


config = config_reader.load_config()

# Azure IoT Hub connection settings
IOT_HUB_HOSTNAME = config.get('IOT_HUB_HOSTNAME', 'your-iot-hub.azure-devices.net')
DEVICE_ID = config.get('DEVICE_ID', 'your-device-id')
SAS_TOKEN = config.get('SAS_TOKEN', 'your-sas-token')

print("Azure IoT Hub Hostname:", IOT_HUB_HOSTNAME)
print("Device ID:", DEVICE_ID)
print("SAS Token:", SAS_TOKEN)

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'SharedAccessSignature {SAS_TOKEN}'
}

URL=f"https://{IOT_HUB_HOSTNAME}.azure-devices.net/devices/{DEVICE_ID}/messages/events?api-version=2020-09-30"

def get_IsoTimestamp():
    """Get the current time in ISO 8601 format."""
    t=time.localtime()
    return "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(t[0], t[1], t[2], t[3], t[4], t[5])

def send_data_to_azure(temperature: float, humidity: float) -> None:
    
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