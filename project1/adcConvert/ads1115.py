#ADS1115 16bit AD converter
import RPi.GPIO as GPIO
import time
import smbus
ADC_DRV_VER ="ADC-R03"
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#bandGap of SFR
global FSR6,FSR4,FSR2,FSR1,FSR05,FSR02
FSR6 = 0x0000
FSR4 = 0x0200
FSR2 = 0x0400
FSR1 = 0x0600
FSR05= 0x0800
FSR02= 0x0c00
#MUX of channels
global CH0TOGND,CH1TOGND,CH2TOGND,CH3TOGND
CH0TOGND = 0x4000
CH1TOGND = 0x5000
CH2TOGND = 0x6000
CH3TOGND = 0x7000
#I2C Register address
I2C_ADDR_POINT_CONV = 0x00
I2C_ADDR_POINT_CONF = 0x01
I2C_ADDR_LOW_TH =0x02
I2C_ADDR_HI_TH = 0x03
#Config registser setting is '1 011 001 1 100 00011
I2C_CONF_SET = 0xf383 #ch3 , 4.096v



#In : common(ground) mode =1,no of ch,
def getAdc(ch):
  i2c = smbus.SMBus(1)
  print("userSA=%x ,userMODE=%x ,userFSR=%x "%(userSA,userMODE,userFSR))
  if (userMODE == 1):
    value = eConv((I2C_CONF_SET&0x81ff)|userFSR|(chConv(ch)))
    print("mode1, Configuration=%x " %value)
    i2c.write_word_data(userSA,I2C_ADDR_POINT_CONF,value)
    #check busy bit15
    value = i2c.read_word_data(userSA,I2C_ADDR_POINT_CONF)
    #if (((value >> 15) & 1 ) >0):
    time.sleep(1e-3)
    #print(hex(i2c.read_word_data(userSA,I2C_ADDR_POINT_CONF)))
    result =(i2c.read_word_data(userSA,I2C_ADDR_POINT_CONV))
    return eConv(result)
  elif (userMODE ==3):
    print ("userMODE =3 , blanking")
  elif (userMODE ==1):
    print ("userMODE = 1, blandking")
  else:
    print ("Out of range , no definition")

  #reg = I2C_ADDR_POINT_CONV
  #time.sleep(1e-3)
  #result =(i2c.read_word_data(addr,reg))
  ##byte swap for little endian of ARM
  #result = ((result << 8) & 0xFF00) + (result >> 8)
  #print(hex(result))
  #return result

#byte swap for little endian convertion of ARM
#In: Word
def eConv(value):
  result = ((value << 8) & 0xFF00) + (value >> 8)
  return int(result)

#get channel from
def chConv(ch):
  print("channel no. = %d"%ch)
  if (ch == 0):
    return CH0TOGND
  elif (ch == 1):
    return CH1TOGND
  elif (ch == 2):
    return CH2TOGND
  elif (ch == 3):
    return CH3TOGND
  else :
    return CH0TOGND

#In : slave address, mode =1(to common ground) or command(AN3)=3 ro diff(command AN1) =2,FSR,ch number
def adc_init(slaveAddr,mode,bandGapFSR,ch):
  global userSA,userFSR,userCH,userMODE
  print(ADC_DRV_VER)
  userSA  = slaveAddr
  userFSR = bandGapFSR
  userCH  = ch
  userMODE = mode
  print("userMODE setting =%i"%userMODE)

  i2c = smbus.SMBus(1)
  addr = slaveAddr
  value = I2C_ADDR_POINT_CONF
  i2c.write_byte(addr,value)
  reg = I2C_ADDR_POINT_CONF

  if (mode == 1):
    value = eConv((I2C_CONF_SET&0x81ff)|bandGapFSR|ch)
    print("init:mode1, value = %x" %value)
    i2c.write_word_data(addr,reg,value)
    print(hex(i2c.read_word_data(addr,reg)))
  elif (mode ==3):
    print ("mode =3 , blanking")
  elif (mode ==1):
    print ("mode = 1, blandking")
  else:
    print ("Out of range(init) , no definition")

#Entry point
adc_init(0x48,1,FSR4,CH3TOGND)




