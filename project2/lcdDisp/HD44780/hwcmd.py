#for HD44780
from .import gpioMapping as gm
import RPi.GPIO as GPIO

import time
LCD_DRV_VER ="LCD-HWCMD-R04"
#LCD_CLR
global LCD_CLR,LCD_ENTRY,LCE_FUNC,LCD_DISP,LCD_ON,LCD_OFF,LCD_SHIFT,SHIFT_ON,SHIFT_OFF,SHIFT_R,SHIFT_L
LCD_CLR= 0x01
#LCD_ENTRY_MODE
LCD_ENTRY= 0x06
#send a "function set" command ,2x16line,4bit data,5x10 char
LCD_FUNC = 0x2c
#"1xxx" display control on/off ,"x1xx" power on,"xx1x" enable cursor,"xxx1" enable cursor blink
LCD_DISP = 0x0C
LCD_ON = 0x04
LCD_OFF = 0x00
LCD_SHIFT = 0x10
SHIFT_ON = 0x08
SHIFT_OFF = 0x00
SHIFT_R = 0x04
SHIFT_L = 0x00
NC =0

def write_4bmode(command, rs_value):
  GPIO.output(gm.pinRs,rs_value)
  time.sleep(1e-3)
  #NC =0
  if gm.pinRw == NC:
    pass
  else :
    GPIO.output(gm.pinRw,GPIO.LOW)
    time.sleep(1e-3)
#  busy_sign() #
  GPIO.output(gm.pinDb4,GPIO.HIGH if ((command >> 4) & 1 ) >0 else GPIO.LOW)
  GPIO.output(gm.pinDb5,GPIO.HIGH if ((command >> 5) & 1 ) >0 else GPIO.LOW)
  GPIO.output(gm.pinDb6,GPIO.HIGH if ((command >> 6) & 1 ) >0 else GPIO.LOW)
  GPIO.output(gm.pinDb7,GPIO.HIGH if ((command >> 7) & 1 ) >0 else GPIO.LOW)
  pulse_en()
#  busy_sign() #
  GPIO.output(gm.pinDb4,GPIO.HIGH if ((command >> 0) & 1 ) >0 else GPIO.LOW)
  GPIO.output(gm.pinDb5,GPIO.HIGH if ((command >> 1) & 1 ) >0 else GPIO.LOW)
  GPIO.output(gm.pinDb6,GPIO.HIGH if ((command >> 2) & 1 ) >0 else GPIO.LOW)
  GPIO.output(gm.pinDb7,GPIO.HIGH if ((command >> 3) & 1 ) >0 else GPIO.LOW)
  pulse_en()
#  busy_sign() #

def pulse_en(delay=1e-3):
  time.sleep(delay)
  GPIO.output(gm.pinEn,GPIO.HIGH)
  time.sleep(delay)
  GPIO.output(gm.pinEn,GPIO.LOW)
  time.sleep(delay)

#special functon to send only the four highest-order bits;
def write4(value):
  GPIO.output(gm.pinRs,GPIO.LOW)
#  busy_sign() #
  time.sleep(1e-3)
  GPIO.output(gm.pinDb4,GPIO.HIGH if ((value >> 0) & 1 ) >0 else GPIO.LOW)
  GPIO.output(gm.pinDb5,GPIO.HIGH if ((value >> 1) & 1 ) >0 else GPIO.LOW)
  GPIO.output(gm.pinDb6,GPIO.HIGH if ((value >> 2) & 1 ) >0 else GPIO.LOW)
  GPIO.output(gm.pinDb7,GPIO.HIGH if ((value >> 3) & 1 ) >0 else GPIO.LOW)
  pulse_en()
 # busy_sign() #


def lcd_init(rs,rw,en,db4,db5,db6,db7):

  gm.lcdPinInit(rs,rw,en,db4,db5,db6,db7)
  #magic sequence
  write4(int("0011", 2))
  write4(int("0011", 2))
  write4(int("0011", 2))
  write4(int("0010", 2))

  #send a "function set" command , 2x16line,4bit data,5x10 char
  write_4bmode(int(LCD_FUNC), rs_value=GPIO.LOW)
  #"1xxx" display control on/off ,"x1xx" power on,"xx1x" enable cursor,"xxx1" enable cursor blink
  #lcd_disp = 0x0f
  write_4bmode(int(LCD_DISP), rs_value=GPIO.LOW)
  #clear the display
  write_4bmode(int(LCD_CLR), rs_value=GPIO.LOW)
  #send the "entry mode set" to set left2right printing(110).
  write_4bmode(int(LCD_ENTRY), rs_value=GPIO.LOW)
  #LCD driver version
  print(LCD_DRV_VER)

# Display on/off control
def lcd_onoff(switch):
  #write_4bmode(int(LCD_DISP&0x0b), rs_value=GPIO.LOW)
  write_4bmode(int(LCD_DISP|switch if ((switch >> 2) &1 ) > 0 else LCD_DISP&(~LCD_ON)), rs_value=GPIO.LOW)

# Define line : 1~2 , position 0~39 (Leftest 0 , Rightest 39)
def cur_seek(line,position):
  acc =(0x80)
  while (position >= 40):
    position-=40
  #address= ((position if (position <40) else position-40) if (line ==1) else (position+64 if (position <40) else (position-40+64)) if (line ==2) else 0)
  address= (position if (line ==1) else ((position+64) if (line ==2) else 0))
  #print(address)
  # set DDRAM address "1AAAAAAA"
  write_4bmode((int(address)|acc), rs_value=GPIO.LOW)

# Clear LCD and cursor to 0 position"
def lcd_clear():
   write_4bmode(int("00000001",2), rs_value=GPIO.LOW)

# LCD shift function (shift_enable,direction)
def lcd_shift(shift_enable,direction):
# set DDRAM address "1AAAAAAA"
  write_4bmode(int((LCD_SHIFT|SHIFT_R|SHIFT_ON) if (direction==SHIFT_R) else LCD_SHIFT|SHIFT_ON if ((shift_enable >> 3) &1 ) > 0 else LCD_SHIFT&SHIFT_OFF), rs_value=GPIO.LOW)

# No condition printing.
def print_msg(instg):
  for letter in instg:
    write_4bmode(ord(letter),rs_value=GPIO.HIGH)

# This is kind of trace function when you need a sign(GPIO BCMpin6) in the hardware debug
'''def busy_sign():
  pinout = 6
  GPIO.setup(pinout,GPIO.OUT)
  GPIO.output(gm.pinRw,GPIO.HIGH)
  #get busy flag of pinDb7
  pulse_en()
  GPIO.output(pinout,GPIO_HIGH if (gm.pinDb7) == True else GPIO.LOW)
  #get address counter from db4~7 , now no use
  pulse_en()
  GPIO.output(gm.pinRw,GPIO.LOW)'''
