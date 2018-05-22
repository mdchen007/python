#ADS1115 16bit AD converter
#import RPi.GPIO as GPIO
#import time
#import smbus
from .ADS1115 import hwcmd as h
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
SA_DEFAULT = 0x48

def getChVal(ch):
  return(h.getAdc(ch))

#Entry point
h.adc_init(SA_DEFAULT,1,h.FSR_TABLE[4.096],h.CH_TABLE[3])




