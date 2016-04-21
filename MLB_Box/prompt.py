#http://www.raspberry-pi-geek.com/Archive/2013/01/Adding-an-On-Off-switch-to-your-Raspberry-Pi/%28offset%29/4

#Import the modules to send commands ot the system and access the GPIO pins
import os
import time
from subprocess import call
import RPi.GPIO as gpio

#Define a function to run when an interrupt is called
def prompt_standings(pin):
    call(['python3', \
          '/home/pi/PiSupply/UTTyler-Capstone/MLB_Box/mlbbox.py'])
#end shutdown

#Set pin numbering to board numbering
gpio.setmode(gpio.BOARD)
#Set pin 12 as input
gpio.setup(12, gpio.IN)
#Set up an interrupt to look for button presses.
#gpio.add_event_detect(12, gpio.RISING, callback=prompt_standings, bouncetime=400)

prev_input = 0
while(True):
    is_pressed = gpio.input(12)
    if((not prev_input) and is_pressed):
        os.system('python3 /home/pi/PiSupply/UTTyler-Capstone/MLB_Box/mlbbox.py')
    #end if
    prev_input = is_pressed
    time.sleep(0.05)
#end while
