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


red_color = (255, 0, 0)
green_color = (0, 255, 0)
while True:
    button_is_clicked = GPIO.input(BUTTON_GPIO_PIN) 
    current_color = green_color if button_is_clicked else red_color 
    pixels.show()
    pixels.fill(current_color)
    time.sleep(0.1)