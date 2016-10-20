#!/usr/bin/python

import socket
import SocketServer
import sys
import fcntl
import struct

ipport = 15435

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
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    ip = get_ip_address('eth0')
    server_address=(ip,ipport)
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((ip, ipport), MyTCPHandler)

    print >>sys.stderr, 'starting up on %s port %s' % server_address

    server.serve_forever()









try:
    #create an AF_INET, STREAM socket (TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
 
server_address = (ip, 15435)

try:
    sock.bind(server_address)
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.listen(1)

while True:
    print >>sys.stderr, 'waiting for a connection...'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'client connected:', client_addressi
        while True:
            data = connection.recv(16)
            

            print >>sys.stderr, 'received "%s"' % data
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()

