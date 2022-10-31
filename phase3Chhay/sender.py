#Author @ Keegan Chhay (file send / socket functionality), Ryan White (gui support)
#EECE Network Design: Protocols and apps
#Phase 3: Implement RDT 2.2 over a reliable UDP channel
#========================================================================#
# ALL PRINT STATEMENTS ARE COMMENTED OUT, IT IS USED TO HELP CHECK OUTPUT
#========================================================================#

# import socket library and math for floor function
from math import floor
from socket import *
import struct
# import gui module and file browsing library
from tkinter import *
from tkinter import filedialog

def MakePkt(seqNum, data, check):
    
    binheader = struct.pack(seqNum, check)
    udt_packet = binheader + data

    return udt_packet

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

def MakePayloads():
    
    # Get textiowrapper of path and extract name for the path to the filename
    directPath = filedialog.askopenfile(mode='r', filetypes=[('Image Files', '*jpeg')])
    filename = directPath.name
    seq_num = 0

    with open(filename, "rb") as f:                         # open the file as a binary type assigned it to f
        image_bytes = f.read()                              # image_bytes is assigned the contents of f
        #print(len(image_bytes))
        #print(image_bytes[0:len(image_bytes)])   
        tot_slice = floor(len(image_bytes)/1024)            # tot_slice returns number of packets to be sent 
        #print(tot_slice)
        
    for slice_index in range(tot_slice + 1):         
        #print(slice_index)                                 # used to check the slice index in the output
        x = slice_index                                     # determining the index for contents of the packet
        starting_index = x * 1024
        stop_index = starting_index + 1024
        packet_slice = (image_bytes[starting_index:stop_index])
        clientSocket.sendto(MakePkt(seq_num, packet_slice, binary_simple_checksum(packet_slice)), (serverName, 12005))
        message, receiver_addr = clientSocket.recvfrom(2048)           

        while(message != 0):
            # Resend data
            clientSocket.sendto(MakePkt(seq_num, packet_slice, binary_simple_checksum(packet_slice)), (serverName, 12005))
            message, receiver_addr = clientSocket.recvfrom(2048)

        seq_num += 1

# configure server and port name
serverName = gethostname()
serverPort = 12000
addr = (serverName, serverPort) 

# creates UDP socket for server
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(addr)

# Configure base gui characteristics: window title, size, label
root = Tk()
root.title('Project Phase 2')
root.geometry('200x200')
titleLabel = Label(root, text = "Network Design Phase 2", font="Verdana")
titleLabel.pack()

# Create button to allow user to upload any bmp file given a path
uploadButton = Button(root, text='Choose File for Upload', command = lambda:MakePayloads())
uploadButton.pack()

root.mainloop()
clientSocket.close() #close the socket
