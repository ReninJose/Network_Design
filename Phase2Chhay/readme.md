Author @ Keegan Chhay,
EECE Network Design: Protocols and apps
Phase 2: Implement RDT 1.0 over a reliable UDP channel
Group member: Renin , Ryan

OS: Windows 10 64-bit
Language: Python 
Version: 3.9.13 

Read the diagram given in chpater 3.4.1

Create a New folder: Name the folder reflecting the phase of this assignment (ex.Phase2YOURNAME)

in the folder create 2 .py scripts , import an bmp image , readme.md and designfile.md

-receiver.py
-sender.py
-"image".bmp 
-readme.md
-DesignFile.md

We are reusing some code from Phase1 here are the following instructions:

From client.py:

1)import python's socket libraries
2)create UDP socket for server
3)attach server name, then port to message and allow it to send into socket

we are going to use these for sender.py

For sender.py:
1)import python's socket libraries
2)create UDP socket for server
3)open image file from the same folder (bmp format)
4)convert that image file to binary 
5)split the data into the amount of packets to be sent (lenght/1024)
6)Make a for loop that each packet index and give each one data bytes until index is done
7)attach server name, then port to message and allow it to send into socket
8)close socket

if you encounter problems and it is not communicating with the server
change hostname() to gethostname().

For Receiver.py: *Renin
1)
2)
3)
4)
5)
6)
7)
8)


Extra Credit: *Ryan
1)
2)
3)
4)
5)
6)
7)
8)


Final Part: *CHANGE THIS FOR NEW INSTRUCTIONS
1) Run the serverUDP.py script
2) Now you can run clientUDP .py script
3) In the client command line arguments you can type any message
4) This will get the same message back