import sys
sys.path.append('..')
sys.path.append('../utils')

import src.thermostat as thermostat
import time
import ntptime
from utils import config_reader
from utils import wifi_connect as wifi


def synchronize_time() -> None:
    config = config_reader.load_config()    
    ssid = config.get('SSID', 'DefaultSSID')
    password = config.get('Password', 'DefaultPW')
    wifi.IS_CONNECTED = wifi.connect_to_wifi(ssid, password)
    
    print("WiFi connection status:", wifi.IS_CONNECTED)
    if wifi.IS_CONNECTED:
        """Synchronize system time with NTP server."""
        try:
            ntptime.settime()
            print("System time synchronized with NTP server.")
            print("Current time:", time.localtime())
        except Exception as e:
            print("Failed to synchronize time:", e)


def main() -> None:
    synchronize_time()

#=== Start the thermostat and display  application ===#
    thermostat.main()



if __name__ == "__main__":
    main()

