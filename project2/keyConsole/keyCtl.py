
import RPi.GPIO as GPIO
import time
if __name__ == '__main__':
  import _CONSTANT as C
  from HD44780 import hwcmd as h
else :
  from . import _CONSTANT as C
  from .KEYCTL import hwcmd as h
#from queue import Queue

#global kq
#keystate =C.KEYSTATE_DEF
#kq = Queue()

def key_register(nop,keyList):
  keystate = C.KEYSTATE_REG
  h.key_init(nop,keyList)

#return keyList
def key_init(nop):
  keystate =C.KEYSTATE_DEF
  keyList = [[0 for x in range(nop)] for y in range(C.KEYCOLUMN)]
  return keyList

### code entry point
if __name__ == "__main__":
    print("keyCtl.py is being run directly")
else:
    print("keyCtl is being imported into another module")





