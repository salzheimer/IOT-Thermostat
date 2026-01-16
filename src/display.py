import sys
from drivers.pico_i2c_lcd import I2cLcd
from machine import Pin, SoftI2C
from utime import sleep
sys.path.append('../drivers')

# I2C configuration for the LCD
I2C_ADDR = 0x27  # Change this to your LCD's I2
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = SoftI2C(scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)


def initialize_lcd() -> None:
    """Initialize the LCD display."""
    lcd.backlight_on()
    lcd.putstr("Thermostat Ready")
    sleep(5)
    print("Starting temperature sensor readings...")
    lcd.clear()

def update_lcd(temperature: float, humidity: float) -> None:
    """Update the LCD display with temperature and humidity."""
    lcd.move_to(0, 0)
    lcd.putstr("Temp: {:.2f} F".format(temperature))
    lcd.move_to(0, 1)
    lcd.putstr("Humidity: {:.2f}%".format(humidity))