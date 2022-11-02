# Author: Renin Kingsly Jose
# EECE.4830 Network Design
# Phase 3

# Receiver.py

from math import floor
from queue import Empty
import random
import socket
import struct

# for command line arg
import sys

def CorruptPackets(packet, percentage):

    #n = floor(percentage * len(packetList))
    #packetsToCorrupt = (random.sample(packetList, n))
    #corruptedByte = '\x00' + os.urandom(4) + '\x00'
    #print(corruptedByte)
    #return corruptedByte

    corruptedPacketList = list(packet)
    print(corruptedPacketList)

    for i in range(len(corruptedPacketList) * percentage):
        if (corruptedPacketList[i] == 0):
            corruptedPacketList[i] = 1
        elif corruptedPacketList[i] == 1:
            corruptedPacketList[i] = 0

    corruptedPacket = ''.join(corruptedPacketList)
    corruptedPacket = corruptedPacket.encode('UTF-8')

    return corruptedPacket

def binary_simple_checksum(data):

    """Data is a byte object. Returns 1 byte checksum"""
    cs_max = 0xffffffff # 32 bits
    sum = cs_max
    for i in range(len(data)):
        val = data[i]
        sum += val
        sum <<= val
        sum %= (cs_max)

    return sum

local_port = 12005
buffer_size = 2048 #bytes

r_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
r_socket.bind(('', local_port))
r_socket.settimeout(10)                                                         # Timeout for socket.recvfrom(); Can be modified (in sec) 

option = int(sys.argv[1])
percentage = int(sys.argv[2])

image = []
buffer = []

# Read data
while True:
    try:
        incoming_packet, sender_addr = r_socket.recvfrom(buffer_size)           #incoming_packet = (chksum, sq_num, raw_data)
        chksum, sq_num, raw_data = struct.unpack("II1024s", incoming_packet)
        
        


        if(option == 3):
            # Data packet bit corruption
            raw_data = CorruptPackets(raw_data, percentage)
            print("Raw data corrupted")
        
        # raw_data corruption identifier
        print(chksum) 
        print(binary_simple_checksum(raw_data))

        if(chksum != binary_simple_checksum(raw_data)):
            # Send a n-ack to sender
            print("Negative ack: Bit error detected")

            if(option == 2):
                ack = CorruptPackets(b'11111111', percentage)
                print("Ack corrupted")
            else:
                ack = b'11111111'

            r_socket.sendto(ack, sender_addr)
        else:
            # Send an ack to sender
            print("Positive ack")

            if(option == 2):
                ack = CorruptPackets(b'00000000', percentage)
                print("Ack corrupted")
            else:
                ack = b'00000000'

            r_socket.sendto(ack , sender_addr)
            image.append(raw_data)

    except Exception as e:
        print(e.args)
        break

rawData = b''.join(image)               # Extracting data
file = open("output.jpg", "wb")
file.write(rawData)                     # Writing Raw data to output.bmp
file.close()

r_socket.close()                        # Close UDP connection