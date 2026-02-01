# Raspberry Pi Pico Thermostat

A MicroPython-based thermostat application for Raspberry Pi Pico that monitors temperature and humidity using a DHT11 sensor, displays readings on an I2C LCD screen, and sends data to Azure IoT Hub for cloud monitoring.

## Quick Start

1. Flash MicroPython v1.20.0+ to Raspberry Pi Pico W
2. Copy project files to Pico: `main.py`, `src/`, `drivers/`, `utils/`, `config.txt`
3. Configure WiFi and Azure credentials in `config.txt`
4. Choose authentication: `USE_SAS_AUTH=True` (SAS Token) or `False` (X.509)
5. Power on - device will auto-connect and start sending data

**Default Authentication**: SAS Token (simpler setup)
**Production Ready**: X.509 Certificates (more secure)

## Features

- **Temperature & Humidity Monitoring**: Reads environmental data from a DHT11 sensor
- **LCD Display**: Shows real-time temperature (Fahrenheit) and humidity on a 16x2 I2C LCD
- **Cloud Integration**: Sends sensor data to Azure IoT Hub for remote monitoring and analytics
- **Dual Authentication Support**: Choose between SAS Token or X.509 Certificate authentication
  - **SAS Token**: Simple HTTP-based authentication via REST API
  - **X.509 Certificates**: Secure MQTT-based authentication with client certificates
- **WiFi Connectivity**: Connects to WiFi network for cloud communication
- **Time Synchronization**: Syncs system time with NTP servers for accurate timestamps
- **Configuration Management**: Easy setup via configuration file
- **Modular Architecture**: Separated concerns for sensor reading, display, and data transmission

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

**Built-in Libraries:**
- `dht` - DHT11 sensor driver
- `machine` - Hardware control (Pin, SoftI2C)
- `network` - WiFi connectivity
- `ntptime` - NTP time synchronization
- `ssl` - SSL/TLS support for secure connections
- `json` - JSON encoding/decoding
- `time`/`utime` - Time functions

**Network Libraries:**
- `urequests` - HTTP requests for SAS Token authentication
- `umqtt.simple` - MQTT client for X.509 Certificate authentication

**Custom Modules Included:**
- `drivers/pico_i2c_lcd.py` - I2C LCD driver
- `drivers/lcd_api.py` - LCD API interface
- `src/thermostat.py` - Sensor reading module
- `src/display.py` - LCD display management
- `src/data_send.py` - Azure IoT Hub communication (dual authentication)
- `utils/config_reader.py` - Configuration parser
- `utils/wifi_connect.py` - WiFi management

## Installation

1. **Flash MicroPython** to your Raspberry Pi Pico W (v1.20.0 or later required for SSL/TLS support)
2. **Clone or download** this repository
3. **Copy all required directories and files** to your Pico:
   - `main.py` (application entry point at root)
   - `src/` directory (all application modules)
   - `drivers/` directory (LCD drivers)
   - `utils/` directory (configuration and WiFi utilities)
   - `config.txt` (your configuration file)
   - `lib/` directory (for external libraries like umqtt)
   - `certs/` directory (only if using X.509 Certificate authentication)

4. **Install MQTT library** (only needed for X.509 Certificate authentication):
   ```python
   import upip
   upip.install('micropython-umqtt.simple')
   ```
   Or manually copy umqtt library to the `lib/` directory

5. **Configure your settings**:
   - Copy `config.example.txt` to `config.txt`
   - Edit `config.txt` with your WiFi and Azure credentials (see Configuration section)
   - Choose your authentication method (`USE_SAS_AUTH`)

## Configuration

Create or edit `config.txt` with your settings. The project supports two authentication methods:

### Option 1: SAS Token Authentication (Default)

```
# WiFi Configuration
SSID=YourWiFiNetwork
Password=YourWiFiPassword

# Azure IoT Hub Configuration
IOT_HUB_HOSTNAME=your-iot-hub
DEVICE_ID=your-device-id

# Use SAS Token Authentication
USE_SAS_AUTH=True
SAS_TOKEN=your-sas-token
```

### Option 2: X.509 Certificate Authentication

```
# WiFi Configuration
SSID=YourWiFiNetwork
Password=YourWiFiPassword

# Azure IoT Hub Configuration
IOT_HUB_HOSTNAME=your-iot-hub
DEVICE_ID=your-device-id

# Use X.509 Certificate Authentication
USE_SAS_AUTH=False
CERT_FILE_PATH=certs/your-device.crt.der
KEY_FILE_PATH=certs/your-device.key.der
```

**Security Notes**:
- The `config.txt` file contains sensitive credentials
- Add `config.txt` to `.gitignore` (already included)
- Never commit actual credentials to version control
- For X.509, also add `certs/` directory to `.gitignore`

## Azure IoT Hub Setup

### Common Setup Steps

1. Create an Azure IoT Hub in the Azure Portal
2. Register a new device in your IoT Hub

### Authentication Method Setup

#### SAS Token Authentication

1. In Azure Portal, navigate to your device
2. Generate a SAS token (or use Azure IoT Explorer):
   ```bash
   az iot hub generate-sas-token --hub-name {your-hub} --device-id {your-device}
   ```
3. Update `config.txt` with:
   - IoT Hub hostname (e.g., `my-hub`)
   - Device ID
   - SAS token
   - Set `USE_SAS_AUTH=True`

**Pros**: Simple, no certificates needed
**Cons**: Tokens expire and need renewal

#### X.509 Certificate Authentication

1. Generate a device certificate and private key:
   ```bash
   # Self-signed certificate example
   openssl req -newkey rsa:2048 -nodes -keyout device.key -x509 -days 365 -out device.crt
   ```

2. Convert to DER format (recommended for MicroPython):
   ```bash
   openssl x509 -in device.crt -outform DER -out device.crt.der
   openssl rsa -in device.key -outform DER -out device.key.der
   ```

3. Upload certificate thumbprint to Azure IoT Hub:
   - Get thumbprint: `openssl x509 -in device.crt -fingerprint -noout`
   - In Azure Portal, set device authentication to "X.509 Self-Signed"
   - Add thumbprint(s)

4. Copy certificate files to `certs/` directory on Pico

5. Update `config.txt` with:
   - IoT Hub hostname
   - Device ID
   - Set `USE_SAS_AUTH=False`
   - Certificate paths

**Pros**: More secure, no token expiration
**Cons**: Certificate management required

## Usage

### Running the Application

The application starts automatically when the Pico is powered on. The entry point is `main.py` at the root:

```python
python main.py
```

MicroPython on Pico will automatically run `main.py` on boot if it exists at the root directory.

### Workflow

1. **Initialization**:
   - Connects to WiFi and synchronizes time with NTP
   - Initializes LCD display
   - Configures Azure IoT Hub connection based on `USE_SAS_AUTH` setting
     - If `USE_SAS_AUTH=True`: Configures HTTP client with SAS token
     - If `USE_SAS_AUTH=False`: Establishes MQTT connection with X.509 certificates

2. **Display Ready**: LCD shows "Thermostat Ready" for 5 seconds

3. **Monitoring Loop**: Every 15 seconds:
   - Reads temperature and humidity from DHT11 sensor
   - Updates LCD display with current readings
   - Sends data to Azure IoT Hub (via HTTP or MQTT based on auth method)
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
├── main.py              # Entry point, WiFi/NTP setup, main loop
├── config.txt           # Configuration file (not tracked in git)
├── config.example.txt   # Configuration template
├── requirements.txt     # Project dependencies
├── README.md            # This file
├── .gitignore          # Git ignore rules
│
├── src/                 # Application source code
│   ├── thermostat.py   # Sensor reading (DHT11)
│   ├── display.py      # LCD display management
│   └── data_send.py    # Azure IoT Hub dual authentication
│
├── drivers/             # Hardware drivers
│   ├── lcd_api.py      # LCD API abstraction layer
│   └── pico_i2c_lcd.py # I2C LCD driver implementation
│
├── utils/               # Utility modules
│   ├── config_reader.py # Configuration file parser
│   └── wifi_connect.py  # WiFi connection management
│
├── certs/               # X.509 certificates (not tracked in git)
│   ├── *.crt           # Device certificate (PEM format)
│   ├── *.crt.der       # Device certificate (DER format)
│   ├── *.key           # Private key (PEM format)
│   └── *.key.der       # Private key (DER format)
│
├── lib/                 # External libraries
│   └── umqtt/          # MQTT library (for X.509 auth)
│
├── tools/               # Development and testing tools
│   ├── blink.py        # LED blink test utility
│   └── wifi_scan.py    # WiFi network scanner
│
├── tests/               # Test files
│   ├── README.md       # Testing documentation
│   └── test_config_reader.py # Unit tests for config reader
│
└── docs/                # Additional documentation
    └── MIGRATION_GUIDE.md # Migration guide for restructure
```

## Module Descriptions

### [main.py](main.py)
Application entry point that handles:
- WiFi connection and NTP time synchronization
- Authentication method selection (SAS or X.509)
- Main monitoring loop coordinating sensor reading, display updates, and cloud communication
- Runs automatically on Pico boot

### [src/thermostat.py](src/thermostat.py)
Sensor reading module that:
- Interfaces with DHT11 sensor on GPIO 28
- Reads temperature (converted to Fahrenheit) and humidity
- Returns sensor data to main loop

### [src/display.py](src/display.py)
LCD display management module that:
- Initializes the 16x2 I2C LCD
- Updates display with temperature and humidity readings
- Shows "Thermostat Ready" message on startup

### [src/data_send.py](src/data_send.py)
Azure IoT Hub communication module with dual authentication support:
- **SAS Token mode**: HTTP REST API calls via `urequests`
- **X.509 mode**: MQTT over TLS via `umqtt.simple`
- Certificate loading for X.509 authentication
- Payload formatting with ISO 8601 timestamps
- Error handling and connection management

### [utils/wifi_connect.py](utils/wifi_connect.py)
WiFi connection handler with:
- Automatic connection with retry logic
- Connection status management
- Country-specific WiFi configuration

### [utils/config_reader.py](utils/config_reader.py)
Configuration file parser that:
- Reads and parses `config.txt` key-value pairs
- Handles comments and malformed lines
- Provides default values for missing settings

### [drivers/pico_i2c_lcd.py](drivers/pico_i2c_lcd.py)
I2C LCD driver for HD44780-compatible displays via PCF8574 I2C expander. Forked from [RPI-PICO-I2C-LCD](https://github.com/T-622/RPI-PICO-I2C-LCD/).

### [drivers/lcd_api.py](drivers/lcd_api.py)
Abstract LCD API providing a common interface for LCD operations (cursor movement, character writing, backlight control).

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

**For SAS Token Authentication:**
- Verify IoT Hub hostname, device ID, and SAS token in `config.txt`
- Check SAS token expiration date
- Ensure device is registered in IoT Hub
- Verify token format is correct
- Check HTTP response codes in console output

**For X.509 Certificate Authentication:**
- Verify certificate files exist in `certs/` directory
- Check certificate file paths in `config.txt`
- Ensure certificate thumbprint is registered in Azure IoT Hub
- Verify device authentication type is set to "X.509" in Azure Portal
- Check certificate hasn't expired
- Confirm DER format certificates are being used (PEM works but DER is smaller)
- Verify MQTT broker hostname matches IoT Hub hostname
- Check console for SSL/TLS errors
- Ensure MicroPython version supports SSL (v1.20.0+)

## Authentication Method Comparison

| Feature | SAS Token | X.509 Certificate |
|---------|-----------|-------------------|
| **Protocol** | HTTP/HTTPS | MQTT over TLS |
| **Security** | Token-based | Certificate-based |
| **Setup Complexity** | Simple | Moderate |
| **Token/Cert Expiration** | Yes (requires renewal) | Yes (but typically longer) |
| **Network Overhead** | Higher (HTTP) | Lower (MQTT) |
| **Library Requirements** | urequests | umqtt.simple |
| **Best For** | Quick prototyping | Production deployments |
| **Azure Portal Config** | Generate SAS token | Upload certificate thumbprint |

**Recommendation**: Use SAS Token for initial development and testing. Switch to X.509 certificates for production deployments requiring enhanced security.

## Future Enhancements

Potential improvements for this project:
- Add thermostat control with relay for HVAC systems
- Implement temperature threshold alerts
- Add web interface for configuration
- Support for multiple sensors
- Local data logging to SD card
- Battery backup with low-power sleep modes
- Certificate auto-renewal for X.509
- Cloud-to-device messaging support
- Device twin properties integration

## License

This project is provided as-is for educational and personal use.

## Contributing

Contributions are welcome. Please submit pull requests or open issues for bugs and feature requests.
