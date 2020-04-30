import serial
import time
from datetime import datetime

# Name of file that will be created and store the saved data
file_name = "SavedData.txt"
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
print("\n Welcome to the Scan and Store example!\n\n")

# Method for parsing and writing to file
def write_data_to_file(out_data):
    addr_string = ""
    data_string = ""
    now = datetime.now() # Generating a timestamp
    current_time = now.strftime("%H:%M:%S") # Formatting the timestamp
    out_data = out_data.replace('\r','') # Remove return.
    out_data = out_data.replace('\n','') # Remove new line.
    fo = open(file_name, "a")
    for i in range(2,21): # Reading the MAC-Address and saving it into addr_string
        addr_string += out_data[i]
    for x in range(41, 102): # Here the advertising/response data gets stored in the data_string variable
        data_string += out_data[x]
    fo.write("{")
    fo.write("["+current_time+"]")
    fo.write(addr_string)
    fo.write(":")
    fo.write(data_string)
    fo.write("}\n")
    fo.close()


new_input = 1
try:
    while 1 and console.is_open.__bool__():
        # get keyboard input once
        if (new_input == 1):
            # Python 2 users
            # input = raw_input("Enter something such as a Manufacturer Specific (MFS) ID to scan for and store in a file or just leave it blank to scan all: ")
            new_input = input("Enter something such as a Manufacturer Specific (MFS) ID to scan for and store in a file or just leave it blank to scan all: ")
            time.sleep(0.1)
            # sends the commands to the dongle. Important to send the \r as that is the return-key.
            console.write(str.encode("AT+CENTRAL"))
            console.write('\r'.encode())
            time.sleep(0.1)
            console.write(str.encode("AT+FINDSCANDATA="))
            console.write(new_input.encode())
            console.write('\r'.encode())
            out = ''
            # Let's wait one second before reading output (let's give device time to answer)
            time.sleep(1)
            print("\nCollecting data...\nPress Ctrl-C to stop.")
        while console.inWaiting() > 0:
            out += console.read(console.inWaiting()).decode()
        else:
            if not out.isspace():
                # We make sure it doesn't print the same message over and over again by setting [out] to blankspace
                # and check for blankspace and that [out] isn't anything else before writing to file
                if not out.__contains__("AT+") and not len(out) <= 106:
                    write_data_to_file(out)
                out = "  "
except KeyboardInterrupt:
    exit()
