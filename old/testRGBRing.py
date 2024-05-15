# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi

import time
import board
import neopixel


# ---------- Expander stuff ---------
import busio
import digitalio
from RPi import GPIO
from adafruit_mcp230xx.mcp23017 import MCP23017

# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)  # MCP23017

pin_A0 = mcp.get_pin(0)
pin_A1 = mcp.get_pin(1)
pin_A2 = mcp.get_pin(2)
pin_A3 = mcp.get_pin(3)
pin_A4 = mcp.get_pin(4)
pin_A5 = mcp.get_pin(5)
pin_A6 = mcp.get_pin(6)
pin_A7 = mcp.get_pin(7)
pin_B7 = mcp.get_pin(15)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button1 = board.GPIO1
button2 = board.GPIO17
button3 = board.GPI22

pin_A1.direction = digitalio.Direction.INPUT

pin_A0.pull = digitalio.Pull.UP
pin_A1.pull = digitalio.Pull.UP
pin_A2.pull = digitalio.Pull.UP
pin_A3.pull = digitalio.Pull.UP
pin_A4.pull = digitalio.Pull.UP
pin_A5.pull = digitalio.Pull.UP
pin_A6.pull = digitalio.Pull.UP
pin_A7.pull = digitalio.Pull.UP
pin_B7.pull = digitalio.Pull.UP
# --------------------


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 35 * 12 

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


def cycle_through_pixels(wait):
    for i in range(num_pixels):
        pixels.fill((0,0,0))
        pixels[i] = (255,0,0)
        pixels.show()
        time.sleep(wait)
    


while True:
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((255, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 255, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0, 0))
    pixels.show()
    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255, 0))
    pixels.show()
    time.sleep(1)

    # cycle_through_pixels(0.1)  # rainbow cycle with 1ms delay per step