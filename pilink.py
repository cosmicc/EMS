#!/usr/bin/python

import smbus
import time
import sys

bus = smbus.SMBus(1)
dataext = " ".join(sys.argv[1:])

# This is the address we setup in the Arduino Program
address = 0x75

def sendval(value1, value2):
 bdata = bytearray()
 bdata.extend(value2)
 cbdata=[bdata[0]]
 for ibdata in range (1, len(bdata)):
   cbdata=cbdata+[bdata[ibdata]]
 bus.write_block_data(address, value1, cbdata)
 return -1

if len(dataext) < 21:
 sendval(99,dataext)
else:
 print "Error: String too long."

#print "Sent: "+dataext

# sleep one second
time.sleep(1)

