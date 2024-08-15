import time

from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import neopixel
import numpy as np
import busio
import digitalio

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)  # MCP23017

pin_A0 = mcp.get_pin(0)
pin_A1 = mcp.get_pin(1)

pin_A0.switch_to_output(value=True)

pin_A1.direction = digitalio.Direction.INPUT
pin_A1.pull = digitalio.Pull.UP

print(pin_A0.value, pin_A0, pin_A0._pin)
# LED strip configuration:
LED_COUNT   = 12      # Number of LED pixels.
LED_PIN     = board.D18     # GPIO pin
LED_BRIGHTNESS = 1  # LED brightness
LED_ORDER = neopixel.GRB # order of LED colours. May also be RGB, GRBW, or RGBW

# The colour selection selected for this project: red, blue, yellow, green, pink, and silver respectively

gokai_colours = [(255,0,0),(0,0,255),(255,255,0),(0,255,0),(255,105,180),(192,192,192)]

# Create NeoPixel object with appropriate configuration.
strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness = LED_BRIGHTNESS, auto_write=False, pixel_order = LED_ORDER)

# Create a way to fade/transition between colours using numpy arrays

def fade(colour1, colour2, percent):
    colour1 = np.array(colour1)
    colour2 = np.array(colour2)
    vector = colour2-colour1
    newcolour = (int((colour1 + vector * percent)[0]), int((colour1 + vector * percent)[1]), int((colour1 + vector * percent)[2]))
    return newcolour

# Create a function that will cycle through the colours selected above
	
def rollcall_cycle(wait):
    for j in range(len(gokai_colours)):
        for i in range(10):
            color1 = gokai_colours[j]
            if j == 5:
                color2 = (255,255,255)
            else:
                color2 = gokai_colours[(j+1)]
            percent = i*0.1   # 0.1*100 so 10% increments between colours
            strip.fill((fade(color1,color2,percent)))
            strip.show()
            time.sleep(wait)

strip.fill((255,255,255))
strip.show()

# Main function loop
print("Starting")
 
while True:
    time.sleep(1)
    print("Hello world")
    if not pin_A1.value:
        print("Hello world again")
        rollcall_cycle(0.2)    # 0.2 seconds between colour updates
    else:
        print("Nothing")



        #Får knappen til å fungere men ikke til å funke men får ikke lys i neopixelen. 12.10.23 Magnus
