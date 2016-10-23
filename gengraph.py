#!/usr/bin/python

import sys, os, os.path, signal, MySQLdb, rrdtool

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

    period = '10m'
    rrdtool.graph( "/var/www/html/d1temp.jpg", "--start", "-%s" %(period),
     "--full-size-mode",
     "--alt-autoscale",
     "--width=700 --height=400",
     "--vertical-label", "Temperature (C)",
     "--slope-mode",
     "--color=SHADEB#9999CC",
     "--watermark='Device 1 Temperature'",
     "DEF:temp=/opt/rrddata/d1temp.rrd:temp:MAX",
     "LINE2:temp#00FF00:'Temp'",
     "HRULE:25#FF0000:'Low Limit'")

