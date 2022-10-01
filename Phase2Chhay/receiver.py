# Author: Renin Kingsly Jose
# EECE.4830 Network Design
# Phase 2

# Receiver.py

import socket

local_port = 12005
buffer_size = 1024 #bytes

r_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
r_socket.bind(('', local_port))
r_socket.settimeout(3)                  # Timeout for socket.recvfrom(); Can be modified (in sec) 

image = []                              # A list to store bytes of data in each index

# Read data
while True:
    try:
        incoming_packet, sender_addr = r_socket.recvfrom(buffer_size)
        image.append(incoming_packet)
    except:
        break

rawData = b''.join(image)               # Extracting data

f = open("output.bmp", "wb")
f.write(rawData)                        # Writing Raw data to output.bmp
f.close()

r_socket.close()                        # Close UDP connection