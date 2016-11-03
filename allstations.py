#!/usr/bin/python

import subprocess

def run_command(command):
 p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
 return iter(p.stdout.readline, b'')

def activestations():
 sta = []
 command = '/opt/EMS/allstations.sh'.split()
 for line in run_command(command):
  junk,inst=line.split("=")
  inst=inst.rstrip('\n')
  sta.append(inst)
 return sta


#sta=activestations()
#for i in sta:
# print i

#print len(sta)
