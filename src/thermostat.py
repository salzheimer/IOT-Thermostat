import sys
sys.path.append('..')
sys.path.append('../drivers')
sys.path.append('../src')

import dht
from machine import Pin, SoftI2C
from drivers.pico_i2c_lcd import I2cLcd
from utime import sleep
from src import data_send

    
sensor = dht.DHT11(Pin(28))  # Assuming the temperature sensor is connected to GPIO 28
# I2C configuration for the LCD
I2C_ADDR = 0x27  # Change this to your LCD's I2
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = SoftI2C(scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

def read_temperature_sensor():
    """get temperature and humidity from DHT11 sensor"""
    sensor.measure()
    temperature_celcius = sensor.temperature()
    humidity = sensor.humidity()
    temperature_fahrenheit = (temperature_celcius * 9 / 5) + 32
   
    return temperature_fahrenheit, humidity

def main()->None:

    lcd.backlight_on()
    lcd.putstr("Thermostat Ready")
    sleep(5)
    print("Starting temperature sensor readings...")
    lcd.clear()
    while True:
    
        temp, hum = read_temperature_sensor()
        data_send.send_data_to_azure(temp, hum)
        print("Temperature: {:.2f} °F, Humidity: {:.2f}%".format(temp, hum))
        
        lcd.move_to(0, 0)
        lcd.putstr("Temp: {:.2f} F".format(temp))
        lcd.move_to(0, 1)
        lcd.putstr("Humidity: {:.2f}%".format(hum))   
        sleep(15)



if __name__ == "__main__":
    main()