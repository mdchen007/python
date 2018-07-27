#GPIO mapping to HD44780
vss = 1 #ground
vdd = 2 #5volt.
v0 = 3
rs = 4 #send a command (0) , updating the display (1) over dbx pins
rw = 5 #read (1)/write (0)
en = 6 #enable pin, hi=enable , low=disable. (w/ 10uf cap in the enternal is perfer.)
db0 = 7 #for 8bit command only
db1 = 8 #for 8bit command only
db2 = 9 #for 8bit command only
db3 = 10 #for 8bit command only
db4 = 11 #for 4bit/8bit command
db5 = 12 #for 4bit/8bit command
db6 = 13 #for 4bit/8bit command
db7 = 14 #for 4bit/8bit command
ledp = 15 #LED+
ledm = 16 #LED-

#Defined by user of MCU which physical pins is used and mapping to HD44780
import RPi.GPIO as GPIO
def lcdPinInit(rs,rw,en,db4,db5,db6,db7):
  global pinRs,pinRw,pinEn,pinDb4,pinDb5,pinDb6,pinDb7
  pinRs = rs
  #RW pin can be wired to ground by hardware setting
  pinRw = rw
  pinEn = en
  pinDb4 = db4
  pinDb5 = db5
  pinDb6 = db6
  pinDb7 = db7
  GPIO.setup(pinRs,GPIO.OUT)
  GPIO.setup(pinRw,GPIO.OUT)
  GPIO.setup(pinEn,GPIO.OUT)
  GPIO.setup(pinDb4,GPIO.OUT)
  GPIO.setup(pinDb5,GPIO.OUT)
  GPIO.setup(pinDb6,GPIO.OUT)
  GPIO.setup(pinDb7,GPIO.OUT)
