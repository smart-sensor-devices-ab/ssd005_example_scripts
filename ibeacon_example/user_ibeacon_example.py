import uuid

import serial
import time

connecting_to_dongle = 0
print("Connecting to dongle...")
#Trying to connect to dongle
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
print("\n Welcome to the iBeacon example!\n\n")


new_input = 1
while 1 and console.is_open.__bool__():
    # get keyboard input once
    if (new_input == 1):
        # Python 2 users
        # input = raw_input("Enter the UUID... ")
        new_input = input("Enter the UUID (x) string with Major (j), Minor (n) and TX (t) (format:"
                          "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxjjjjnnnntt): ")
        # send the character to the dongle
        time.sleep(0.1)
        console.write(str.encode("AT+ADVDATAI="))
        console.write(new_input.encode())
        console.write('\r'.encode())
        time.sleep(0.1)
        console.write(str.encode("AT+ADVSTART=0;200;3000;0;"))
        console.write('\r'.encode())
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
    while console.inWaiting() > 0:
        out += console.read(console.inWaiting()).decode()
    else:
        if not out.isspace():
            # We make sure it doesn't print the same message over and over again by setting [out] to blankspace
            # after printing once and check for blankspace before print again
            print(">>" + out)
            out = "  "