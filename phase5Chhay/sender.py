#Author @ Keegan Chhay (file send / socket functionality), Ryan White (gui support)
#EECE Network Design: Protocols and apps
#Phase 5: Implement GBN over a reliable UDP channel with bit-errors and loss
#========================================================================#
# ALL PRINT STATEMENTS ARE COMMENTED OUT, IT IS USED TO HELP CHECK OUTPUT
#========================================================================#

# import socket library and math for floor function
from math import floor
from socket import *
import struct
import time
from time import struct_time
import sys

# import gui module and file browsing library
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import traceback

winSize = int(sys.argv[1])
dividedPackets = [] # hold the segmented data from the packet division
gbnBuffer = [] # sliding window to send packets to the receiver

# Configure base gui characteristics: window title, size, label
root = Tk()
root.title('Project Phase 5')
titleLabel = Label(root, text = "Network Design Phase 5", font="Verdana")
titleLabel.pack()

# Create button to allow user to upload any bmp file given a path
uploadButton = Button(root, text='Choose File for Upload', command = lambda:MakePayloads())
uploadButton.pack()

progressbar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=100)
progressbar.pack()

def MakePkt(seqNum, data, check):

    format = "II" + str(1024) + "s"
    packedData = struct.pack(format, check, seqNum, data)
    return packedData

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
    directPath = filedialog.askopenfile(mode='r', filetypes=[('Image Files', '*jpg')])
    filename = directPath.name
    # declare initial sequence number and base pointer
    seq_num = 0; base = 0; nextSeqNum = 0

    start_time = time.time()
    print(start_time)

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
        dividedPackets.append(packet_slice)
    
    while(True):
        try:
            while (nextSeqNum < base + winSize):
                print("sending ", nextSeqNum)
                gbnBuffer.append(MakePkt(nextSeqNum, dividedPackets[nextSeqNum], binary_simple_checksum(dividedPackets[nextSeqNum])))
                nextSeqNum += 1
                clientSocket.sendto(gbnBuffer[len(gbnBuffer)-1], (serverName, 12005))
            
            ack, receiver_addr = clientSocket.recvfrom(2048)
            if(ack != b'00000000' and ack != b'11111111'):
                # Ack corrupted: therefore, resend all N packets in the window
                print("ACK CORRUPTED")
                nextSeqNum = base
                #for i in range(len(gbnBuffer)):
                #    clientSocket.sendto(gbnBuffer[i], receiver_addr)
                #    nextSeqNum += 1

            if(ack == b'11111111'):
                # Resend data
                # Negative acknowledgement received: therefore, resend all N packets in the window
                nextSeqNum = base

            if(ack == b'00000000'):
                # Positive ack, continue sending next packet
                # Shift the base pointer, pop earliest packet
                base += 1
                gbnBuffer.pop(0)

                progressbar['value'] += 1.5873
                if (nextSeqNum == 63):
                    #endTime = time.time()
                    #print(endTime - start_time)
                    uploadLabel = Label(root,text='All packets sent!',font="Verdana")
                    uploadLabel.pack()
                continue

        except TimeoutError as e:
            #Timeout. Resend all N packets in window
            print("Timeout, Resending window")
            nextSeqNum = base
        except IndexError:
            print("Sending complete!")
            break
        except Exception as e:
            print(e)
            break


# configure server and port name
serverName = gethostname()
serverPort = 12000
addr = (serverName, serverPort) 

# creates UDP socket for server
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(addr)
clientSocket.settimeout(0.0015)      # Timeout; Can be modified

root.mainloop()
clientSocket.close()            #close the socket