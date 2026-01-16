import dht
import sys
from machine import Pin

from utime import sleep





    
sensor = dht.DHT11(Pin(28))  # Assuming the temperature sensor is connected to GPIO 28


def read_temperature_sensor():
    """get temperature and humidity from DHT11 sensor"""
    sensor.measure()
    temperature_celcius = sensor.temperature()
    humidity = sensor.humidity()
    temperature_fahrenheit = (temperature_celcius * 9 / 5) + 32
   
    return temperature_fahrenheit, humidity



