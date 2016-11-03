#!/usr/bin/python

import smbus
import time
import sys
import subprocess

bus = smbus.SMBus(1)

address = 0x75

def sendval(value1, value2):
 bdata = bytearray()
 bdata.extend(value2)
 cbdata=[bdata[0]]
 for ibdata in range (1, len(bdata)):
   cbdata=cbdata+[bdata[ibdata]]
 bus.write_block_data(address, value1, cbdata)
 return -1

subprocess.call("service statusbar stop")
subprocess.call("service ems_server stop")

sendval(99,"499+")
