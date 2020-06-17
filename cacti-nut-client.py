#!/usr/bin/env python3
#upsc apc_BR1500MS_a@192.168.10.209

import sys
import subprocess

import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from datetime import timedelta

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename="/var/www/htdocs/cacti/log/cacti-nut-client.log", maxBytes=1048576, backupCount=1)
logger.addHandler(handler)
logger.info("Script started: " + str(datetime.now()) + " -- Arguments -- " + str(sys.argv[1:]))

try:
    serveraddress = str(sys.argv[1])
    upsname = str(sys.argv[2])
except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Arguments Error -- " + str(e))
    sys.exit(1)

cmd = "/usr/bin/upsc " + upsname + "@" + serveraddress + " 2>&1 | grep -v '^Init SSL'"

def nutdata(cmd):
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE)
    process.wait()
    data, err = process.communicate()
    if process.returncode is 0:
        return data.decode('utf-8')
    else:
        print("Error:", err)
    return ""

data = nutdata(cmd)

ddict = {}
for line in data.split('\n'):
    if line == "":
        continue
    d = line.split(':')
    ddict[d[0]] = d[1].lstrip()

returndata = "battery_charge:" + ddict['battery.charge'] + " battery_runtime:" + ddict['battery.runtime']
print(returndata)

logger.info("Script ended: " + str(datetime.now()) + " -- Output -- " + returndata)
