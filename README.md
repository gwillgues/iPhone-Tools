

# iPhone-Tools
Collection of tooling related to iOS/iPhones
All of these tools require the device to be connected to a PC via USB, and you must trust the PC from the iPhone.

# Dependencies
You pymobiledevice3 is required for these tools to work. After cloning the repository, you can install it via ```python3 -m pip install -r requirements.txt```

# iPhone-ntop.py

This script is designed to be useful for detecting malware or other abnormal processes sending traffic on Apple iOS. By building a baseline of which process names have network activity, one can look for outliers. This is a similar technique that is used in the Mobile Verification Toolkit, which uses very similar logs (datausage.sqlite), except this is run in real time on the device instead of using logs extracted from backups. The script opens a syslog stream from the target device. It then scans the logs for Data Usage events generated by symptomsd, parses the log, and monitors which processes are using WiFi/Cellular data. It displays this data in a CLI interface similar to the **top** command. This could be used in some cases to detect malware present on an iPhone. Fullscreen your terminal before running, the curses interface doesn't display properly in a small terminal.
```
usage: iPhone-ntop.py [-h] [--jsonfile JSONFILE] [--output OUTPUT]
                      [--sortby SORTBY]

Monitor iPhone syslog stream for data usage events, and create a live table of
processes using WiFi/Cellular data.

options:
  -h, --help           show this help message and exit
  --jsonfile JSONFILE  File path to load a json state file previously saved
                       with --output
  --output OUTPUT      File path to save the current state of the network
                       process table upon exiting the application. Can be
                       loaded later with the --jsonfile argument.
  --sortby SORTBY      Select which field to sort by when displaying
                       information. Can be uniqueFlowIds, wifiRx, wifiTx,
                       cellRx, cellTx, wifiDeltaRx, wifiDeltaTx, cellDeltaRx,
                       or cellDeltaTx.
```

The fields that are defined are as follows


**Process Name** - Name of the process making network connections

**uniqueFlowIds/# Unique Flows** - There is a field called Flow ID in the Data Usage events, this appears to correspond to unique flows for a specific network request. A larger number of these may indicate the process is opening a large  number of sockets. The script keeps tally of the total number of unique flow IDs observed for a given process name.

**wifiRx** - Bytes received via the WiFi interface for the given process name

**wifiTx** - Bytes sent via the WiFi interface for the given process name

**cellRx** - Bytes received via the cellular interface for the given process name

**cellTx** - Bytes sent via the cellular interface for the given process name

**wifiDeltaRx** - Every time a Data Usage event is generated for a process, this field indicates the number of bytes that has increased in the wifiRx field since the last observed event for a given process name.

**wifiDeltaTx** - Every time a Data Usage event is generated for a process, this field indicates the number of bytes that has increased in the wifiTx field since the last observed event for a given process name.

**cellDeltaRx** - Every time a Data Usage event is generated for a process, this field indicates the number of bytes that has increased in the cellRx field since the last observed event for a given process name.

**cellDeltaTx** - Every time a Data Usage event is generated for a process, this field indicates the number of bytes that has increased in the cellTx field since the last observed event for a given process name.

Save the output to a json file when exiting the application by using the --output parameter. It is possible to load those same json files back into the program using the --jsonfile parameter. Choose which field to sort by using the --sortby parameter.





# iPhoneDNS-monitor.py

This is currently a crude script in development that monitors DNS requests/IP connections by specific processes on an iPhone, and keeps track and makes a state table of which processes have connected to which domains/IP addreses. This requires scapy.

# procList.py

This script gets a process listing from the target device. This includes process ID and process name


# logger.py

This script extracts saved logs from the device's storage, and saves them to a directory named iPhoneLogs-**TIMESTAMP** . These logs are in a Unified Log format. You can parse these binary log files using a tool such as [Mandiant's unifiedlog_parser](https://github.com/mandiant/macos-UnifiedLogs)
