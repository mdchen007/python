import CONSTANT as C
import global_ as gl
import threading
import time
import RPi.GPIO as GPIO
from queue import Queue
from adcConvert import adcMonitor as ad
from lcdDisp import lcdDisplay as lcd
from keyConsole import keyCtl as k
from uart import uart as ua
#one wire for DS18b20 temperature sensor
from w1thermsensor import W1ThermSensor

MAIN_VER ="DVK-R0.15"
adcArray = []
chVolt = []
exitFlag = 0

p1_screen =[C.PAGE1TOPLEFT,C.PAGE1TOPRIGHT,C.PAGE1BOMLEFT,C.PAGE1BOMRIGHT]
p2_screen =[C.PAGE2TOPLEFT,C.PAGE2TOPRIGHT,C.PAGE2BOMLEFT,C.PAGE2BOMRIGHT]

def globalVar_config():
  gl.set_value('adcArray',[])
  gl.set_value('chVolt',[])
  gl.set_value('pwm_ser',[])
  gl.set_value('pwm_freq',b' ')
  gl.set_value('pwm_dur',b' ')

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
  lcd.hw_init()
  if (config ==lcd.C.LCD_P1 or config ==lcd.C.LCDALLPAGE):
    lcd.page_init(lcd.C.LCD_P1,p1_screen[0],p1_screen[1],p1_screen[2],p1_screen[3])
  if (config ==lcd.C.LCD_P2 or config ==lcd.C.LCDALLPAGE):
    lcd.page_init(lcd.C.LCD_P2,p2_screen[0],p2_screen[1],p2_screen[2],p2_screen[3])
  lcd.two_page_disp()

#callback function
def pagekey_func(callback):
    kq.put(k.C.KEYSTATE_PAGE)
    print ("falling edge detected on GPIO%s ,state =%s"%(C.PAGEKEY,k.C.KEYSTATE_PAGE))
    #callback()

#callback function
def exitkey_func(callback):
    print ("falling edge detected on GPIO%s ,state =%s"%(C.EXITKEY,k.C.KEYSTATE_EXIT))
    kq.put(k.C.KEYSTATE_EXIT)
    #callback()

# number of keys allocation, assign to hook callback with specific key
def keycallback_config():
  keyList = k.key_init(k.C.TWOKEYS)
  keyList[0][0]= C.PAGEKEY
  keyList[0][1]= pagekey_func
  keyList[1][0]= C.EXITKEY
  keyList[1][1]= exitkey_func
  return k.C.TWOKEYS,keyList

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter,pwm_ser,nok,keyList,kq):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.pwm_ser = pwm_ser
        self.kq =kq
        k.key_register(nok,keyList)
    def run(self):
        print("Starting to run :"+ self.name)
        adcMonitorTask(self.name, self.counter, 5,self.pwm_ser,self.kq)
        print("Exiting from run:"+ self.name)
    def stop(self):
        self.thread_stop = True
        print (" thread1-stop :%s" %self.thread_stop)

#Adc 4ch monitoring
def adcMonitorTask(threadName, delay, counter,pwm_ser,kq):
  global exitFlag
  while counter:
    if exitFlag:
      counter =1
    time.sleep(delay)
    print ("%s: counter=%s %s" % (threadName, counter,time.ctime(time.time())))
    adcMonitor()
    for ch in range (4):
      print("Volt of channel%s is :%05.3f"%(ch,chVolt[ch]))
    lcd.print_string(lcd.C.LCD_P1,(str(chVolt[3])[:5])+'v  ',3)
    lcd.print_string(lcd.C.LCD_P1,(str(chVolt[2])[:5])+'v  ',2)
    lcd.print_string(lcd.C.LCD_P1,(str(chVolt[1])[:5])+'v  ',1)
    lcd.print_string(lcd.C.LCD_P1,(str(chVolt[0])[:5])+'v  ',0)
    try :
      sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20,"041702b228ff")
      temperature = sensor.get_temperature()
      lcd.print_string(lcd.C.LCD_P2,(str(temperature)[:5]+'c'),0)
      lcd.print_string(lcd.C.LCD_P2,'CNTR:'+"{:0>3d}".format(counter),1)
      print("The temperature is %s celsius" % temperature)

      f_vaule,d_value = ua.uart_get(pwm_ser)
      lcd.print_string(lcd.C.LCD_P2,str(f_vaule)[2:7],2)
      lcd.print_string(lcd.C.LCD_P2,str(d_value)[2:6]+'%',3)
      print(f_vaule,d_value)

    except:
      print("Check GPIO-BCM4 which is pulled up or not")

    while not kq.empty():
      keystate = kq.get()
      print ("state-q %s"%keystate)
      if (keystate ==k.C.KEYSTATE_PAGE):
        lcd.disp_page_slide(lcd.C.LCD_P2,lcd.LCD_PAGE_TOG)
        counter = 200
      elif (keystate ==k.C.KEYSTATE_EXIT):
        pass
        exitFlag =1
    counter -= 1



#One wire DS I/F initialiation for ds18b20
def ds18b20_init():
  GPIO.setup(C.TEMP_GPIO,GPIO.IN,GPIO.PUD_UP)
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

#adc channel init
def adc_chan_init():
  result =ad.adc_init(ad.C.ADC_DEVICE1,ad.C.COMMONGND,ad.C.V4096,ad.C.CH3)
  #adcA_=gl.get_value('adcArray')
  #chV_=gl.get_value('chVolt')
  if result ==False:
    return False
  else :
    for i in range (4):
      #adcA_.append(i)
      #chV_.append(i)
      adcArray.append(i)
      chVolt.append(i)
    #get each channel value and convert to voltage
    for ch in range (4):
      #chV_[ch] = volConv(ad.getChVal(ch))
      chVolt[ch] = volConv(ad.getChVal(ch))
      print("Volt of channel%s is :%05.3f"%(ch,chVolt[ch]))

#####main function declare#####
def main():
  print(MAIN_VER)
  gl._init()
  globalVar_config()

  #hook callback function for key event
  global kq
  kq = Queue()
  nok,keyList = keycallback_config()
  #adc channel init
  adc_chan_init()

  #temperature sensor DS18B20 init
  ds18b20_init()
  #UART init
  pwm_ser,pwm_freq,pwm_dur = ua.uart_init(ua.PWM_DEVICE)
  print("main :f_value=%s d_value=%s"%(pwm_freq,pwm_dur))
  #LCD display init
  disp_init(lcd.C.LCDALLPAGE)

  #thread init
  thread1 = myThread(1, "Threading-1", 3,pwm_ser,nok,keyList,kq)
  print (" thread1 :%s" %thread1)
  try:
    thread1.start()
  except:
    print("Error: unable to start thread")
  thread1.join()

#####Entry point here #####
if __name__ == '__main__':
  main()
