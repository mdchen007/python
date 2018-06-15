import threading
import time
import RPi.GPIO as GPIO
from adcConvert import adcMonitor as ad
from lcdDisp import lcdDisplay as lcd
from keyConsole import keyCtl as k

#one wire for DS18b20 temperature sensor
from w1thermsensor import W1ThermSensor

#for BLE fucntion using bluepy
from bluepy.bluepy.btle import Scanner, DefaultDelegate, BTLEException,Peripheral

MAIN_VER ="MAIN-R0.11"
global adcArray,adc2Voltage
adcArray = []
chVolt = []
exitFlag = 0
PAGEKEY =17
EXITKEY =23
PAGE1TOPLEFT ='PV(5V)'
PAGE1TOPRIGHT ='RPI3.3V'
PAGE2TOPLEFT ='Temp(C)'
PAGE2TOPRIGHT ='CH0'
LCDPAGE1=1
LCDPAGE2=2
TEMP_GPIO = 4

loc_naming =[PAGE1TOPLEFT,PAGE1TOPRIGHT,PAGE2TOPLEFT,PAGE2TOPRIGHT]

def volConv(value):
  volt = 4.096*((float(value)/float(0x7fff)))
  return volt

#4 adc channel monitoring , it uses adcarray to store all of value from each adc convertor.
#Then value transfer to voltage base that bandgap is choose 4.069v.
def adcMonitor():
  for ch in range(4):
    adcArray[ch] = ad.getChVal(ch)
    chVolt[ch] = volConv(adcArray[ch])

#config =1 means page1 init, =2 means page2 init , =3 means both init
def disp_init(config):
  if (config ==1 or config ==3):
    lcd.page_init(lcd.LCD_P1,loc_naming[0],loc_naming[1],(str(chVolt[2])[:5])+'v',(str(chVolt[3])[:5])+'v')
  if (config ==2 or config ==3):
    lcd.page_init(lcd.LCD_P2,loc_naming[2],loc_naming[3],(str(chVolt[1])[:5])+'C',(str(chVolt[0])[:5])+'v')

#callback function
def pagekey_func(callback):
    k.keystate = 1
    k.kq.put(k.keystate)
    print ("falling edge detected on GPIO17 ,state =%s"%k.keystate)
    #callback()

#callback function
def exitkey_func(callback):
    k.keystate =2
    print ("falling edge detected on GPIO23 , state =%s"%k.keystate)
    k.kq.put(k.keystate)
    #callback()

# assign to hook callback with specific key
def keycallback_config():
  k.keyList[0][0]= PAGEKEY
  k.keyList[0][1]= pagekey_func
  k.keyList[1][0]= EXITKEY
  k.keyList[1][1]= exitkey_func

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        k.key_cb_enable(2,k.keyList)
    def run(self):
        print("Starting to run :"+ self.name)
        adcMonitorTask(self.name, self.counter, 5)
        print("Exiting from run:"+ self.name)
    def stop(self):
        self.thread_stop = True
        print (" thread1-stop :%s" %self.thread_stop)

#Adc 4ch monitoring
def adcMonitorTask(threadName, delay, counter):
  global exitFlag
  while counter:
    if exitFlag:
      counter =1
    time.sleep(delay)
    print ("%s: counter=%s %s" % (threadName, counter,time.ctime(time.time())))
    adcMonitor()
    for ch in range (4):
      print("Volt of channel%s is :%05.3f"%(ch,chVolt[ch]))
    lcd.print_string(lcd.LCD_P1,(str(chVolt[3])[:5]),3)
    lcd.print_string(lcd.LCD_P1,(str(chVolt[2])[:5]),2)
    lcd.print_string(lcd.LCD_P2,(str(chVolt[1])[:5]),3)
    #lcd.print_string(lcd.LCD_P2,(str(chVolt[0])[:5]),2)
    try :
      temperature = sensor.get_temperature()
      temperature =24
      lcd.print_string(lcd.LCD_P2,(str(temperature)[:5]),2)
      lcd.print_string(lcd.LCD_NOW_PAGE,'CNTR:'+"{:0>3d}".format(counter),1)
     # print("The temperature is %s celsius" % temperature)
      print("No exception")
    except:
      print("Check GPIO-BCM4 which is pulled up or not")

    while not k.kq.empty():
      keystate = k.kq.get()
      print ("state-q %s"%k.keystate)
      if (k.keystate ==1):
        lcd.disp_page_slide(lcd.LCD_P2,lcd.LCD_PAGE_TOG)
        counter = 200
      elif (k.keystate ==2):
        pass
        exitFlag =1
    counter -= 1

### define for BLE portion
# Scan Delegate...
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

### BLE function
def ble_init():
  print ('Scanning...')
  scanner = Scanner().withDelegate(ScanDelegate())
  devices = scanner.scan(10.0)
  for dev in devices:
    print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi) )
    for (adtype, desc, value) in dev.getScanData():
        print ("  %s = %s" % (desc, value))
  print ('Querying...')
  try:
    p = Peripheral("DB:4C:AF:AB:A7:EC", "random",0)
  except:
    print("Check device on or does it throw an BTLEException exception from BLE constructor? ")

  try:
    c = p.getCharacteristics(uuid="BD6664C8941DCBA806E1AA75F7D44BAC")[0]
    #c = p.getCharacteristics(uuid="1814")[0]
  except:
    print("getCharacteristics Error")
  #print (c.read())

#####main function here
def main():
  print(MAIN_VER)
  #hook callback function for key event
  keycallback_config()
  #array init for ADC sample and hold
  for i in range (4):
    adcArray.append(i)
    chVolt.append(i)
  #get each channel value and convert to voltage
  for ch in range (4):
    chVolt[ch] = volConv(ad.getChVal(ch))
    print("Volt of channel%s is :%05.3f"%(ch,chVolt[ch]))

  #BLE portion
  #ble_init()

  #temperature sensor DS18B20 init
  GPIO.setup(TEMP_GPIO,GPIO.IN,GPIO.PUD_UP)
  sensor_temp_init =0
  counter =10
  while( not sensor_temp_init or counter !=0 ):
    try :
      sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20,"041702b228ff")
      temperature = sensor.get_temperature()
      print("The temperature is %s celsius" % temperature)
      sensor_temp_init=1
      counter =0
    except:
      print("Check pin-BCM4 that is pulled up or not, waiting for a minutes ,%s" %counter)
      time.sleep(1)
      counter-= 1

  #LCD display init
  disp_init(3)
  lcd.two_page_disp()

  #thread init
  thread1 = myThread(1, "Threading-1", 3)
  print (" thread1 :%s" %thread1)
  try:
    thread1.start()
  except:
    print("Error: unable to start thread")
  thread1.join()

#####Entry point here
if __name__ == '__main__':
  main()
