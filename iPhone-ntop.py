#!/usr/bin/python3
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.syslog import SyslogService
from pymobiledevice3.services.os_trace import OsTraceService
import time
import re
import curses

lockdown = create_using_usbmux()

#curses block

stdscr = curses.initscr()
stdscr.scrollok(1)
curses.curs_set(0)
stdscr.nodelay(1)
stdscr.timeout(10)

sh, sw = stdscr.getmaxyx()
header = stdscr.subwin(1, sw, 0, 0)
try:
    header.addstr('Waiting for Data Usage logs...')
    header.refresh()
except curses.error as e:
    print(str(e))

def drawTable(data):
    sh, sw = stdscr.getmaxyx()
    rows = len(data)
    cols = len(data[0])
    cell_width = int(sw - 52) // cols
    cell_height = int(sh) // rows


    stdscr.erase()
    stdscr.clear()
    header = stdscr.subwin(1, sw, 0, 0)
    try:
        header.addstr('Process Name | # Unique Flows | wifiRx | wifiTx | cellRx | cellTx | wifiDeltaRx | wifiDeltaTx | cellDeltaRx | cellDeltaTx')
        header.refresh()
    except curses.error as e:
        print(str(e))
    for r in range(rows):
        for c in range(cols):
            if c == 0:
                x = 0
            else:
                x = (((c - 1)  * cell_width) + 42)
            y = r * cell_height
            try:
                stdscr.addstr(y + 2, x, str(data[r][c]), curses.A_STANDOUT)
            except curses.error as e:
                print(str(e))

    
    stdscr.refresh()
######

completePattern = r"Data\sUsage\sfor\s(?P<procName>[\w\.\-\_\(\)]+)\son\sflow\s(?P<flowID>[0-9]{1,8})\s-\sWiFi\sin\/out\:\s(?P<wifiRx>[0-9]{1,13})\/(?P<wifiTx>[0-9]{1,13})\,\sWiFi\sdelta_in\/delta_out\:\s(?P<wifiDeltaRx>[0-9]{1,13})\/(?P<wifiDeltaTx>[0-9]{1,13})\,\sCell\sin\/out\:\s(?P<cellRx>[0-9]{1,13})\/(?P<cellTx>[0-9]{1,13})\,\sCell\sdelta_in\/delta_out\:\s(?P<cellDeltaRx>[0-9]{1,13})\/(?P<cellDeltaTx>[0-9]{1,13})\,\s"

networkProcTable = {}
i = 0
for line in SyslogService(service_provider=lockdown).watch():
    flowLog = []
    if "Data Usage for " in line:
        match = re.search(completePattern, line)
        if match:
            flowLog.append(match.groupdict()["procName"])
            flowLog.append(match.groupdict()["flowID"])
            flowLog.append(match.groupdict()["wifiRx"])
            flowLog.append(match.groupdict()["wifiTx"])
            flowLog.append(match.groupdict()["wifiDeltaRx"])
            flowLog.append(match.groupdict()["wifiDeltaTx"])
            flowLog.append(match.groupdict()["cellRx"])
            flowLog.append(match.groupdict()["cellTx"])
            flowLog.append(match.groupdict()["cellDeltaRx"])
            flowLog.append(match.groupdict()["cellDeltaTx"])

            logDict = match.groupdict()
            if logDict['procName'] not in networkProcTable.keys():
                flowIds = [logDict['flowID']]
                tmpSubDict = {'uniqueFlowIds': flowIds,
                              'wifiRx': logDict['wifiRx'],
                              'wifiTx': logDict['wifiTx'],
                              'cellRx': logDict['cellRx'],
                              'cellTx': logDict['cellTx'],
                              'wifiDeltaRx': logDict['wifiDeltaRx'],
                              'wifiDeltaTx': logDict['wifiDeltaTx'],
                              'cellDeltaRx': logDict['cellDeltaRx'],
                              'cellDeltaRx': logDict['cellDeltaTx']                           
                              }

                networkProcTable[logDict['procName']] = tmpSubDict
            else:
                networkProcTable[logDict['procName']]['uniqueFlowIds'].append(logDict['flowID'])
                networkProcTable[logDict['procName']]['wifiRx'] = logDict['wifiRx']
                networkProcTable[logDict['procName']]['wifiTx'] = logDict['wifiTx']
                networkProcTable[logDict['procName']]['cellRx'] = logDict['cellRx']
                networkProcTable[logDict['procName']]['cellTx'] = logDict['cellTx']
                networkProcTable[logDict['procName']]['wifiDeltaRx'] = logDict['wifiDeltaRx']
                networkProcTable[logDict['procName']]['wifiDeltaTx'] = logDict['wifiDeltaTx']
                networkProcTable[logDict['procName']]['cellDeltaRx'] = logDict['cellDeltaRx']
                networkProcTable[logDict['procName']]['cellDeltaTx'] = logDict['cellDeltaTx']

        else:
            print("No match found.")
            print(line)

        i = i + 1
        if i % 2 == 0:
            sorted_dict = dict(sorted(networkProcTable.items(), key=lambda item: int(item[1]['cellTx']), reverse=True))
            outputList = []
            for key, val in sorted_dict.items():
                if 'cellDeltaTx' not in val.keys():
                    val['cellDeltaTx'] = '0'
                tmpNetworkProcList = [key,
                                      len(val['uniqueFlowIds']),
                                      val['wifiRx'],
                                      val['wifiTx'],
                                      val['cellRx'],
                                      val['cellTx'],
                                      val['wifiDeltaRx'],
                                      val['wifiDeltaTx'],
                                      val['cellDeltaRx'],
                                      val['cellDeltaTx']
                                      ]
                outputList.append(tmpNetworkProcList)
            drawTable(outputList)
