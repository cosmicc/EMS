#!/usr/bin/python

import sys, os, os.path, signal, time, datetime, socket, SocketServer, fcntl, struct, MySQLdb, rrdtool, daemon, smbus, argparse
from config import Config

pidfile = '/var/lock/ems_server'

try:
 cfg = Config('/opt/EMS/ems.conf')
except:
 print "No config file found. Exiting."
 sys.exit()

version = cfg.version
eth = cfg.eth
tcpport = int(cfg.tcpport)
address = int(cfg.address, 16)

parser = argparse.ArgumentParser(description='Environmental Managmeant System Server Application')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
parser.add_argument('-d', action='store_true', default=False, help='Run as Daemon')
parser.add_argument('--version', action='version', version='Environmental Managmeant System '+version)

args = parser.parse_args()

def main_program():
 if args.d == True:
  sys.stdout = open('/var/log/ems_server.log', 'w')
  sys.stderr = open('/var/log/ems_server.log', 'w')

 if os.path.isfile(pidfile):
  pidf = open(pidfile, "r")
  pid = pidf.read()
  pidf.close()
  print "EMS Server already running pid "+str(pid)+". Exiting."
  sys.exit()
 else:
  pid = os.getpid()
  pidf = open(pidfile, "w")
  print "Locking process pid "+str(pid)
  pidf.write(str(pid))
  pidf.close()

 db = MySQLdb.connect(host = "localhost", user = "root", passwd = "EMS16", db = "EMS")
 cur = db.cursor()
 bus = smbus.SMBus(1)
 
# SIGINT Catch
 def signal_handler(signal, frame):
  pilink("22+")
  print "SIGNINT Exiting."
  cur.close()
  if db.open:
   db.close()
  if os.path.isfile(pidfile):
   print "Removing proccess lock."
   os.remove(pidfile)
  sys.exit(0)

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

# Determine IP
 def get_ip_address(ifname):
     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     return socket.inet_ntoa(fcntl.ioctl(
         s.fileno(),
         0x8915,  # SIOCGIFADDR
         struct.pack('256s', ifname[:15])
     )[20:24])

 class MyTCPHandler(SocketServer.BaseRequestHandler):
     def handle(self):
         # self.request is the TCP socket connected to the client
         self.data = self.request.recv(50).strip()
         now = datetime.datetime.now()
         sdata = [x for x in self.data.split("#")]
         pilink("499+")
         print "Received from "+format(self.client_address[0])+" (Device "+sdata[0]+"): "+self.data
         if sdata[0] == '1':
          try:
           cur.execute("""INSERT INTO EMS.d1data(timestamp,temp,humidity,lux,co2,pressure) VALUES(%s,%s,%s,%s,%s,%s)""",(now,sdata[1],sdata[2],sdata[3],sdata[4],sdata[5]))
           db.commit()
          except:
           print "Database Error."
           db.rollback()
          ret = rrdtool.update('/opt/rrddata/d1temp.rrd', 'N:%s' %(sdata[1]))
          if ret:
           print rrdtool.error()

         elif sdata[0] == '2':
          try:
           cur.execute("""INSERT INTO EMS.d2data(timestamp,temp,humidity,lux,co2,pressure) VALUES(%s,%s,%s,%s,%s,%s)""",(now,sdata[1],sdata[2],sdata[3],sdata[4],sdata[5]))
           db.commit()
          except:
           print "Database Error."
           db.rollback()
         elif sdata[0] == '3':
          try:
           cur.execute("""INSERT INTO EMS.d3data(timestamp,temp,humidity,lux,co2,pressure) VALUES(%s,%s,%s,%s,%s,%s)""",(now,sdata[1],sdata[2],sdata[3],sdata[4],sdata[5]))
           db.commit()
          except:
           print "Database Error."
           db.rollback()
         elif sdata[0] == '4':
          try:
           cur.execute("""INSERT INTO EMS.d4data(timestamp,temp,humidity,lux,co2,pressure) VALUES(%s,%s,%s,%s,%s,%s)""",(now,sdata[1],sdata[2],sdata[3],sdata[4],sdata[5]))
           db.commit()
          except:
           print "Database Error."
           db.rollback()

        # just send back the same data, but upper-cased
         self.request.sendall(self.data.upper())

 try:
  signal.signal(signal.SIGINT, signal_handler)
  if not os.path.isfile('/opt/rrddata/d1temp.rrd'):
   rrdtool.create(
    "/opt/rrddata/d1temp.rrd",
    "--start", "now",
    "--step", "300",
    "DS:temp:GAUGE:600:0:38",
    "RRA:AVERAGE:0.5:1:12",
    "RRA:AVERAGE:0.5:1:288",
    "RRA:AVERAGE:0.5:12:168",
    "RRA:AVERAGE:0.5:12:720",
    "RRA:AVERAGE:0.5:288:365")

  ip = get_ip_address(eth)
  server_address=(ip,tcpport)
  # Create the server, binding to localhost on port 9999
  server = SocketServer.TCPServer((ip, tcpport), MyTCPHandler)
  if not os.path.isfile('/run/lock/statusbar'):
   pilink("100EMS Server "+version+"+") 
  pilink("101"+ip+"+")
  time.sleep(10)
  print "Starting up on "+eth+" "+ip+":"+str(tcpport)
  pilink("23+")
  server.serve_forever()
 except KeyboardInterrupt:
  print('CTRL-C Exiting.')
  pilink("22+")
  cur.close()
  if db.open:
   db.close()
  if os.path.isfile(pidfile):
   print "Removing proccess lock."
   os.remove(pidfile)
  sys.exit(0)
  raise
 finally:
  print('Exiting.')
  pilink("22+")
  cur.close()
  if db.open:
   db.close()
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

