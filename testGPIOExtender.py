import time
import board
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017

#This exapmle is a simple test for the MCP23017 GPIO Extender when connected to a Raspberry Pi.
#The setup of the expanders is that the SDA and SCL i2C connetion is daisy chained to each expander board.
#The address of the expanders are set by soldering is by following the guide on the adafruit website: https://learn.adafruit.com/adafruit-mcp23017-i2c-gpio-expander/pinouts#address-pins-3113114

# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)

# Create instancees of the MCP23017 class with adresses for the 5 expanders
mcp0 = MCP23017(i2c, address=0x20)
mcp1 = MCP23017(i2c, address=0x21)  
mcp2 = MCP23017(i2c, address=0x22)
mcp3 = MCP23017(i2c, address=0x23)
mcp4 = MCP23017(i2c, address=0x24)

board0pin0 = mcp0.get_pin(0)
board1pin0 = mcp1.get_pin(0)
board2pin0 = mcp2.get_pin(0)
board3pin0 = mcp3.get_pin(0)
board4pin0 = mcp4.get_pin(0)

board0pin0.direction = digitalio.Direction.INPUT
board0pin0.pull = digitalio.Pull.UP

board1pin0.direction = digitalio.Direction.INPUT
board1pin0.pull = digitalio.Pull.UP

board2pin0.direction = digitalio.Direction.INPUT
board2pin0.pull = digitalio.Pull.UP

board3pin0.direction = digitalio.Direction.INPUT
board3pin0.pull = digitalio.Pull.UP

board4pin0.direction = digitalio.Direction.INPUT
board4pin0.pull = digitalio.Pull.UP

# Now loop blinking the pin 0 output and reading the state of pin 1 input.
while True:
    time.sleep(0.01)
    time.sleep(0.01)
    # Read pin 1 and print its state.
    print("Board0: {0} Board1: {1} Board2: {2} Board3: {3} Board4: {4}".format(board0pin0.value, board1pin0.value, board2pin0.value, board3pin0.value, board4pin0.value))

#This expander test worked with 2 expanders daisy chained: 11.04.23 - Magnus, Nikolai, Erik