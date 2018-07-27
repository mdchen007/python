### Constant definition
print("import _CONSTANT.py module from lcdDisp package")
LCD_P1 =1
LCD_P2 =2
LCDALLPAGE=3
NC =0
DVK512 =True
if DVK512 == True:
  RS = 22
  RW = NC
  EN = 11
  D4 = 23
  D5 = 10
  D6 = 9
  D7 = 25
else :
  RS = 12
  RW = 13
  EN = 11
  D4 = 7
  D5 = 8
  D6 = 9
  D7 = 10
  NC = 0
