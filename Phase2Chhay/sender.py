#Author @ Keegan Chhay (file send / socket functionality), Ryan White (gui support)
#EECE Network Design: Protocols and apps
#Phase 2: Implement RDT 1.0 over a reliable UDP channel
#========================================================================#
# ALL PRINT STATEMENTS ARE COMMENTED OUT, IT IS USED TO HELP CHECK OUTPUT
#========================================================================#

# import socket library and math for floor function
from math import floor
from socket import *

# import gui module and file browsing library
from tkinter import *
from tkinter import filedialog

def SendFile():

    # Get textiowrapper of path and extract name for the path to the filename
    directPath = filedialog.askopenfile(mode='r', filetypes=[('Image Files', '*bmp')])
    filename = directPath.name

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
    
    # Inform user of successful file transfer
    completed = Label(root, text = "Upload complete!", font="Verdana")
    completed.pack()

# configure server and port name
serverName = gethostname()
serverPort = 12000

# Configure base gui characteristics: window title, size, label
root = Tk()
root.title('Project Phase 2')
root.geometry('200x200')
titleLabel = Label(root, text = "Network Design Phase 2", font="Verdana")
titleLabel.pack()

# Create button to allow user to upload any bmp file given a path
uploadButton = Button(root, text='Choose File for Upload', command = lambda:SendFile())
uploadButton.pack()

# creates UDP socket for server
clientSocket = socket(AF_INET, SOCK_DGRAM)

SendFile()

root.mainloop()
clientSocket.close() #close the socket