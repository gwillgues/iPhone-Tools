

# iPhone-Tools
Collection of tooling related to iOS/iPhones
All of these tools require the device to be connected to a PC via USB, and you must trust the PC from the iPhone.

# Dependencies
You pymobiledevice3 is required for these tools to work. After cloning the repository, you can install it via ```python3 -m pip install -r requirements.txt```

# iPhone-ntop.py

This script opens a syslog stream from the target device. It then scans the logs for Data Usage events, parses the log, and monitors which processes are using WiFi/Cellular data. It displays this data in a CLI interface similar to the **top** command. This could be used in some cases to detect malware present on an iPhone.

# iPhoneDNS-monitor.py

This is currently a crude script in development that monitors DNS requests/IP connections by specific processes on an iPhone, and keeps track and makes a state table of which processes have connected to which domains/IP addreses. This requires scapy.

# procList.py

This script gets a process listing from the target device. This includes process ID and process name


# logger.py

This script extracts saved logs from the device's storage, and saves them to a directory named iPhoneLogs-**TIMESTAMP** . These logs are in a Unified Log format. You can parse these binary log files using a tool such as [Mandiant's unifiedlog_parser](https://github.com/mandiant/macos-UnifiedLogs)
