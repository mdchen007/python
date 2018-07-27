#import threading
#import _thread
#import time
#import RPi.GPIO as GPIO
#from adcConvert import adcMonitor as ad
#from lcdDisp import lcdDisplay as lcd
#from keyConsole import keyCtl as k
##one wire for DS18b20 temperature sensor
#from w1thermsensor import W1ThermSensor
##for BLE fucntion using bluepy
from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate, BTLEException

MAIN_VER ="MAIN-R0.9"

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

#####Entry point here
if __name__ == '__main__':
  print(MAIN_VER)


#BLE portion
print ('Scanning...')
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
for dev in devices:
    print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi) )
    for (adtype, desc, value) in dev.getScanData():
        print ("  %s = %s" % (desc, value))

