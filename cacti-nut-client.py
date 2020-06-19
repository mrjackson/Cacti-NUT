#!/usr/bin/env python3
#upsc apc_BR1500MS_a@192.168.10.209 2>&1 | grep -v '^Init SSL'

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

try:
    ddict['input.voltage']
except:
    ddict['input.voltage'] = "U"
try:
    ddict['input.frequency']
except:
    ddict['input.frequency'] = "U"
try:
    ddict['input.transfer.low']
except:
    ddict['input.transfer.low'] = "U"
try:
    ddict['input.transfer.high']
except:
    ddict['input.transfer.high'] = "U"

try:
    ddict['battery.runtime']
except:
    ddict['battery.runtime'] = "U"
try:
    ddict['battery.voltage']
except:
    ddict['battery.voltage'] = "U"
try:
    ddict['battery.runtime.low']
except:
    ddict['battery.runtime.low'] = "U"
try:
    ddict['battery.charge']
except:
    ddict['battery.charge'] = "U"

try:
    ddict['ups.load']
except:
    ddict['ups.load'] = "0"
try:
    ddict['ups.status']
    if ddict['ups.status'] == "OL":
        ddict['ups.status'] = "0"
    else:
        ddict['ups.status'] = "1"
except:
    ddict['ups.status'] = "U"
try:
    ddict['ups.realpower.nominal']
except:
    ddict['ups.realpower.nominal'] = "U"
try:
    ddict['ups.realpower']
except:
    try:
        ddict['ups.realpower'] = str(int(ddict['ups.realpower.nominal']) * (int(ddict['ups.load'])/100))
    except:
        ddict['ups.realpower'] = "U"


#ups_power = (int(ddict['ups.realpower.nominal']) * (int(ddict['ups.load'])/100))

#returndata = "battery_charge:" + ddict['battery.charge'] + " battery_runtime:" + ddict['battery.runtime']
returndata = "input_transfer_low:" + ddict['input.transfer.low']\
    + " input_transfer_high:" + ddict['input.transfer.high']\
    + " input_voltage:" + ddict['input.voltage']\
    + " input_frequency:" + ddict['input.frequency']\
    + " battery_runtime:" + ddict['battery.runtime']\
    + " battery_voltage:" + ddict['battery.voltage']\
    + " battery_runtime_low:" + ddict['battery.runtime.low']\
    + " battery_charge:" + ddict['battery.charge']\
    + " ups_load:" + ddict['ups.load']\
    + " ups_status:" + ddict['ups.status']\
    + " ups_realpower:" + ddict['ups.realpower']\
    + " ups_realpower_nominal:" + ddict['ups.realpower.nominal']

print(returndata)

logger.info("Script ended: " + str(datetime.now()) + " -- Output -- " + returndata)

