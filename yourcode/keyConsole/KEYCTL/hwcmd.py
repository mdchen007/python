
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time
KEY_DRV_VER ="KEY-CMD-R0.1"

# [pinNo.][funcpoint]
def key_init(noOf,ioList):
  print("%s"%KEY_DRV_VER)
  for x in range (noOf):
    GPIO.setup(ioList[x][0],GPIO.IN,GPIO.PUD_UP)
    GPIO.add_event_detect(ioList[x][0], GPIO.FALLING, callback=ioList[x][1], bouncetime=300)


