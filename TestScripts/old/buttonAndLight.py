# from adafruit_mcp230xx.mcp23017 import MCP23017
import time
from RPi import GPIO
import board
import busio
import digitalio

# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)  # MCP23017

pin_A0 = mcp.get_pin(0)
# pin_A1 = mcp.get_pin(1)
# pin_A2 = mcp.get_pin(2)
# pin_A3 = mcp.get_pin(3)
# pin_A4 = mcp.get_pin(4)
# pin_A5 = mcp.get_pin(5)
# pin_A6 = mcp.get_pin(6)
# pin_A7 = mcp.get_pin(7)
# pin_B7 = mcp.get_pin(15)

# GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# button1 = board.GPIO1

# button2 = board.GPIO17
# button3 = board.GPI22

# pin_A1.direction = digitalio.Direction.INPUT

pin_A0.pull = digitalio.Pull.UP
# pin_A1.pull = digitalio.Pull.UP
# pin_A2.pull = digitalio.Pull.UP
# pin_A3.pull = digitalio.Pull.UP
# pin_A4.pull = digitalio.Pull.UP
# pin_A5.pull = digitalio.Pull.UP
# pin_A6.pull = digitalio.Pull.UP
# pin_A7.pull = digitalio.Pull.UP
# pin_B7.pull = digitalio.Pull.UP


while True:
    time.sleep(0.1)
    # Read pin 1 and print its state.
    poop_emoji = "\U0001F4A9"
    stop_sign = "\U000026D4"
    button2 = GPIO.input(17)
    # a0 = poop_emoji if button1 else stop_sign
    a1 = poop_emoji if button2 else stop_sign
    # a2 = poop_emoji if button3 else stop_sign
    # a3 = poop_emoji if pin_A3.value else stop_sign
    # a4 = poop_emoji if pin_A4.value else stop_sign
    # a5 = poop_emoji if pin_A5.value else stop_sign
    # a6 = poop_emoji if pin_A6.value else stop_sign
    # a7 = poop_emoji if pin_A7.value else stop_sign
    # b7 = poop_emoji if pin_B7.value else stop_sign
    board = a1
    # board += a3 + a4 + a5 + '\n'
    # board += a6 + a7 + b7
    print()
    print(board)


# Denne koden kjører fint 14.09.23, vi fikk til expanders :)