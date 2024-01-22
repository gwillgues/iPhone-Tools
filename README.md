# iPhone-Tools
Collection of tooling related to iOS/iPhones
All of these tools require the device to be connected to a PC via USB, and you must trust the PC from the iPhone.

# iPhone-ntop.py

This script opens a syslog stream from the target device. It then scans the logs for Data Usage events, parses the log, and monitors which processes are using WiFi/Cellular data. It displays this data in a CLI interface similar to the **top** command. This could be used in some cases to detect malware present on an iPhone.
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


# procList.py

This script gets a process listing from the target device. This includes process ID and process name


# logger.py

This script extracts saved logs from the device's storage, and saves them to a directory named iPhoneLogs-**TIMESTAMP** . These logs are in a Unified Log format. You can parse these binary log files using a tool such as [Mandiant's unifiedlog_parser](https://github.com/mandiant/macos-UnifiedLogs)
