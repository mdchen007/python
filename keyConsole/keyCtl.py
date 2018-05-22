
import RPi.GPIO as GPIO
import time
from KEYCTL import hwcmd as h
GPIO.setmode(GPIO.BCM)
global keyList
# 0 default. 1 toggle , 2 exit.
keyList =[[],[]]
GPIO17 =17
GPIO23 =23

def toggle_func(callback):
    keystate = 1
    print ("falling edge detected on 17 ,state =%s"%keystate)
    callback()

def exit_func(callback):
    keystate =2
    print ("falling edge detected on 23, state =%s"%keystate)
    callback()

def printmsg():
  print("callback function")

# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
# So we'll be setting up falling edge detection for both
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
h.callbackByio(GPIO17,toggle_func)
h.callbackByio(GPIO23,exit_func)
global keystate
keystate =3
while((keystate != 2)):
  print ("state %s"%keystate)
  time.sleep(0.1)
  pass
#keyList =[[GPIO17,GPIO23][toggle_func][exit_func]]
# GPIO 24 set up as an input, pulled down, connected to 3V3 on button press
#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# now we'll define two threaded callback functions
# these will run in another thread when our events are detected
#h.key_init(2,keyList)
