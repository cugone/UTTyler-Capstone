#Copyright (C) 2016 Casey Ugone
#Full description of licensing rights available in LICENSE.txt file provided with this distribution.
#If a LICENSE.txt file was not provided with this distribution, it is in violation of the GPLv3

import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

pulsesPerCycle = 60
pwm = GPIO.PWM(11, pulsesPerCycle)

pi_list = [x for x in range(0, 2)]
print(pi_list)

for i in pi_list:
    print(i * 0.06)
    pwm.start(i * 0.06)
    time.sleep(0.16)
#end for

pwm.stop()
GPIO.cleanup()

print("DONE! :D")
