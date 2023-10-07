#!/usr/bin/python3
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.syslog import SyslogService
from pymobiledevice3.services.os_trace import OsTraceService

lockdown = create_using_usbmux()
processList = OsTraceService(lockdown=lockdown).get_pid_list()

if processList['Status'] == "RequestSuccessful":
    for key, value in processList['Payload'].items():
        print(key, end='')
        print("|| ", value['ProcessName'])
