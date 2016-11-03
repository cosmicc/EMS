#!/usr/bin/python

import sys, os, os.path, math, signal, socket, fcntl, struct, time, datetime, MySQLdb, daemon, smbus, psutil, argparse, subprocess, RPi.GPIO as GPIO
from config import Config

try:
 cfg = Config('/opt/EMS/ems.conf')
except:
 print "No config file found. Exiting."
 sys.exit()

version = cfg.version
eth = cfg.mon
address = int(cfg.address, 16)
loopdelay = cfg.loopdelay
startupdelay = cfg.startupdelay

pidfile = '/var/lock/statusbar'

parser = argparse.ArgumentParser(description='Environmental Managmeant System Statusbar Application')
parser.add_argument('-d', action='store_true', default=False, help='Run as Daemon')
parser.add_argument('--version', action='version', version='Environmental Managmeant System Statusbar')

args = parser.parse_args()

def main_program():
 if args.d == True:
  sys.stdout = open('/var/log/statusbar.log', 'w')
  sys.stderr = open('/var/log/statusbar.log', 'w')
 
 if os.path.isfile(pidfile):
  pidf = open(pidfile, "r")
  pid = pidf.read()
  pidf.close()
  print "Statusbar already running pid "+str(pid)+". Exiting."
  sys.exit()
 else:
  pid = os.getpid()
  pidf = open(pidfile, "w")
  print "Locking process pid "+str(pid)
  pidf.write(str(pid))
  pidf.close()
 
# SIGINT Catch
 def signal_handler(signal, frame):
  pilink("11red+")
  pilink("399+")
  print "SIGNINT Exiting."
  if os.path.isfile(pidfile):
   print "Removing proccess lock."
   os.remove(pidfile)
  sys.exit(0)

 time.sleep(startupdelay)
 bus = smbus.SMBus(1)
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
 GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)

 def pilink(value1):
  bdata = bytearray()
  bdata.extend(value1)
  cbdata=[bdata[0]]
  for ibdata in range (1, len(bdata)):
    cbdata=cbdata+[bdata[ibdata]]
  try:
   bus.write_block_data(address, 99, cbdata)
  except:
   print "Error communicating with i2c interface."
  return -1

 def rstButton(channel):
  print("Reset Button pressed!")

 pilink("300S1  S2  S3  S4  +")

 GPIO.add_event_detect(24, GPIO.RISING, callback=rstButton, bouncetime=2000)
 global lcdstate
 lcdstate = 1

 def run_command(command):
  p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  return iter(p.stdout.readline, b'')
  p.kill()

 def activestations():
  sta = []
  command = '/opt/EMS/allstations.sh'.split()
  for line in run_command(command):
   junk,inst=line.split("=")
   inst=inst.rstrip('\n')
   sta.append(inst)
  #p.kill()
  if len(sta) == 0:
   pilink("3010 Wifi Connected+")
   pilink("11green+")
  else:
   pilink("301"+str(len(sta))+" Wifi Connected+")
   pilink("10green+")
  #return len(sta)

 def showip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915, struct.pack('256s', eth[:15]))[20:24])
  pilink("301"+ip+"+")

 def showtime():
  now = datetime.datetime.now()
  nowstr = str(now.month)+"-"+str(now.day)+"-"+str(now.year)+" "+str(now.hour)+":"+str(now.minute)
  #print nowstr
  pilink("301"+nowstr+"+")

 def showrss():
  cpu=psutil.cpu_percent(interval=1)
  mem=psutil.virtual_memory()
  disk=psutil.disk_usage('/')
  cpud = int(round(cpu,0))
  memd = int(round(mem.percent,0))
  dskd = int(round(disk.percent,0))
  #print ("101C"+str(cpud)+"% M"+str(memd)+"% D"+str(dskd)+"%+")
  pilink("301C"+str(cpud)+"% M"+str(memd)+"% D"+str(dskd)+"%+")

 def showlast():
  last = checklast()
  #print ("101"+str(last)+"+")
  pilink("301"+str(last)+"+")
 
 def lcdButton(channel):
  global ispushed
  ispushed=True
  if args.d == False:
   print("LCD Button pressed")
  global lcdstate
  if (lcdstate == 5):
   lcdstate = 0
  lcdstate=lcdstate+1
  if (lcdstate == 1):
   activestations()
  elif (lcdstate == 2):
   showlast()
  elif (lcdstate == 3):
   showrss()
  elif (lcdstate == 4):
   showtime()
  elif (lcdstate == 5):
   showip()
  ispushed=False

 GPIO.add_event_detect(23, GPIO.RISING, callback=lcdButton, bouncetime=1000)

 def checklast(): 
  db = MySQLdb.connect(host = "localhost", user = "root", passwd = "EMS16", db = "EMS")
  cur = db.cursor()
  lastd1 = 0
  lastd2 = 0
  lastd3 = 0
  lastd4 = 0
  lastcount = 0
  now = datetime.datetime.now()
  cur.execute("SELECT timestamp FROM d1data ORDER BY timestamp DESC LIMIT 1")
  tstamp = cur.fetchone()
  if tstamp is not None:
   lastd1 = tstamp   
   if (now - tstamp[0]) < datetime.timedelta(0,180):
    pilink("511+")
    pilink("20green+")
   else:
    pilink("510+")
    lastcount = lastcount + 1
  else:
   pilink("510+")
   lastcount = lastcount + 1
  cur.execute("SELECT timestamp FROM d2data ORDER BY timestamp DESC LIMIT 1")
  tstamp = cur.fetchone()
  if tstamp is not None:
   lastd2 = tstamp
   if (now - tstamp[0]) < datetime.timedelta(0,180):
    pilink("521+")
    pilink("20green+")
   else:
    pilink("520+")
    lastcount = lastcount + 1
  else:
   pilink("520+")
   lastcount = lastcount + 1
  cur.execute("SELECT timestamp FROM d3data ORDER BY timestamp DESC LIMIT 1")
  tstamp = cur.fetchone()
  if tstamp is not None:
   lastd3 = tstamp
   if (now - tstamp[0]) < datetime.timedelta(0,180):
    pilink("531+")
    pilink("20green+")
   else:
    pilink("530+")
    lastcount = lastcount + 1
  else:
   pilink("530+")
   lastcount = lastcount + 1
  cur.execute("SELECT timestamp FROM d4data ORDER BY timestamp DESC LIMIT 1")
  tstamp = cur.fetchone()
  if tstamp is not None:
   lastd4 = tstamp
   if (now - tstamp[0]) < datetime.timedelta(0,180):
    pilink("541+")
    pilink("20green+")
   else:
    pilink("540+")
    lastcount = lastcount + 1
  else:
   pilink("540+")
   lastcount = lastcount + 1
  if os.path.isfile(pidfile):
   pidf = open(pidfile, "r")
   pid = pidf.read()
   pidf.close()
   if not os.path.isdir("/proc/"+str(pid)):
    pilink("21red+")
   else:
    if (lastcount == 4):
     pilink("21green+")
    else: 
     pilink("20green+")
  else:
   pilink("21red+") 
  mylist = [lastd1, lastd2, lastd3, lastd4]
  latest = max(mylist)
  try:
   seconds = (now - latest[0]).seconds
   minutes = seconds / 60
   hours = seconds / 3600
   days = seconds / 86400
   if (hours > 24):
    hours = hours-days*24
    last = str(days)+" Days "+str(hours)+" Hrs"
   elif (minutes > 60):
    minutes = minutes-hours*60
    last = str(hours)+" Hrs "+str(minutes)+" Min"
   elif (seconds > 60):
    seconds = seconds-(minutes*60)
    last = str(minutes)+" Min "+str(seconds)+" Sec"
   else:
    last = str(seconds)+" Seconds ago"
   cur.close()
   db.close()
   return last
  except:
   print "No Data."

 global ispushed
 ispushed = False 
 try: 
  while True:
   if args.d == False:
    start = time.time() 
   checklast()
   if args.d == False:
    print "LCD Sreen State: #"+str(lcdstate)
   if ispushed == False:
    if (lcdstate == 1):
     activestations()
    elif (lcdstate == 2):
     showlast()
    elif (lcdstate == 3):
     showrss()
    elif (lcdstate == 4):
     showtime()
    elif (lcdstate == 5):
     showip()
   if args.d == False:
    end = time.time()
    extime = (end - start)
    millis = int(round(extime * 1000))
    print "Execution Time: "+str(millis)+"ms"
   time.sleep(loopdelay)
 except KeyboardInterrupt:
  print('CTRL-C Exiting.')
  if os.path.isfile(pidfile):
   print "Removing proccess lock."
   os.remove(pidfile)
  sys.exit(0)
  raise
 finally:
  print('Exiting.')
  if os.path.isfile(pidfile):
   print "Removing proccess lock."
   os.remove(pidfile)
  sys.exit(0)

def daemon_run():
    with daemon.DaemonContext():
         main_program()

if __name__ == "__main__":
    if args.d == False:
     main_program()
    else:
     daemon_run()
