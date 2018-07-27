#ADS1115 16bit AD converter
if __name__ == '__main__':
  import _CONSTANT as C
  from ADS1115 import hwcmd as h
else:
  from . import _CONSTANT as C
  from .ADS1115 import hwcmd as h

def getChVal(ch):
  return(h.getAdc(ch))

def adc_init(device_addr,mode,gain,ch):
  return h.adc_init(device_addr,mode,h.FSR_TABLE[gain],h.CH_TABLE[ch])

def main():
  h.adc_init(C.ADC_DEVICE1,C.COMMONGND,h.FSR_TABLE[C.V4096],h.CH_TABLE[C.CH3])

#####Entry point here #####
if __name__ == '__main__':
  main()




