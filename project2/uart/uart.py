# -*- coding: utf-8 -*-
import serial
import time
if __name__ == '__main__':
  from XYLPWM import hwcmd as h
else:
  from uart.XYLPWM import hwcmd as h
UART_VER = "UART-R0.01"
PWM_DEVICE = "XY-LPWM"

#uart init
#in : device name, out : ser id , frequency , duration
def uart_init(device):
    if device == PWM_DEVICE:
      ser=h.xy_lpwm_init()
      if ser != 0:
        uart_set(ser,b'F12.6',b'D019')
        f_value,d_value=uart_get(ser)
        print("f_value=%s d_value=%s"%(f_value,d_value))
        return ser,f_value,d_value
      else:
        print("failed to init UART for %"%PWM_DEVICE)
        return 0,-1,-1
    else:
      print("It is a TO BE Define device")
      return 0,-1,-1

def uart_set(ser,set_f,set_d):
  h.xy_lpwm_set(ser,set_f,set_d)

def uart_get(ser):
  f_value=h.xy_lpwm_get(ser)
  d_value=h.xy_lpwm_get(ser)
  return f_value,d_value

def main():
    print(UART_VER)
    ser = h.xy_lpwm_init()
    uart_set(ser,b'F55.5',b'D055')
    value1=uart_get(ser)
    value2=uart_get(ser)
    print("my55.5value1=%s value2=%s"%(value1,value2))
    time.sleep(2)
    uart_set(ser,b'F66.6',b'D066')
    value1=h.xy_lpwm_get(ser)    
    value2=h.xy_lpwm_get(ser)
    print("my66.6value1=%s value2=%s"%(value1,value2))
    time.sleep(2)
#####Entry point here #####
if __name__ == '__main__':
  main()
