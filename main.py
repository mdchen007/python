import threading
import _thread
import time
from adcConvert import adcMonitor as ad
from lcdDisp import lcdDisplay as lcd
MAIN_VER ="MAIN-R0.5"
global adcArray,adc2Voltage
adcArray = []
chVolt = []
exitFlag = 0

def volConv(value):
  volt = 4.096*((float(value)/float(0x7fff)))
  return volt

def adcMonitor():
  for ch in range(4):
    adcArray[ch] = ad.getChVal(ch)
    chVolt[ch] = volConv(adcArray[ch])

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name, self.counter, 5)
        print ("退出线程：" + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        adcMonitor()
        lcd.print_string((str(chVolt[3])[:5]),3)
        lcd.print_string((str(chVolt[2])[:5]),2)
        counter -= 1

#####Entry point here
#if __name__ == '__main__':
print(MAIN_VER)

#array init
for i in range (4):
  adcArray.append(i)
  chVolt.append(i)
for ch in range (4):
  chVolt[ch] = volConv(ad.getChVal(ch))
  print("Volt of channel%s is :%05.3f"%(ch,chVolt[ch]))

thread1 = myThread(1, "Threading-1", 3)

lcd.page_init(1,'PV(5V)','RPI3.3V',(str(chVolt[2])[:5])+'v',(str(chVolt[3])[:5])+'v')
lcd.page_init(2,'CH1','CH0',(str(chVolt[1])[:5])+'v',(str(chVolt[0])[:5])+'v')
lcd.two_page_disp()

thread1.start()
thread1.join()

#try:
#  _thread.start_new_thread( _print_time, ("Thread-1", 2, ) )
#except:
#   print ("Error: unable to start thread")

#while 1:
#  pass
  #adcMonitor()

