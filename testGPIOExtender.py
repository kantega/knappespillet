from adafruit_mcp230xx.mcp23017 import MCP23017
import time
import board
import busio
import digitalio

# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)  # MCP23017

pin_A0 = mcp.get_pin(0)
pin_A1 = mcp.get_pin(1)

pin_A0.switch_to_output(value=True)


pin_A1.direction = digitalio.Direction.INPUT
pin_A1.pull = digitalio.Pull.UP


while True:
    pin_A0.value = True
    time.sleep(0.1)
    pin_A0.value = False
    time.sleep(0.1)
    # Read pin 1 and print its state.
    print("Pin 1 is at a high level: {0}".format(pin_A1.value))


# Denne koden kjører fint 14.09.23, vi fikk til expanders :)