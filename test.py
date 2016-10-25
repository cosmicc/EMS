#!/usr/bin/python

import psutil

cpu=psutil.cpu_percent(interval=1)
mem=psutil.virtual_memory()
disk=psutil.disk_usage('/')

cpud int(round(cpu,0))
memd int(round(mem.percent,0))
dskd int(round(disk.percent,0))
