#!/usr/bin/python

import sys, os, signal, MySQLdb, rrdtool


# Open Database
db = MySQLdb.connect(host = "localhost", user = "root", passwd = "EMS16", db = "EMS")
cur = db.cursor()

# SIGINT Catch
def signal_handler(signal, frame):
        print('Exiting.')
	cur.close()
	db.close()
        sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    cur.execute('select timestamp, temp from d1data');
    rows = cur.fetchall()
    
