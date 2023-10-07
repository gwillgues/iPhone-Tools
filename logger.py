#!/usr/bin/python3
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.syslog import SyslogService
from pymobiledevice3.services.os_trace import OsTraceService
import time


lockdown = create_using_usbmux()
timestamp = str(int(time.time()))
dirName = f"iphoneLogs-{timestamp}"
syslogObj = OsTraceService(lockdown=lockdown).collect(dirName)
