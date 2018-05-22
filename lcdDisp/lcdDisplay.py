
import RPi.GPIO as GPIO
import time
import smbus
from .HD44780 import hwcmd as h
from .HD44780 import gpioMapping as gm
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TL_PAGE1 = 40
TR_PAGE1 = 48
BL_PAGE1 = 80
BR_PAGE1 = 88
TL_PAGE2 = 16
TR_PAGE2 = 24
BL_PAGE2 = 56
BR_PAGE2 = 64

#This is a page initialation. It is provide 2 field one line each ,total 4 fields.
#Line1 0~15 and Line2 40~55 we called page1 and page2 is in the line1 16~31 and line2 56~71 range.
#Input (numofpage (1 or 2), TopLeft,para2,para3,para4)
def page_init(nop,TL,TR,BL,BR):
  if (nop == 1):
    h.cur_seek(1,TL_PAGE1)
    h.print_msg(TL)
    h.cur_seek(1,TR_PAGE1)
    h.print_msg(TR)
    h.cur_seek(2,BL_PAGE1)
    h.print_msg(BL)
    h.cur_seek(2,BR_PAGE1)
    h.print_msg(BR)
  else :
    h.cur_seek(1,TL_PAGE2)
    h.print_msg(TL)
    h.cur_seek(1,TR_PAGE2)
    h.print_msg(TR)
    h.cur_seek(2,BL_PAGE2)
    h.print_msg(BL)
    h.cur_seek(2,BR_PAGE2)
    h.print_msg(BR)
  print('page'+str(nop))

#print a string via defined address
def print_string(string,location):
  if (location == 0):
    h.cur_seek(1,TL_PAGE1)
  elif (location == 1):
    h.cur_seek(1,TR_PAGE1)
  elif (location == 2):
    h.cur_seek(2,BL_PAGE1)
  elif (location == 3):
    h.cur_seek(2,BR_PAGE1)
  else :
    string ="ERROR"
  h.print_msg(string)

def diagnostic():
  h.lcd_init(12,13,11,7,8,9,10)
  h.lcd_clear()
  h.print_msg('V:04.3')
  time.sleep(1)
  h.cur_seek(1,8)
  h.print_msg('I:0.36')
  time.sleep(1)
  h.cur_seek(1,16)
  h.print_msg('T:34.9 Page2')
  time.sleep(1)
  h.cur_seek(2,0)
  h.print_msg('01234 Page1')
  time.sleep(1)
  h.lcd_onoff(h.LCD_OFF)
  for count in range (0,16):
    time.sleep(1e-3)
    h.lcd_shift(h.SHIFT_ON,h.SHIFT_L)
  h.lcd_onoff(h.LCD_ON)
  time.sleep(2)
  h.lcd_onoff(h.LCD_OFF)
  for count in range (0,16):
    time.sleep(1e-3)
    h.lcd_shift(h.SHIFT_ON,h.SHIFT_R)
  h.lcd_onoff(h.LCD_ON)
  time.sleep(1)
  h.lcd_onoff(h.LCD_OFF)
  time.sleep(1)
  h.lcd_onoff(h.LCD_ON)

def two_page_disp():
  time.sleep(1)
  h.lcd_onoff(h.LCD_OFF)
  for count in range (0,16):
    time.sleep(1e-3)
    h.lcd_shift(h.SHIFT_ON,h.SHIFT_L)
  h.lcd_onoff(h.LCD_ON)
  time.sleep(2)
  h.lcd_onoff(h.LCD_OFF)
  for count in range (0,16):
    time.sleep(1e-3)
    h.lcd_shift(h.SHIFT_ON,h.SHIFT_R)
  h.lcd_onoff(h.LCD_ON)

#Entry point here
h.lcd_init(12,13,11,7,8,9,10)


# This is 16x2 LCD char display.
# This API is used to define your naming length (1~4 char) follow a string with max.4char.
# def layoutInit(line1Leftname,line1Stg,line2Leftname,line2Stg):
