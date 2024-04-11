"""
This script sets up a simple game where random buttons RGB ring gets lit up, and the player needs to press the corresponding button. 
Each time the player presses the correct button, a counter is increased. The script runs indefinitely until interrupted.

Script can be run from on a raspberry pi that has installed following:

pip3 install adafruit-circuitpython-mcp230xx

Start script by standing in the same directory as the script and run it using the command

python completeGameSetup.py

"""
from adafruit_mcp230xx.mcp23017 import MCP23017
import time
import busio
import digitalio
import board
import neopixel
import random
import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels (Using 9 rgb rings with 12 light on each)
num_pixels = 12 * 9 

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# Initialize the I2C bus on the raspberry PI:
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)  # MCP23017

#Setup pins - Initial only imagines there is a 3 x 3 matrix of buttons
pin_A0 = mcp.get_pin(0)
pin_A1 = mcp.get_pin(1)
pin_A2 = mcp.get_pin(2)
pin_A3 = mcp.get_pin(3)
pin_A4 = mcp.get_pin(4)
pin_A5 = mcp.get_pin(5)
pin_A6 = mcp.get_pin(6)
pin_A7 = mcp.get_pin(7)
pin_B7 = mcp.get_pin(15)

pin_A0.pull = digitalio.Pull.UP
pin_A1.pull = digitalio.Pull.UP
pin_A2.pull = digitalio.Pull.UP
pin_A3.pull = digitalio.Pull.UP
pin_A4.pull = digitalio.Pull.UP
pin_A5.pull = digitalio.Pull.UP
pin_A6.pull = digitalio.Pull.UP
pin_A7.pull = digitalio.Pull.UP
pin_B7.pull = digitalio.Pull.UP

#TODO: Make all of the following setup a lot cleaner!
# Set button pixel mappings as variables
button_one_pixels = [0, 1, 2, 3, 4, 5, 6, 7, 8]
button_two_pixels = [9, 10, 11, 12, 13, 14, 15, 16, 17]
button_three_pixels = [18, 19, 20, 21, 22, 23, 24, 25, 26]
button_four_pixels = [27, 28, 29, 30, 31, 32, 33, 34, 35]
button_five_pixels = [36, 37, 38, 39, 40, 41, 42, 43, 44]
button_six_pixels = [45, 46, 47, 48, 49, 50, 51, 52, 53]
button_seven_pixels = [54, 55, 56, 57, 58, 59, 60, 61, 62]
button_eight_pixels = [63, 64, 65, 66, 67, 68, 69, 70, 71]
button_nine_pixels = [72, 73, 74, 75, 76, 77, 78, 79, 80]

def light_up_random_button():
    # Generate a random number between 1 and 9 to select a button
    button_number = random.randint(1, 9)
    
    # Determine the pixels associated with the selected button
    if button_number == 1:
        button_pixels = button_one_pixels
    elif button_number == 2:
        button_pixels = button_two_pixels
    elif button_number == 3:
        button_pixels = button_three_pixels
    elif button_number == 4:
        button_pixels = button_four_pixels
    elif button_number == 5:
        button_pixels = button_five_pixels
    elif button_number == 6:
        button_pixels = button_six_pixels
    elif button_number == 7:
        button_pixels = button_seven_pixels
    elif button_number == 8:
        button_pixels = button_eight_pixels
    elif button_number == 9:
        button_pixels = button_nine_pixels
    
    # Light up the pixels associated with the selected button
    for pixel in button_pixels:
        pixels[pixel] = (255, 255, 255)  # Set the pixel color to white
    
    pixels.show()  # Update the NeoPixel strip to show the changes
    
    return button_number

#Simple test game idea that:
    #Lights up a random buttons rgb ring
    #Waits for buttonpress
    #On button press, increase a counter
    #Turn off light of button
    #Repeats

while True:
    #Call function to light up a random button
    active_button = light_up_random_button()

    #Make pins into a list
    button_pins = [pin_A0, pin_A1, pin_A2, pin_A3, pin_A4, pin_A5, pin_A6, pin_A7, pin_B7]
    
    #Make pixels for each button into a list
    button_pixels = [button_one_pixels, button_two_pixels, button_three_pixels, button_four_pixels, button_five_pixels, button_six_pixels, button_seven_pixels, button_eight_pixels, button_nine_pixels]

    for i in range(len(button_pins)):
        if not button_pins[active_button - 1].value:
            counter += 1
            for pixel in button_pixels[active_button - 1]:
                pixels[pixel] = (0, 0, 0)
            pixels.show()
            break
    
    # Print the emoji matrix
    counter = 0

    for row in range(3):
        for col in range(3):
            if (row * 3) + col + 1 == active_button:
                print("🟢")
            else:
                print("⚪️")
        print()

    print("Counter:", counter)

    # Create I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Check I2C connection and device address
    if not i2c.try_lock():
        raise ValueError("Unable to acquire I2C bus lock")
    try:
        devices = i2c.scan()
        if not 0x20 in devices:
            raise ValueError("No I2C device at address: 0x20")
    finally:
        i2c.unlock()

    # Initialize MCP23017
    mcp = MCP23017(i2c, address=0x20)

    # TODO: Add a way to wait for a button press and check if the button press is correct
