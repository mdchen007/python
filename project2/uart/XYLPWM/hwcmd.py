
#It is a XY-LPWM module thru uart controlling/setting
import serial
import time

def xy_lpwm_init():
  ser = serial.Serial(
  port ='/dev/ttyS0',
  baudrate =9600,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS)
  return ser

def xy_lpwm_set(ser,freq,duty):
    try:
        time.sleep(0.1)
        ser.write(duty)
        state = ser.readline()
        print("Duty state :%s"%state)
        time.sleep(0.1)
        ser.write(freq)
        state =ser.readline()
        print("Frequency state : %s"%state)
    except:
        ser.close()
        print("Set error")

def xy_lpwm_get(ser):
    try:
        time.sleep(0.1)
        ser.write(b'read')
        setting=ser.readline()
        return setting
        print(setting)
    except:
        ser.close()
        print("Get error")