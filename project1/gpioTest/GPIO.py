

import RPi.GPIO as GPIO
import time

pin =6
status =True
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin,GPIO.OUT)
for x in range(100):
    GPIO.output(pin, status)
    print(GPIO.input(pin))
    time.sleep(1)
    status = not status
    #GPIO.output(pin,1)
    #time.sleep(1)
    #print(GPIO.input(pin))
    #if GPIO.input(pin):
    # print ("High")
    #else:
    #print ("Low") 
