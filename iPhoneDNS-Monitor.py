#!/usr/bin/python3

import hexdump
from scapy.all import *
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.pcapd import PcapdService

def parse_answer_section(packet):
    if packet.an is not None:
        for rr in packet.an:
            print(f"RR Name: {rr.rrname}")
            print(f"RR Data: {str(rr.rdata)}")
            print(f"RR Class: {rr.rclass}\n")

            if isinstance(rr.rdata, DNSRR):
                parse_answer_section(rr.rdata)

def getResourceRecords(dnsPacket):

    if dnsPacket.an != None:
#                parse_answer_section(dnsPacket)
       print(type(dnsPacket.an[0]))
       for rr in dnsPacket.an:
           print(f"RR Name: {rr.rrname}")
           print(f"RR Data: {rr.rdata}")
           print(f"RR Class: {rr.rclass}\n")
           print(f"RR Type: {rr.type}\n")
           if rr.type == 5:
               for i in range(0, len(dnsPacket)):
                   if dnsPacket[i].haslayer(DNSRR):
                       try:
                           for j in range(0, 64):
                               try:
                                   if dnsPacket[i].an[j].haslayer(DNSRR):
                                       for rr in dnsPacket[i].an[j]:
                                           print(f"RR Name: {rr.rrname}")
                                           print(f"RR Data: {rr.rdata}")
                               except IndexError:
                                   break
                       except AttributeError:
                           break

#                print(dnsPacket.an)

lockdown = create_using_usbmux()

service = PcapdService(lockdown=lockdown)
packet_generator = service.watch()

for packet in packet_generator:
#    print(packet.pid)
#    print(packet.io)
#    print(packet.comm)
#    print(packet.data)
    raw_bytes = packet.data
#    hexdump(raw_bytes)
    parsed = Ether(raw_bytes)
    if parsed.haslayer(UDP):
#        print("UDP Parsed")
#        print(parsed['UDP'])
        if parsed['UDP'].haslayer(DNS):
            dnsPacket = parsed['DNS']
            getResourceRecords(dnsPacket)
            if dnsPacket.an != None:
#                parse_answer_section(dnsPacket)
                print(type(dnsPacket.an[0]))
                for rr in dnsPacket.an:
                    print(f"RR Name: {rr.rrname}")
                    print(f"RR Data: {rr.rdata}")
                    print(f"RR Class: {rr.rclass}\n")
                    print(f"RR Type: {rr.type}\n")
                    if rr.type == 5:
                        for i in range(0, len(dnsPacket)):
                            if dnsPacket[i].haslayer(DNSRR):
                                try:
                                    for j in range(0, 64):
                                        try:
                                            if dnsPacket[i].an[j].haslayer(DNSRR):
                                                for rr in dnsPacket[i].an[j]:
                                                    print(f"RR Name: {rr.rrname}")
                                                    print(f"RR Data: {rr.rdata}")
                                        except IndexError:
                                            break
                                except AttributeError:
                                    break

#                print(dnsPacket.an)
#                print(dnsPacket.an[0].rrname)
#                print(dnsPacket.an[0].rdata)
#                print(dnsPacket.an[0].rclass)
                print("_" * 25)
    elif parsed.haslayer(TCP):
        pass
#        print("TCP Parsed")
#        print(parsed['TCP'])
    elif parsed.haslayer(IP):
        pass
#        print("IP Parsed")
#        print(parsed)
    else:
        pass
#        print("No UDP, TCP, or IP layer")
#        print(parsed)

#    print(packet.interface_name)
#    print(packet.protocol_family)
#    print("---------------------------------------------------------")
