#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# GPIO to LCD mapping (BCM)
LCD_RS = 17
LCD_E  = 27
LCD_D4 = 22
LCD_D5 = 23
LCD_D6 = 24
LCD_D7 = 25

# LCD constants
LCD_WIDTH = 16    # characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for 2nd line

E_PULSE = 0.0005
E_DELAY = 0.0005

def lcd_init():
    lcd_byte(0x33, LCD_CMD)  # Initialize
    lcd_byte(0x32, LCD_CMD)  # Set to 4-bit mode
    lcd_byte(0x06, LCD_CMD)  # Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # Display On, Cursor Off
    lcd_byte(0x28, LCD_CMD)  # 4-bit, 2 line
    lcd_byte(0x01, LCD_CMD)  # Clear display
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode)
    # High nibble
    GPIO.output(LCD_D4, bool(bits & 0x10))
    GPIO.output(LCD_D5, bool(bits & 0x20))
    GPIO.output(LCD_D6, bool(bits & 0x40))
    GPIO.output(LCD_D7, bool(bits & 0x80))
    lcd_toggle_enable()
    # Low nibble
    GPIO.output(LCD_D4, bool(bits & 0x01))
    GPIO.output(LCD_D5, bool(bits & 0x02))
    GPIO.output(LCD_D6, bool(bits & 0x04))
    GPIO.output(LCD_D7, bool(bits & 0x08))
    lcd_toggle_enable()

def lcd_toggle_enable():
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for char in message:
        lcd_byte(ord(char), LCD_CHR)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Setup GPIO
    for pin in [LCD_E, LCD_RS, LCD_D4, LCD_D5, LCD_D6, LCD_D7]:
        GPIO.setup(pin, GPIO.OUT)
    lcd_init()

    try:
        while True:
            lcd_string("Hello Raspberry Pi", LCD_LINE_1)
            lcd_string("1602A LCD Demo", LCD_LINE_2)
            time.sleep(3)
            lcd_string("RPi GPIO Python", LCD_LINE_1)
            lcd_string("Working!", LCD_LINE_2)
            time.sleep(3)

    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)  # Clear
        GPIO.cleanup()

if __name__ == "__main__":
    main()
