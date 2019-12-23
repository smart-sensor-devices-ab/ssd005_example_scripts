import serial
import time

connecting_to_dongle = 0
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


print("\n\nConnected to Dongle.\n")
print("\nWelcome to the Serial Port Service (SPS) example!\n\n")

# Python 2 users
# input = raw_input("Choose 1) for... ")
role_input = input("Choose \n1) for Peripheral Role\n2) for Central role\n>> ")
while not role_input == "1" or role_input == "2":
    role_input = input("Please choose 1 or 2.\nChoose 1 for Peripheral Role or 2 for Central role: ")

connected = "0";
while 1 and console.is_open.__bool__():
    out = ""
    while console.inWaiting() > 0:
        out += console.read(console.inWaiting()).decode()
        if not out.isspace():
            # We make sure it doesn't print the same message over and over again by setting [out] to blankspace
            # after printing once and check for blankspace before print again
            print(out + " ")
            out = " "

    if role_input == "1":
        time.sleep(0.1)
        # sends the commands to the dongle. Important to send the \r as that is the return-key.
        console.write(str.encode("AT+ADVSTART"))
        console.write('\r'.encode())
        print("Please wait for Central to connect before typing.")
        while connected == "0":
            out += console.read(console.inWaiting()).decode()
            time.sleep(5)
            if not out.isspace():
                # We make sure it doesn't print the same message over and over again by setting [out] to blankspace
                # after printing once and check for blankspace before print again
                print(out + " ")
                if out.__contains__("CONNECTED."):
                    connected = "1"
                out = " "
        console.write(str.encode("AT+SPSRECEIVE"))
        console.write('\r'.encode())
        role_input = "0"
    elif role_input == "2":
        time.sleep(0.1)
        # sends the commands to the dongle. Important to send the \r as that is the return-key.
        console.write(str.encode("AT+CENTRAL"))
        console.write('\r'.encode())
        input_address = input("Please address ([x]xx:xx:xx:xx:xx:xx) of Peripheral device: ")
        console.write(str.encode("AT+GAPCONNECT="))
        console.write(input_address.encode())
        console.write('\r'.encode())
        print("Please wait to connect to Peripheral before typing.")
        while connected == "0":
            out += console.read(console.inWaiting()).decode()
            time.sleep(5)
            if not out.isspace():
                # We make sure it doesn't print the same message over and over again by setting [out] to blankspace
                # after printing once and check for blankspace before print again
                print(out + " ")
                if out.__contains__("CONNECTED."):
                    connected = "1"
                out = " "
        console.write(str.encode("AT+SPSRECEIVE"))
        console.write('\r'.encode())
        role_input = "0"

        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)

    # Wait to open terminal until the device is connected
    if connected == "1":
        terminal_input = input(">>")
        time.sleep(0.1)
        # sends the commands to the dongle. Important to send the \r as that is the return-key.
        console.write(str.encode("AT+SPSSEND="))
        console.write(terminal_input.encode())
        console.write('\r'.encode())
        time.sleep(0.5)