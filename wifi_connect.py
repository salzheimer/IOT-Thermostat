import network
import socket
import rp2
import time
import config_reader 

def connect_to_wifi(ssid: str, password: str, max_retries: int = 5) -> bool:
    """Connect to a WiFi network."""
    rp2.country('US')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"Connecting to network {ssid}...")
        wlan.connect(ssid, password)
        
        retries = 0
        while not wlan.isconnected() and retries < max_retries:
            print("Waiting for connection...")
            time.sleep(2)
            retries += 1
            
    if wlan.isconnected():
        print("Connected to WiFi")
        print("Network config:", wlan.ifconfig())
        return True
    else:
        print("Failed to connect to WiFi")
        return False
    
def main()->None:
    config = config_reader.load_config()
    ssid = config.get('ssid', 'DefaultSSID')
    password = config.get('password', 'DefaultPW')
    connect_to_wifi(ssid, password)

if __name__ == "__main__":
    main()
