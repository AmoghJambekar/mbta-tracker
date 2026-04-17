from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
import utime

# I2C setup - SDA on GP0, SCL on GP1
I2C_ADDR = 0x27
I2C_BUS = 0
SDA_PIN = 0
SCL_PIN = 1
LCD_ROWS = 2
LCD_COLS = 16

def init_lcd():
    i2c = I2C(I2C_BUS, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
    
    # Scan for LCD and print address (useful for debugging)
    devices = i2c.scan()
    print("I2C devices found:", [hex(d) for d in devices])
    
    if not devices:
        print("No I2C device found - check wiring!")
        return None
    
    # Use first found device in case address isn't 0x27
    addr = devices[0]
    lcd = I2cLcd(i2c, addr, LCD_ROWS, LCD_COLS)
    return lcd

def display_test(lcd):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("E:  5m  11m  18m")
    lcd.move_to(0, 1)
    lcd.putstr("39: 3m   9m  --m")

# Main
lcd = init_lcd()

if lcd:
    display_test(lcd)
    print("LCD initialized successfully")
else:
    print("LCD failed to initialize")