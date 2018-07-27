#for GPIO
import RPi.GPIO as GPIO
import time
KEY_DRV_VER ="KEY-CMD-R0.1"
GPIO.setmode(GPIO.BCM)
#ioList = [[0 for x in range(2)] for y in range(1)]

# when a falling edge is detected on port 17, regardless of whatever
# else is happening in the program, the function my_callback will be run
#def callbackByio(pinno,callbackFunc):
#  GPIO.add_event_detect(pinno, GPIO.FALLING, callback=callbackFunc, bouncetime=300)

# [pinNo.][funcpoint]
def key_init(noOf,ioList):
  print("%s"%KEY_DRV_VER)
  for x in range (noOf):
    GPIO.setup(ioList[x][0],GPIO.IN,GPIO.PUD_UP)
    GPIO.add_event_detect(ioList[x][0], GPIO.FALLING, callback=ioList[x][1], bouncetime=300)


