import sys
import time
import ntptime
import src.thermostat as thermostat
import src.display as display
import src.data_send as data_send

from utils import config_reader
from utils import wifi_connect as wifi

sys.path.append('..')
sys.path.append('../utils')




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
    display.initialize_lcd()

    #data_send.configure_azure_sas()
    data_send.intialize_azure_x509()
    client = data_send.intialize_azure_x509()
    while True:
        temp, hum = thermostat.read_temperature_sensor()
        print("WiFi connection status inside main loop:", wifi.IS_CONNECTED)
        if wifi.IS_CONNECTED:
    #        data_send.send_data_to_azure_sas(temp, hum)
            data_send.send_data_to_azure_x509(client, temp, hum)
        print("Temperature: {:.2f} °F, Humidity: {:.2f}%".format(temp, hum))
        
        display.update_lcd(temp, hum)   
        time.sleep(15)



if __name__ == "__main__":
    main()

