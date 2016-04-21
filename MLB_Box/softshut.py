#http://www.raspberry-pi-geek.com/Archive/2013/01/Adding-an-On-Off-switch-to-your-Raspberry-Pi/%28offset%29/4

#Import the modules to send commands ot the system and access the GPIO pins
from subprocess import call
import RPi.GPIO as gpio
import time

#Set pin numbering to board numbering
gpio.setmode(gpio.BOARD)
#Set pin 11 as input
gpio.setup(11, gpio.IN)
#Set up an interrupt to look for button presses.
#gpio.add_event_detect(11, gpio.RISING, callback=shutdown, bouncetime=200)

prev_input = 0
while(True):
    is_pressed = gpio.input(11)
    if ((not prev_input) and is_pressed):
        call(['sudo', 'shutdown', '-h', 'now'])
    #end if
    prev_input = is_pressed
    time.sleep(0.05)
#endWhile

