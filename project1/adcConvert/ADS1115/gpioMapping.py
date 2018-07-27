#GPIO mapping to ADS1115
from .import pinDef as pd


#Defined by user of MCU which physical pins is used and mapping to HD44780
import RPi.GPIO as GPIO
import smbus
def adcPinInit(scl,sda,alrt): #later we may define i2c input gpio.
  global pinScl,pinSda,pinAlrt
  pinScl = rw
  pinSda = en
  pinAlrt = alrt
  GPIO.setup(pinAlrt,GPIO.IN)
