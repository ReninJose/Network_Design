# Author: Renin Kingsly Jose
# EECE.4830 Network Design
# Phase 4

# Receiver.py

from math import floor
from queue import Empty
import random
import socket
import struct

# for command line arg
import sys

# WRITE FUNCTION FOR PACKET LOSS HERE

def CorruptRawData(packet, percentage):

    try:
        # enter if packet is randomly selected to be corrupted
        if (random.random() < percentage):
            print("Raw data corrupted")
            packetString = str(packet)
            packetList = list(packetString)

            # revise? corrupts 
            for i in range(len(packetList)):
                if (packetList[i].isalpha() and packetList[i] != 'b'):
                    packetList[i] = 'a'
            
            for i in range(len(packetList)):
                if (packetList[i] == '\\'):
                    packetList[i] == ''
            # add jpeg header
            packetList[:2] = '\\xff\\xd8'
            corruptedPacket = ''.join(packetList)
            corruptedPacket = bytes(corruptedPacket.encode())
            return corruptedPacket
        else:
            # no changes: don't corrupt packet
            return packet
    except Exception as e:
        print("Raw data corrupt throwing")
        print(e)
        return -1

def CorruptACK(packet, percentage):
    try:
        # corrupt ack at selected frequency
        if (random.random() < percentage):
            print(random.random())
            print("Ack corrupted")
            packet = ''.join('1' if x == '0' else '0' for x in packet)
            packet = bytes(packet.encode())
            print(type(packet))
            return packet
        else:
            print(type(packet))
            return packet
    except Exception as e:
        print("ACK corrupt throwing")
        print(e)

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
percentage = int(sys.argv[2]) / 100

image = []
buffer = -1         # Setting a non-zero sq_num for buffer

# Read data
while True:
    try:
        duplicate = False                                                       # Boolean to set duplicate
        incoming_packet, sender_addr = r_socket.recvfrom(buffer_size)           #incoming_packet = (chksum, sq_num, raw_data)
        chksum, sq_num, raw_data = struct.unpack("II1024s", incoming_packet)
        print("Packet: ", sq_num)

        if(buffer == sq_num):
            # Duplicate
            print("Duplicate packet detected")

            # Send positive ack
            print("Positive ack")

            if(option == 2):
                ack = CorruptACK(b'00000000', percentage)
            else:
                ack = b'00000000'

            r_socket.sendto(ack, sender_addr)         
            duplicate = True

        # Perform this operation only 
        if(duplicate == False):
            if(option == 3):
                # Data packet bit corruption
                raw_data = CorruptRawData(raw_data, percentage)
            
            if(option == 5):
                # CALL PACKET LOSS FUNCTION HERE
                raw_data = IDK_MAN_WHATEVER_YOU_NAME_IT(raw_data, percentage)

            # raw_data corruption identifier
            print(chksum) 
            print(binary_simple_checksum(raw_data))

            if(chksum != binary_simple_checksum(raw_data)):
                # Send a n-ack to sender
                print("Negative ack: Packet error detected")

                if(option == 2):
                    ack = CorruptACK(b'11111111', percentage)
                else:
                    ack = b'11111111'

                r_socket.sendto(ack, sender_addr) 
            else:
                # Send an ack to sender
                print("Positive ack")

                if(option == 2):
                    ack = CorruptACK(b'00000000', percentage)
                else:
                    ack = b'00000000'

                r_socket.sendto(ack, sender_addr)
                buffer = sq_num
                image.append(raw_data)

    except Exception as e:
        print(e.args)
        break

rawData = b''.join(image)               # Extracting data
file = open("output.jpg", "wb")
file.write(rawData)                     # Writing Raw data to output.bmp
file.close()

r_socket.close()                        # Close UDP connection