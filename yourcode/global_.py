# -*- coding: utf-8 -*-
print("import Global.py module")
def _init():
  global _global_dict
  _global_dict ={}
def set_value(name,value):
  _global_dict[name]=value
def get_value(name,defValue=None):
  try:
    return _global_dict[name]
  except KeyError:
    return defValue

### Global variable definintion
#__all__ =["adcArray,adc2Voltage,pwm_ser,pwm_freq,pwm_dur"]
global adcArray,adc2Voltage,pwm_ser,pwm_freq,pwm_dur
adcArray = []
chVolt = []


