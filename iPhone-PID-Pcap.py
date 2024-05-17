#!/usr/bin/python3

import sys
import pcapng.blocks as blocks
from pcapng import FileWriter
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.pcapd import PcapdService

# Connect to Device, setup pcap service, setup packet generator object
lockdown = create_using_usbmux()
service = PcapdService(lockdown=lockdown)
packet_generator = service.watch()

#Setup Section header block
shb = blocks.SectionHeader(
    options={
        "shb_hardware": "artificial",
        "shb_os": "python",
        "shb_userappl": "python-pcapng",
    }
)

#Set Interface Description Block

idb = shb.new_member(
    blocks.InterfaceDescription,
    link_type=1,
    options={
        "if_description": "iPhone",
        "if_os": "iOS 17.4"
    },
)


filename = sys.argv[1]
fd = open(filename, "wb")

#Setup FileWriter for writing to pcapng, pcapng format required for Comment section of packet, Comment section to add process data to pcap file
writer = FileWriter(fd, shb)

print("Capturing Packets....\n")
try:
    for packet in packet_generator:
        raw_bytes = packet.data
        new_packet = shb.new_member(blocks.EnhancedPacket, options={
            "opt_comment": f"Process ID: {packet.pid}, Process Name: {packet.comm}"
            })
        new_packet.packet_data = raw_bytes
        writer.write_block(new_packet)

except KeyboardInterrupt:
    print(f"\nSaving pcap to {filename}")
    fd.close()
    exit


fd.close()
