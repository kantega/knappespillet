import RPi.GPIO as GPIO  
from time import sleep

GPIO.setmode(GPIO.BCM) # set up BCM GPIO numbering (BOARD is the alternative, aka pin numbers)

possible_pins=[16,23]

for pin in possible_pins:
    GPIO.setup(pin, GPIO.IN)

try:  
    while True: 
        anyHigh = False
        for pin in possible_pins:
            if GPIO.input(pin):
                print("PIN "+str(pin)+" HIGH")
                anyHigh=True        
        if anyHigh==False:
            print("All PINS are LOW")
        sleep(0.1)
  
except KeyboardInterrupt:  
    GPIO.cleanup()    