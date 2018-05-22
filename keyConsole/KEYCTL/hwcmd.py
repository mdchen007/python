#for GPIO
import RPi.GPIO as GPIO
import time
KEY_DRV_VER ="KEY-CMD-R0.1"
GPIO.setmode(GPIO.BCM)

def my_callback(channel):
    print ("falling edge detected on 17")

def my_callback2(channel):
    print ("falling edge detected on 23")

# when a falling edge is detected on port 17, regardless of whatever
# else is happening in the program, the function my_callback will be run
def callbackByio(pinno,callbackFunc):
  GPIO.add_event_detect(pinno, GPIO.FALLING, callback=callbackFunc, bouncetime=300)

# [pinNo.][funcpoint]
def key_init(noOfPin,ioList):
  for i in range (noOfPin):
    ioList.append[[i],[i]]
  for x in range (noOfPin):
    GPIO.setup(ioList[[x],[0]],GPIO.IN,GPIO.PUD_UP)
    callbackByio(ioList[[1],[x]],ioList[[1],[x]])
