# -*- coding: utf-8 -*-
import serial
import time 

ser = serial.Serial(
        port ='/dev/ttyS0',
        baudrate =9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS)
    
#test_string ="D020".encode('utf-8')
try:
        ser.write(b'D023')
        state = ser.readline()
        print("Duty :%s"%state)
        time.sleep(0.1)
        ser.write(b'F10.5')
        state =ser.readline()
        print("Frequency:%s"%state)        
        #ser.write(b'0')
        #ser.write(b'2')
        #ser.write(b'0')
        #state =ser.readline()
        #print("%s"%state)
except:
    ser.close()
    print("Error")
