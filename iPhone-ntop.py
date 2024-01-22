#!/usr/bin/python3
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.syslog import SyslogService
#from pymobiledevice3.services.os_trace import OsTraceService
import time
import re
import curses
import argparse
import json


def drawTable(data, stdscr):
    sh, sw = stdscr.getmaxyx()
    rows = len(data)
    cols = len(data[0])
    cellWidth = int(sw - 52) // cols
    cellHeight = int(sh) // rows


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
                x = (((c - 1)  * cellWidth) + 42)
            y = r * cellHeight
            try:
                stdscr.addstr(y + 2, x, str(data[r][c]), curses.A_STANDOUT)
            except curses.error as e:
                print(str(e))

    
    stdscr.refresh()

def main():
    parser = argparse.ArgumentParser(description='Monitor iPhone syslog stream for data usage events, and create a live table of processes using WiFi/Cellular data.')
    parser.add_argument('--jsonfile', type=str,  help='File path to load a json state file previously saved with --output')
    parser.add_argument('--output', type=str,  help='File path to save the current state of the network process table upon exiting the application. Can be loaded later with the --jsonfile argument.')
    parser.add_argument('--sortby', type=str,  help='Select which field to sort by when displaying information. Can be uniqueFlowIds, wifiRx, wifiTx, cellRx, cellTx, wifiDeltaRx, wifiDeltaTx, cellDeltaRx, or cellDeltaTx.')
    args = parser.parse_args()


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
    completePattern = r"Data\sUsage\sfor\s(?P<procName>[\w\.\-\_\(\)]+)\son\sflow\s(?P<flowID>[0-9]{1,8})\s-\sWiFi\sin\/out\:\s(?P<wifiRx>[0-9]{1,13})\/(?P<wifiTx>[0-9]{1,13})\,\sWiFi\sdelta_in\/delta_out\:\s(?P<wifiDeltaRx>[0-9]{1,13})\/(?P<wifiDeltaTx>[0-9]{1,13})\,\sCell\sin\/out\:\s(?P<cellRx>[0-9]{1,13})\/(?P<cellTx>[0-9]{1,13})\,\sCell\sdelta_in\/delta_out\:\s(?P<cellDeltaRx>[0-9]{1,13})\/(?P<cellDeltaTx>[0-9]{1,13})\,\sRNF"
    
    global networkProcTable
    if args.jsonfile == None:
      networkProcTable = {}
    else:
      fd = open(str(args.jsonfile), 'r')
      jsonData = fd.read()
      networkProcTable = json.loads(jsonData)
    i = 0
    try:
        for line in SyslogService(service_provider=lockdown).watch():
            if "Data Usage for " in line:
                match = re.search(completePattern, line)
                if match:
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
                                      'cellDeltaTx': logDict['cellDeltaTx']                           
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
                    if args.sortby == None:
                        sorted_dict = dict(sorted(networkProcTable.items(), key=lambda item: int(item[1]['cellTx']), reverse=True))
                    elif str(args.sortby) == "uniqueFlowIds":
                        sorted_dict = dict(sorted(networkProcTable.items(), key=lambda item: len(item[1]['uniqueFlowIds']), reverse=True))
                    elif str(args.sortby) == "wifiRx":
                        sorted_dict = dict(sorted(networkProcTable.items(), key=lambda item: int(item[1]['wifiRx']), reverse=True))
                    elif str(args.sortby) == "wifiTx":
                        sorted_dict = dict(sorted(networkProcTable.items(), key=lambda item: int(item[1]['wifiTx']), reverse=True))
                    elif str(args.sortby) == "cellRx":
                        sorted_dict = dict(sorted(networkProcTable.items(), key=lambda item: int(item[1]['cellRx']), reverse=True))
                    elif str(args.sortby) == "cellTx":
                        sorted_dict = dict(sorted(networkProcTable.items(), key=lambda item: int(item[1]['cellTx']), reverse=True))
                    elif str(args.sortby) == "wifiDeltaRx":
                        sorted_dict = dict(sorted(networkProcTable.items(), key=lambda item: int(item[1]['wifiDeltaRx']), reverse=True))
                    elif str(args.sortby) == "wifiDeltaTx":
                        sorted_dict = dict(sorted(networkProcTable.items(), key=lambda item: int(item[1]['wifiDeltaTx']), reverse=True))
                    elif str(args.sortby) == "cellDeltaRx":
                        sorted_dict = dict(sorted(networkProcTable.items(), key=lambda item: int(item[1]['cellDeltaRx']), reverse=True))
                    elif str(args.sortby) == "cellDeltaTx":
                        sorted_dict = dict(sorted(networkProcTable.items(), key=lambda item: int(item[1]['cellDeltaTx']), reverse=True))
                    else:
                        sorted_dict = dict(sorted(networkProcTable.items(), key=lambda item: int(item[1]['cellTx']), reverse=True))


                    outputList = []

                    for key, val in sorted_dict.items():
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
                    drawTable(outputList, stdscr)
    except KeyboardInterrupt:
        curses.endwin()
        if args.output != None:
            jsonData = json.dumps(networkProcTable)
            fd = open(str(args.output), 'w')
            fd.write(jsonData)
            fd.close()
            print("KeyboardInterrupt, saving and exiting")
        else:
            print("KeyboardInterrupt, exiting without saving")

    except ConnectionAbortedError:
        curses.endwin()
        if args.output != None:
            jsonData = json.dumps(networkProcTable)
            fd = open(str(args.output), 'w')
            fd.write(jsonData)
            fd.close()
            print("Device disconnected or other connection error, saving and exiting")
        else:
            print("Device disconnected or other connection error, exiting without saving")
        


if __name__ == "__main__":
    main()
