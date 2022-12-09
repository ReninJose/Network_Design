Authors: Ryan White, Keegan Chhay, Renin Kingsly-Jose
EECE 4830: Network Design
Prof. Vinod Vokkarane
Project Phase 5: Implement Go-Back-N protocol over an unreliable UDP channel

OS: Windows 10 64-bit, Ubuntu (Linux)
Python Version: 3.9.13

Contents:
Phase5_DesignDoc.dox: Design documentation.
receiver.py: Receive multiple packets from sender.py and append approved packets to image. Unapproved packets are sent again within the configured timeout.
sender.py: Slices jpeg image into multiple packets of data and sends to receiver.py. Depending on ACK value received, either resend previous packet or send next packet.
stonks.jpg: File to be transmitted.

Instructions:

1. Create two seperate terminal windows, and navigate to project folder.
2. Run sender.py in one terminal window with one command line arguments specifying window size.
3. Run receiver.py in the other terminal window with two command line arguments: the first dictates the option (1-5), and the next the percentage of corruption as an integer.
4. In the GUI created by sender.py, select stonks.jpg.
5. After waiting for the receiver to process the image, open output.jpg, and compare to stonks.jpg.