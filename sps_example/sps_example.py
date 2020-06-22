import serial
import time

target_dongle_mac_address = "[0]40:48:FD:E5:2D:05" # Change this to the peripheral's mac address.
your_com_port = 'COM14' # Change this to the com port your dongle is connected to.

# Global
connecting_to_dongle = True
counter = 0
msg = ""
latest_msg = ""
error_counter = 0

print("Connecting to dongle...")
# Trying to connect to dongle until connected. Make sure the port and baudrate is the same as your dongle.
# You can check in the device manager to see what port then right-click and choose properties then the Port Settings
# tab to see the other settings
while connecting_to_dongle:
    try:
        console = serial.Serial(
            port=your_com_port,
            baudrate=57600,
            parity="N",
            stopbits=1,
            bytesize=8,
            timeout=0
        )
        if console.is_open.__bool__():
            connecting_to_dongle = False
    except:
        print("Dongle not connected. Please reconnect Dongle.")
        time.sleep(5)

# This script will send data from one dongle to another which in turn will echo it back and forth between the dongles.
print("\n\nConnected to Dongle.\n")
print("\nWelcome to the Serial Port Service (SPS) example!\n\n")
print("\nRemember to setup the Peripheral dongle first so Central has something to connect to.\n\n")

# Python 2 users
# input = raw_input("Choose \n1) for Peripheral...
role_input = input("Choose: \n1) for Peripheral Role\n2) for Central role\n>> ")
while not (role_input == "1" or role_input == "2"):
    role_input = input("Please choose 1 or 2.\nChoose: \n1) for Peripheral Role \n2) for Central role\n>>  ")

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
        time.sleep(0.1)
        print("Putting dongle in Central role and trying to connect to other dongle.")
        while connected == "0":
            # Sends the commands to the dongle. Important to send the \r as that is the return-key.
            time.sleep(0.5)
            console.write(str.encode("AT+GAPCONNECT="))
            console.write(str.encode(target_dongle_mac_address))
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
                    time.sleep(2)
                    # We wait a bit then sends the starting msg to the other dongle.
                    console.write(str.encode(msg))
                    counter += 1
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
                # so we put it in a try-except block so that it wont crash the script. We also save the last message as
                # a fallback in case of error.
                try:
                    # Here we convert the msg to a string and strip it of all newlines and carriage returns.
                    msg = str(dongle_output3.decode("ascii"))
                    msg = msg.replace('[Received]: ', '')
                    msg = msg.replace("\r\n", "")
                    latest_msg = msg
                except:
                    # In case of an error we use the last received message instead and increment the error counter.
                    msg = latest_msg
                    error_counter += 1
                print("This is what we will send: " + msg)
                # Encodes the string msg than sends it back to the other dongle.
                console.write(str.encode(msg))
                counter += 1
                # Just a little counter to show how many messages we've sent.
                print(str(counter) + " message(s) sent. " + str(error_counter) + " error(s).")
                # In case we get disconnected from the other dongle we go back to the previous state of waiting for a
                # connection (Peripheral) / trying to reconnect (Central).
            if dongle_output3.__contains__(str.encode("\r\nDISCONNECTED.")):
                print("Disconnected!")
                # Send an Escape to abort stream.
                console.write(0x1B)
                connected = "0"
            dongle_output3 = ""
        msg = ""
