
import RPi.GPIO as GPIO
import time
#import queue
from queue import Queue
from .KEYCTL.hwcmd import key_init
#from KEYCTL import hwcmd as h
GPIO.setmode(GPIO.BCM)
GPIO17 =17
GPIO23 =23

#keyList [GPIO NO.][callbackFunc]
global keyList,keystate,kq
keystate =5
#kq = queue.Queue()
kq = Queue()

def toggle_func(callback):
    keystate = 1
    kq.put(keystate)
    print ("falling edge detected on GPIO17 ,state =%s"%keystate)
    #callback()

def exit_func(callback):
    keystate =2
    print ("falling edge detected on GPIO23 , state =%s"%keystate)
    kq.put(keystate)
    #callback()

def key_cb_enable(nop,callbacklist):
  key_init(noOfPin,keyList)

### code entry point
if __name__ == "__main__":
    print("keyCtl.py is being run directly")
else:
    print("keyCtl is being imported into another module")

# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
# So we'll be setting up falling edge detection for both

w, h ,noOfPin = 2, 2, 2;
keyList = [[0 for x in range(w)] for y in range(h)]
keystate =4
#keyList[0][0]= GPIO17
#keyList[0][1]= toggle_func
#keyList[1][0]= GPIO23
#keyList[1][1]= exit_func

#key_init(noOfPin,keyList)
#
#while((keystate != 2)):
#  print ("state %s"%keystate)
#  while not kq.empty():
#    keystate = kq.get()
#    print ("state-q %s"%keystate)
#  time.sleep(0.2)
#print ("state-exit")




