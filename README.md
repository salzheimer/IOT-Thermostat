# Raspberry Pi Pico Thermostat

A MicroPython-based thermostat application for Raspberry Pi Pico that monitors temperature and humidity using a DHT11 sensor, displays readings on an I2C LCD screen, and sends data to Azure IoT Hub for cloud monitoring.

## Features

- **Temperature & Humidity Monitoring**: Reads environmental data from a DHT11 sensor
- **LCD Display**: Shows real-time temperature (Fahrenheit) and humidity on a 16x2 I2C LCD
- **Cloud Integration**: Sends sensor data to Azure IoT Hub for remote monitoring and analytics
- **WiFi Connectivity**: Connects to WiFi network for cloud communication
- **Time Synchronization**: Syncs system time with NTP servers for accurate timestamps
- **Configuration Management**: Easy setup via configuration file

## Hardware Requirements

- Raspberry Pi Pico W (with WiFi capability)
- DHT11 Temperature & Humidity Sensor
- 16x2 I2C LCD Display (I2C address: 0x27)
- Connecting wires

## Pin Configuration

- **DHT11 Sensor**: GPIO 28
- **I2C LCD**:
  - SDA: GPIO 0
  - SCL: GPIO 1

## Software Dependencies

This project uses MicroPython with the following libraries:
- `dht` - DHT11 sensor driver
- `machine` - Hardware control (Pin, SoftI2C)
- `network` - WiFi connectivity
- `ntptime` - NTP time synchronization
- `urequests` - HTTP requests for Azure IoT Hub

Custom modules included:
- `pico_i2c_lcd.py` - I2C LCD driver
- `lcd_api.py` - LCD API interface

## Installation

1. **Flash MicroPython** to your Raspberry Pi Pico W
2. **Clone or download** this repository
3. **Copy all required directories and files** to your Pico:
   - `src/` directory (all application files)
   - `drivers/` directory (LCD drivers)
   - `utils/` directory (configuration and WiFi utilities)
   - `config.txt` (your configuration file)

4. **Configure your settings**:
   - Copy `config.example.txt` to `config.txt`
   - Edit `config.txt` with your WiFi and Azure credentials (see Configuration section)

## Configuration

Create or edit `config.txt` with your settings:

```
SSID=YourWiFiNetwork
Password=YourWiFiPassword

IOT_HUB_HOSTNAME=your-iot-hub
DEVICE_ID=your-device-id
SAS_TOKEN=your-sas-token
```

**Note**: The `config.txt` file contains sensitive credentials. Make sure to:
- Add `config.txt` to `.gitignore` (already included in this project)
- Never commit your actual credentials to version control

## Azure IoT Hub Setup

1. Create an Azure IoT Hub in the Azure Portal
2. Register a new device in your IoT Hub
3. Generate a SAS token for your device
4. Update the `config.txt` file with:
   - Your IoT Hub hostname
   - Your device ID
   - Your SAS token

## Usage

### Running the Application

The application starts automatically when the Pico is powered on. The entry point is:

```python
python src/main.py
```

### Workflow

1. **Initialization**: Connects to WiFi and synchronizes time with NTP
2. **Display Ready**: LCD shows "Thermostat Ready" for 5 seconds
3. **Monitoring Loop**: Every 15 seconds:
   - Reads temperature and humidity from DHT11 sensor
   - Displays values on LCD screen
   - Sends data to Azure IoT Hub
   - Prints readings to console

### Sample Output

```
Temperature: 72.50 °F, Humidity: 45.00%
```

LCD Display:
```
Temp: 72.50 F
Humidity: 45.00%
```

## Project Structure

```
.
├── src/                 # Application source code
│   ├── main.py         # Entry point, WiFi/NTP setup
│   ├── thermostat.py   # Main thermostat logic and sensor reading
│   └── data_send.py    # Azure IoT Hub data transmission
├── drivers/             # Hardware drivers
│   ├── lcd_api.py      # LCD API abstraction layer
│   └── pico_i2c_lcd.py # I2C LCD driver implementation
├── utils/               # Utility modules
│   ├── config_reader.py # Configuration file parser
│   └── wifi_connect.py  # WiFi connection management
├── tools/               # Development and testing tools
│   ├── blink.py        # LED blink test utility
│   └── wifi_scan.py    # WiFi network scanner
├── tests/               # Test files
│   ├── README.md       # Testing documentation
│   └── test_config_reader.py # Unit tests for config reader
├── docs/                # Additional documentation
├── config.txt           # Configuration file (not tracked in git)
├── config.example.txt   # Configuration template
├── requirements.txt     # Project dependencies
├── .gitignore          # Git ignore rules
└── README.md            # This file
```

## Module Descriptions

### [src/main.py](src/main.py)
Entry point that handles WiFi connection, NTP time synchronization, and starts the thermostat application.

### [src/thermostat.py](src/thermostat.py)
Core thermostat functionality including sensor reading, LCD display updates, and main monitoring loop.

### [src/data_send.py](src/data_send.py)
Manages Azure IoT Hub communication, formats telemetry data with timestamps, and sends HTTP POST requests.

### [utils/wifi_connect.py](utils/wifi_connect.py)
WiFi connection handler with retry logic and connection status management.

### [utils/config_reader.py](utils/config_reader.py)
Reads and parses the `config.txt` file, providing configuration values to other modules.

### [drivers/pico_i2c_lcd.py](drivers/pico_i2c_lcd.py)
I2C LCD driver for HD44780-compatible displays, forked from [RPI-PICO-I2C-LCD](https://github.com/T-622/RPI-PICO-I2C-LCD/).

### [drivers/lcd_api.py](drivers/lcd_api.py)
Abstract LCD API providing a common interface for LCD operations.

## Troubleshooting

### WiFi Connection Issues
- Verify SSID and password in `config.txt`
- Check WiFi signal strength
- Ensure Pico W is in range of the router

### Sensor Reading Errors
- Check DHT11 wiring to GPIO 28
- Verify sensor power supply (3.3V)
- Allow sensor warm-up time after power-on

### LCD Not Displaying
- Verify I2C address (default: 0x27)
- Check SDA/SCL connections (GPIO 0/1)
- Test I2C communication with i2c.scan()

### Azure IoT Hub Connection Failures
- Verify IoT Hub hostname, device ID, and SAS token
- Check SAS token expiration date
- Ensure device is registered in IoT Hub

## Future Enhancements

Potential improvements for this project:
- Add thermostat control with relay for HVAC systems
- Implement temperature threshold alerts
- Add web interface for configuration
- Support for multiple sensors
- Local data logging to SD card
- Battery backup with low-power sleep modes

## License

This project is provided as-is for educational and personal use.

## Contributing

Contributions are welcome. Please submit pull requests or open issues for bugs and feature requests.
