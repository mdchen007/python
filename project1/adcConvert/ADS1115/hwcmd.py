#ADS1115 16bit AD converter
import RPi.GPIO as GPIO
import time
import smbus
ADC_DRV_VER ="ADC-R05"
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#bandGap of SFR
#global FSR6,FSR4,FSR2,FSR1,FSR05,FSR02
FSR6 = 0x0000
FSR4 = 0x0200
FSR2 = 0x0400
FSR1 = 0x0600
FSR05= 0x0800
FSR02= 0x0c00
#MUX of channels
#global CH0TOGND,CH1TOGND,CH2TOGND,CH3TOGND
CH0TOGND = 0x4000
CH1TOGND = 0x5000
CH2TOGND = 0x6000
CH3TOGND = 0x7000
#Dictionaries
global FSR_TABLE,CH_TABLE
FSR_TABLE = {0.256:FSR2 ,0.512:FSR05 ,1.024:FSR1 ,2.048:FSR2 ,4.096:FSR4 ,6.144:FSR6}
CH_TABLE = {0:CH0TOGND ,1:CH1TOGND ,2:CH2TOGND ,3:CH3TOGND}
#I2C Register address
#SA_DEFAULT = 0x48
I2C_ADDR_POINT_CONV = 0x00
I2C_ADDR_POINT_CONF = 0x01
I2C_ADDR_LOW_TH =0x02
I2C_ADDR_HI_TH = 0x03
#Config registser setting is '1 011 001 1 100 00011
I2C_CONF_SET = 0xf383 #ch3 , 4.096v



#In : common(ground) mode =1,no of ch,
def getAdc(ch):
  i2c = smbus.SMBus(1)
  if (userMODE == 1):
    value = eConv((I2C_CONF_SET&0x81ff)|userFSR|CH_TABLE[ch])
    #print("mode1-getAdc,ch =%i,Configuration=%x "%(ch,value))
    adc_busy2free()
    i2c.write_word_data(userSA,I2C_ADDR_POINT_CONF,value)
    #check busy bit15
    value = i2c.read_word_data(userSA,I2C_ADDR_POINT_CONF)
    adc_busy2free()
    #time.sleep(10e-3)
    result =(i2c.read_word_data(userSA,I2C_ADDR_POINT_CONV))
    return eConv(result)
  elif (userMODE ==3):
    print ("userMODE =3 , blanking")
  elif (userMODE ==2):
    print ("userMODE = 2, blanking")
  else:
    print ("Out of range , no definition")

#byte swap for little endian convertion of ARM
#In: Word
def eConv(value):
  result = ((value << 8) & 0xFF00) + (value >> 8)
  return int(result)

#In : slave address, mode =1(to common ground) or command(AN3)=3 ro diff(command AN1) =2,FSR,ch number
def adc_init(slaveAddr,mode,bandGapFSR,ch):
  global userSA,userFSR,userCH,userMODE
  print(ADC_DRV_VER)
  userSA  = slaveAddr
  userFSR = bandGapFSR
  userCH  = ch
  userMODE = mode
  print("userSA=%x ,userMODE=%x ,userFSR=%x "%(userSA,userMODE,userFSR))
  i2c = smbus.SMBus(1)
  addr = slaveAddr
  value = I2C_ADDR_POINT_CONF
  i2c.write_byte(addr,value)
  reg = I2C_ADDR_POINT_CONF

  if (mode == 1):
    value = eConv((I2C_CONF_SET&0x81ff)|bandGapFSR|ch)
    print("init:mode1, configuration = %x" %value)
    i2c.write_word_data(addr,reg,value)
    #print(hex(i2c.read_word_data(addr,reg)))
    time.sleep(1e-3)
  elif (mode ==3):
    print ("mode =3 , blanking")
  elif (mode ==2):
    print ("mode = 2, blanking")
  else:
    print ("Out of range(init) , no definition")

def adc_busy2free():
  i2c = smbus.SMBus(1)
  value = i2c.read_word_data(userSA,I2C_ADDR_POINT_CONF)
  result = eConv(value)
  while(((result >> 15) & 1 ) == 0):
    #print("Busy bit15 of configraluation reg =%x"%result)
    time.sleep(1e-3)
    result = eConv(i2c.read_word_data(userSA,I2C_ADDR_POINT_CONF))
  #print("Busy bit15 of configraluation reg =%x"%result)



