#!/usr/bin/python

import sys, os, signal, time, datetime, socket, SocketServer, fcntl, struct, MySQLdb

tcpport = 15435
deviceid = 'EMS.d1data'

# Open Database

db = MySQLdb.connect(host = "localhost", user = "root", passwd = "EMS16", db = "EMS")
cur = db.cursor()

# SIGINT Catch
def signal_handler(signal, frame):
        print('Exiting.')
	cur.close()
	db.close()
        sys.exit(0)


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
        self.data = self.request.recv(1024).strip()
        print "Received from {}: ".format(self.client_address[0])+self.data
        now = datetime.datetime.now()

        try:
             cur.execute("""INSERT INTO %s(timestamp,temp,humidity,lux,co2,pressure) VALUES(%s,%s,%s,%s,%s,%s)""",(deviceid,now,temp,humi,lux,co2,pres))
             db.commit()
        except:
             db.rollback()

	# just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    ip = get_ip_address('eth0')
    server_address=(ip,tcpport)
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((ip, tcpport), MyTCPHandler)

    print >>sys.stderr, 'starting up on %s port %s' % server_address

    server.serve_forever()

