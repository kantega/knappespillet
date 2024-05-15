# Simple program for testing that all the lights are connected, and can be controlled by a single button
import time
import board
import neopixel

# ---------- Expander stuff ---------
from RPi import GPIO

BUTTON_GPIO_PIN = 17
GPIO.setup(BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
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

while True:
    button_is_clicked = GPIO.input(BUTTON_GPIO_PIN) 
    current_color = green_color if button_is_clicked else red_color 
    pixels.fill(current_color)
    pixels.show()
    time.sleep(0.01)