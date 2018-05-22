#HD44780 footprint
vss = 1 #ground
vdd = 2 #5volt.
v0 = 3
rs = 4 #send a command (0) , updating the display (1) over dbx pins
rw = 5 #read (1)/write (0)
en = 6 #enable pin, hi=enable , low=disable. (w/ 10uf cap in the enternal is perfer.)
db0 = 7 #for 8bit command only
db1 = 8 #for 8bit command only
db2 = 9 #for 8bit command only
db3 = 10 #for 8bit command only
db4 = 11 #for 4bit/8bit command
db5 = 12 #for 4bit/8bit command
db6 = 13 #for 4bit/8bit command
db7 = 14 #for 4bit/8bit command
ledp = 15 #LED+
ledm = 16 #LED-

#MCU whick pins is used and mapping to
