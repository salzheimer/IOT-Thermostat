# --- Import the required libraries:
import binascii
import network
import rp2


def main()->None:
    # --- Set the country to avoid possible issues ---
    rp2.country('US')

    # --- Create a WLAN object ---
    wlan = network.WLAN(network.STA_IF)

    # --- Activate the interface ---
    wlan.active(True)

    # --- Scan for available access points ---
    networks = wlan.scan()

    # --- Print the list of available networks ---
    print("Available WiFi Networks:")
    for ssid, bssid, channel, rssi, authmode, hidden in networks:
        print(f"SSID: {ssid.decode('utf-8')}, BSSID: {binascii.hexlify(bssid).decode('utf-8')}, "
              f"Channel: {channel}, RSSI: {rssi}, AuthMode: {authmode}, Hidden: {hidden}")






if __name__ == "__main__":
    main()