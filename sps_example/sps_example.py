import serial
import time

connecting_to_dongle = 0
counter = 0
msg = ""
print("Connecting to dongle...")
# Trying to connect to dongle until connected. Make sure the port and baudrate is the same as your dongle.
# You can check in the device manager to see what port then right-click and choose properties then the Port Settings
# tab to see the other settings
while connecting_to_dongle == 0:
    try:
        console = serial.Serial(
            port='COM14',
            baudrate=57600,
            parity="N",
            stopbits=1,
            bytesize=8,
            timeout=0
        )
        if console.is_open.__bool__():
            connecting_to_dongle = 1
    except:
        print("Dongle not connected. Please reconnect Dongle.")
        time.sleep(5)

# This script will send data from one dongle to another which in turn will echo it back and forth between the dongles.
print("\n\nConnected to Dongle.\n")
print("\nWelcome to the Serial Port Service (SPS) example!\n\n")
print("\nRemember to setup the Peripheral dongle first so Central has something to connect to.\n\n")

# Python 2 users
# input = raw_input("Choose \n1) for Peripheral...
role_input = input("Choose \n1) for Peripheral Role\n2) for Central role\n>> ")
while not (role_input == "1" or role_input == "2"):
    role_input = input("Please choose 1 or 2.\nChoose 1 for Peripheral Role or 2 for Central role: ")

connected = "0"
while 1 and console.is_open.__bool__():
    if role_input == "1":
        print("Starting advertising.")
        time.sleep(0.1)
        # Sends the commands to the dongle. Important to send the \r as that is the return-key.
        console.write(str.encode("AT+ADVSTART"))
        console.write('\r'.encode())
        while connected == "0":
            dongle_output = console.read(console.in_waiting)
            time.sleep(2)
            print("Awaiting connection to Central...")
            if not dongle_output.isspace():
                # We make sure it doesn't print the same message over and over again by resetting [out] to blankspace
                # after printing once and check for blankspace before print again
                print(dongle_output.decode())
                if dongle_output.__contains__(str.encode("\r\nCONNECTED.\r\n")):
                    # Opens Serial Stream
                    console.write(str.encode("AT+SPSSEND"))
                    console.write('\r'.encode())
                    connected = "1"
                    print("Connected!")
                dongle_output = " "
    elif role_input == "2":
        # This is what will be sent back and forth between the dongles.
        # You can change this message to whatever you like.
        msg = "Echo"
        # Sends the commands to the dongle. Important to send the \r as that is the return-key.
        console.write(str.encode("AT+CENTRAL"))
        console.write('\r'.encode())
        print("Putting dongle in Central role and trying to connect to other dongle.")
        while connected == "0":
            time.sleep(0.1)
            # Sends the commands to the dongle. Important to send the \r as that is the return-key.
            time.sleep(0.5)
            console.write(str.encode("AT+GAPCONNECT=[0]40:48:FD:E5:2D:05"))
            console.write('\r'.encode())
            dongle_output2 = console.read(console.in_waiting)
            time.sleep(2)
            print("Trying to connect to Peripheral...")
            if not dongle_output2.isspace():
                # We make sure it doesn't print the same message over and over again by resetting [out] to blankspace
                # after printing once and check for blankspace before print again
                print(dongle_output2.decode())
                if dongle_output2.decode().__contains__("CONNECTED."):
                    # Opens Serial Stream
                    console.write(str.encode("AT+SPSSEND"))
                    console.write('\r'.encode())
                    connected = "1"
                    print("Connected!")
                    # Sends the starting msg to the other dongle.
                    console.write(str.encode(msg))
                dongle_output2 = " "
    while connected == "1":
        dongle_output3 = console.read(console.in_waiting)
        # Let's wait 2 seconds to make sure we have had a chance of receiving anything before proceeding
        time.sleep(2)
        if not dongle_output3.isspace():
            # Here we check if we receive a message.
            if dongle_output3.__contains__(str.encode("\r\n[Received]: ")):
                print(dongle_output3)
                # Sometimes some extra bytes will be sent along with the message that the decode() function can't handle
                # so we put it in a try-except block so that it wont crash the script.
                try:
                    # Here we convert the msg to a string and strip it of all newlines and carriage returns.
                    msg = str(dongle_output3.decode("ascii"))
                    msg = msg.replace('[Received]: ', '')
                    msg = msg.replace("\r\n", "")
                except:
                    msg = "Error"
                print("This is what we will send:")
                print(str.encode(msg))
                time.sleep(1)
                # Encodes the string msg than sends it back to the other dongle.
                console.write(str.encode(msg))
                counter += 1
                # Just a little counter to show how many messages we've sent.
                print(str(counter) + " message(s) sent.")
                # In case we get disconnected from the other dongle we go back to the previous state of waiting for a
                # connection (Peripheral) / trying to reconnect (Central).
            if dongle_output3.__contains__(str.encode("\r\nDISCONNECTED.")):
                print("Disconnected!")
                connected = "0"
            dongle_output3 = ""
        msg = ""
