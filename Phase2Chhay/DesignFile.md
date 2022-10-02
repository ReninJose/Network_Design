Author @ Keegan Chhay, Ryan White, Renin Kingsly Jose
Group member: Renin Kingsly Jose, Ryan White
EECE Network Design: Protocols and apps
Phase 2: Implement RDT 1.0 over a reliable UDP channel

The purpose of this assignment is to transfer a BMP File between a UDP client socket (sender)
and a UDP server (receiver). Doing so by RDT 1.0 protocol.

Sender Design: sender.py

First code block Link:
https://studentuml-my.sharepoint.com/:i:/r/personal/keegan_chhay_student_uml_edu/Documents/phase2snips/first%20block.JPG?csf=1&web=1&e=jpv9Dx
 -Import math library for floor function and import socket library (lines 2-3)
 -Shows how create a host and port (line 12-13)
 -Creates a socket for UDP (AF_INET, SOCK_DGRAM) (line 16)


Second code block Link:
https://studentuml-my.sharepoint.com/:i:/r/personal/keegan_chhay_student_uml_edu/Documents/phase2snips/second%20block.JPG?csf=1&web=1&e=QfazwR
-assigns filename to "kitten.bmp"
-open the file as binary
-read the binary conents and assign it to image_bytes
-all print functions used were to check the output for testing. (lines 21, 22, 24)
this line 21 with show the total amount of bytes in the file, line 22 will show us the contents of bytes turned into hexidecimal
line 24 shows use the total amount of packets that needs to be used
-tot_slice returns the number of packets to be sent by taking the lenght of image_bytes / 1024 bytes. Rounding it to get a whole number.


Third code block Link:
https://studentuml-my.sharepoint.com/:i:/r/personal/keegan_chhay_student_uml_edu/Documents/phase2snips/third%20block.JPG?csf=1&web=1&e=sPGOwR
-for loop for each tot_slice index assigning it to slice_index.
-print(slice_index) is for testing making sure you are outputing each index from tot_slice.
-assign x to slice_index to determine the index for contents of packet
-create a stop and starting index. start = x *1024 , stop = x * 1024 * 1024
-packet_slice will give you the data split into chuncks for each slice index
-print(packet_slice) will show you each packet and the contents used for testing it is comment out.


Last code block Link:
https://studentuml-my.sharepoint.com/:i:/r/personal/keegan_chhay_student_uml_edu/Documents/phase2snips/last%20block.JPG?csf=1&web=1&e=E66pUL
-attach server name, port to message and sends into socket for the ending receiver
-closes the socket

Receiver Design: receiver.py *Renin
- Import python's socket libraries
![image](https://user-images.githubusercontent.com/44981300/193434552-72100c45-1a00-41ed-937a-417ae1efc9a3.png)

- Create/Setup UDP connection
![image](https://user-images.githubusercontent.com/44981300/193434563-747a9ac7-21a4-47c1-bcd9-da8e6430d3ab.png)

- Configurable timeout for receiving data
![image](https://user-images.githubusercontent.com/44981300/193434574-db10b39c-f55e-4da9-9be6-4545950930fd.png)

- Read in packets by packets from the sender and store it in a list
![image](https://user-images.githubusercontent.com/44981300/193434610-68d5df20-0427-4fd1-b9d6-2b02390d659f.png)

- Extract all data from the list and join them
![image](https://user-images.githubusercontent.com/44981300/193434616-7801c839-e08e-437c-85ed-f6bb10e1479d.png)

- Write the complete raw data to "output.bmp"
![image](https://user-images.githubusercontent.com/44981300/193434621-b9a7cd5a-0926-4431-8700-c25dde92f255.png)

- Close socket
![image](https://user-images.githubusercontent.com/44981300/193434625-942dc6c0-49bf-4046-bf3c-273068b36f13.png)


Extra Credit: *Ryan

![image](https://user-images.githubusercontent.com/44981300/193417586-73ba67b3-57e3-4ad7-bc8b-a857d11dde54.png)

I started my design process by importing Python's GUI package tkinter, and importing library that supports file browsing and selection.

![image](https://user-images.githubusercontent.com/44981300/193417636-fd2b316e-4b33-444c-b2c8-3e9764b25e66.png)

After creating the server host name and port number, base GUI characteristics are configured, including the window's title, size, and title label. Line 21 creates the GUI object itself in memory, and Line 25 configures the label to be visually created in the GUI.

![image](https://user-images.githubusercontent.com/44981300/193417818-f2a3d0b0-1f05-4ed5-81de-56cd7b241d8d.png)

Lines 28-29 create and display the button object that, when clicked, will call the SendFile function which prompts the user to select a bmp file to be sent to the receiver.

![image](https://user-images.githubusercontent.com/44981300/193417892-ce3fa17f-e63a-4964-8d97-dfc63846bd19.png)

Now that SendFile has been entered, the user is prompted to select any bmp file in their directory which is returned in the variable directPath. However, since filedialog returns an object known as a textIoWrapper (a buffered text interface to a buffered raw stream), the actual filepath is accessed by invoking directPath.name as seen on line 38. The filename is now ready to be passed to the rest of the sender program.

![image](https://user-images.githubusercontent.com/44981300/193418132-fe70109a-742d-4259-89a5-42fe19aab55c.png)

This label denoting complete file transfer is constructed after the sender code runs, and serves as a visual note of success to the user.

![image](https://user-images.githubusercontent.com/44981300/193418178-b10f13ec-02fd-4adc-9714-d5f03b5cbe17.png)

Line 61 launches the GUI at the conclusion of the script. It notably comes before the client socket closes: if the mainloop method was invoked after the client socket was closed, communication with the receiver side would be impossible.

