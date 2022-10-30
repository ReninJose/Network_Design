# Author: Renin Kingsly Jose
# EECE.4830 Network Design
# Phase 3

# Receiver.py

import socket

def checksum(data):

    chk = ''
    chk_list = []

    s1 = data[0:8]
    s2 = data[8:16]

    sum = bin(int(s1,2)+int(s2,2))[2:]

    if(len(sum) > 8):
        chk = sum[1:]
        chk = bin(int(chk,2)+int(sum[0],2))[2:]
        if(len(chk) < 8):
            while(len(chk) != 8):
               chk = '0' + chk 
    else:
        chk = sum

    chk_list[:0] = chk                  # Convert string to list

    for i in range(0, len(chk_list)):
        if(chk_list[i] == "0"):
            chk_list[i] = "1"
        elif(chk_list[i] == "1"):
            chk_list[i] = "0"

    return ''.join(chk_list)

local_port = 12005
buffer_size = 1024 #bytes

r_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
r_socket.bind(('', local_port))
r_socket.settimeout(7)                  # Timeout for socket.recvfrom(); Can be modified (in sec) 

image = []

# Read data
while True:
    try:
        incoming_packet, sender_addr = r_socket.recvfrom(buffer_size)   #incoming_packet = (chksum, sq_num, raw_data)
        # raw_data corruption identifier
        if(incoming_packet[0] != checksum(incoming_packet[2])):
            # Send a n-ack to sender
            r_socket.sendto(1, sender_addr)
        else:
            # Send an ack to sender
            r_socket.sendto(0, sender_addr)
            image.append(incoming_packet[2])
    except:
        print("Error: Timeout or packet parsing failed")
        break

rawData = b''.join(image)               # Extracting data
file = open("output.bmp", "wb")
file.write(rawData)                     # Writing Raw data to output.bmp
file.close()

r_socket.close()                        # Close UDP connection