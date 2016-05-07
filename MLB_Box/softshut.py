#Copyright (C) 2016 Casey Ugone
#Full description of licensing rights available in LICENSE.txt file provided with this distribution.
#If a LICENSE.txt file was not provided with this distribution, it is in violation of the GPLv3

#Import the modules to send commands ot the system and access the GPIO pins
from subprocess import call
import RPi.GPIO as gpio
import time

#Set pin numbering to board numbering
gpio.setmode(gpio.BOARD)
#Set pin 11 as input
gpio.setup(11, gpio.IN)

prev_input = 0
while(True):
    is_pressed = gpio.input(11)
    if ((not prev_input) and is_pressed):
        call(['sudo', 'shutdown', '-h', 'now'])
    #end if
    prev_input = is_pressed
    time.sleep(0.05)
#endWhile

