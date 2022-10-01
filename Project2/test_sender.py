#Author @ Keegan Chhay,
#EECE Network Design: Protocols and apps
#Phase 2: Implement RDT 1.0 over a reliable UDP channel
#========================================================================#
# ALL PRINT STATEMENTS ARE COMMENTED OUT, IT IS USED TO HELP CHECK OUTPUT
#========================================================================#

# import socket library and math for floor function
from math import floor
from socket import *

serverName = gethostname()
serverPort = 12000

# creates UDP socket for server
clientSocket = socket(AF_INET, SOCK_DGRAM)

filename = "kitten.bmp"         # assign filename to imagefile path
with open(filename, "rb") as f: # open the file as a binary type assigned it to f
    image_bytes = f.read()      # image_bytes is assigned the contents of f
    #print(len(image_bytes))
    #print(image_bytes[0:len(image_bytes)])   
    tot_slice = floor(len(image_bytes)/1024)  # tot_slice retunrs number of packets to be sent 
    #print(tot_slice)


for slice_index in range(tot_slice + 1): #for each packet    
    #print(slice_index) # used to check the slice index in the output
    x = slice_index           # determining the index for contents of the packet
    starting_index = x * 1024
    stop_index = starting_index + 1024
    packet_slice = (image_bytes[starting_index:stop_index])  
   # print(packet_slice) 
  
 
    clientSocket.sendto(packet_slice, (serverName, 12005))  # attach server name, port to message; send into socket


clientSocket.close() #close the socket