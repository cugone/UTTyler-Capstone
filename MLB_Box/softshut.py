#http://www.raspberry-pi-geek.com/Archive/2013/01/Adding-an-On-Off-switch-to-your-Raspberry-Pi/%28offset%29/4

#Import the modules to send commands ot the system and access the GPIO pins
from subprocess import call
import RPi.GPIO as gpio

#Define a function to keep script running
def loop():
    input()
#end loop

#Define a function to run when an interrupt is called
def shutdown(pin):
    call(['sudo', 'shutdown', '-h', 'now'])
#end shutdown

print("!!!SETTING UP GPIO...")
#Set pin numbering to board numbering
gpio.setmode(gpio.BOARD)
#Set pin 11 as input
gpio.setup(11, gpio.IN)
#Set up an interrupt to look for button presses.
gpio.add_event_detect(11, gpio.RISING, callback=shutdown, bouncetime=200)

#Run the loop function to keep script running.
loop()
