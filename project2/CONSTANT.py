### Constant definition
print("import CONSTANT.py module")
#__all__ =['PAGE1TOPLEFT','PAGE1TOPRIGHT','PAGE2TOPLEFT','PAGE2TOPRIGHT']

DVK512 =True
NC =0
KEY0 =5
KEY1 =6
KEY2 =13
KEY3 =19

if DVK512 ==True:
  PAGEKEY = KEY0
  EXITKEY = KEY1
else:
  PAGEKEY = 17
  EXITKEY = 23
PAGE1TOPLEFT ='CH0 vol'
PAGE1TOPRIGHT ='CH1 vol'
PAGE1BOMLEFT ='CH2 vol'
PAGE1BOMRIGHT ='CH3 vOl'
PAGE2TOPLEFT ='Temp'
PAGE2TOPRIGHT ='Counter'
PAGE2BOMLEFT ='Freq'
PAGE2BOMRIGHT ='Duty'
TEMP_GPIO = 4
BLE1_MAC_ADDR ="DB:4C:AF:AB:A7:EC"

