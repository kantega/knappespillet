import time
import board
import busio
import digitalio
# Simple program for testing that all the lights are connected, and can be controlled by a single button
import time
import board
import neopixel

# ---------- Expander stuff ---------

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

""" 
5 Rows x 7 Columns = 35 buttons
Coordinates for the buttons are as follows:

4,0    4,1    4,2    4,3    4,4    4,5    4,6
3,0    3,1    3,2    3,3    3,4    3,5    3,6
2,0    2,1    2,2    2,3    2,4    2,5    2,6
1,0    1,1    1,2    1,3    1,4    1,5    1,6
0,0    0,1    0,2    0,3    0,4    0,5    0,6
"""

row0column0 = mcp0.get_pin(0)
row1column0 = mcp1.get_pin(0)
row2column0 = mcp2.get_pin(0)
row3column0 = mcp3.get_pin(0)
row4column0 = mcp4.get_pin(0)

# row0column1 = mcp0.get_pin(1)
# row1column1 = mcp1.get_pin(1)
# row2column1 = mcp2.get_pin(1)
# row3column1 = mcp3.get_pin(1)
# row4column1 = mcp4.get_pin(1)

# row0column2 = mcp0.get_pin(2)
# row1column2 = mcp1.get_pin(2)
# row2column2 = mcp2.get_pin(2)
# row3column2 = mcp3.get_pin(2)
# row4column2 = mcp4.get_pin(2)

# row0column3 = mcp0.get_pin(3)
# row1column3 = mcp1.get_pin(3)
# row2column3 = mcp2.get_pin(3)
# row3column3 = mcp3.get_pin(3)
# row4column3 = mcp4.get_pin(3)

# row0column4 = mcp0.get_pin(4)
# row1column4 = mcp1.get_pin(4)
# row2column4 = mcp2.get_pin(4)
# row3column4 = mcp3.get_pin(4)
# row4column4 = mcp4.get_pin(4)


row0column5 = mcp0.get_pin(5)
row1column5 = mcp1.get_pin(5)
row2column5 = mcp2.get_pin(5)
row3column5 = mcp3.get_pin(5)
row4column5 = mcp4.get_pin(5)

row0column6 = mcp0.get_pin(6)
row1column6 = mcp1.get_pin(6)
row2column6 = mcp2.get_pin(6)
row3column6 = mcp3.get_pin(6)
row4column6 = mcp4.get_pin(6)

all_buttons = [
row0column0 ,  
row1column0 ,
row2column0 ,
row3column0 ,
row4column0 ,

# row0column1 ,
# row1column1 ,
# row2column1 ,
# row3column1 ,
# row4column1 ,

# row0column2 ,
# row1column2 ,
# row2column2 ,
# row3column2 ,
# row4column2 ,

# row0column3 ,
# row1column3 ,
# row2column3 ,
# row3column3 ,
# row4column3 ,

# row0column4 ,
# row1column4 ,
# row2column4 ,
# row3column4 ,
# row4column4 ,

row0column5,
row1column5,
row2column5,
row3column5,
row4column5,

row0column6,
row1column6,
row2column6,
row3column6,
row4column6,
]

for button in all_buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP



pixel_pin = board.D18 # GPIO18 yellow

NUMBER_OF_CONNECTED_PIXEL_RINGS = 35
PIXELS_PER_PIXEL_RING = 12
NUM_PIXELS = NUMBER_OF_CONNECTED_PIXEL_RINGS * PIXELS_PER_PIXEL_RING 

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER
)

print("STARTING testSingleButtonPressAndCycleLight script")

red_color = (255, 0, 0)
green_color = (0, 255, 0)
blue_color = (0, 255, 255)



def cycle_trough_each_ring():
    for i in range(NUMBER_OF_CONNECTED_PIXEL_RINGS):
        pixels.fill((0,0,0))
        for j in range(PIXELS_PER_PIXEL_RING):
            pixels[i* PIXELS_PER_PIXEL_RING + j ] = blue_color
        time.sleep(0.04)
        pixels.show()

cycle_trough_each_ring()
print("INITIALIZING pixels with color green")
pixels.fill(green_color)
pixels.show()
# Now loop blinking the pin 0 output and reading the state of pin 1 input.
while True:
    any_button_is_clicked = any(all_buttons)
    current_color = green_color if any_button_is_clicked else red_color 
    pixels.fill(current_color)
    pixels.show()
    time.sleep(0.01)
    # Read pin 1 and print its state.
    # print("Pin0 Board0: {0} Board1: {1} Board2: {2} Board3: {3} Board4: {4}".format(board0pin0.value, board1pin0.value, board2pin0.value, board3pin0.value, board4pin0.value))

    # print("Pin6 Board0: {0} Board1: {1} Board2: {2} Board3: {3} Board4: {4}".format(board0pin6.value, board1pin6.value, board2pin6.value, board3pin6.value, board4pin6.value))

#This expander test worked with 2 expanders daisy chained: 11.04.23 - Magnus, Nikolai, Erik