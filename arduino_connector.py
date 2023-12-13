import serial
import socket
import select

host = socket.gethostname()
omni_port = 3009
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connects to the port that was opened by the Omniverse script
s.connect((host,omni_port))
# Connects to the same port as the Ardiuno chip
arduino_port = serial.Serial("COM3")
# Reads the starting state of the light switch
original_data = arduino_port.readline()
# Decodes the starting data
txt_original = original_data.decode('utf-8')
old_status = txt_original
# Sends the starting light switch state to Omniverse
s.sendall(original_data)
while True:
    read_list = [s]
    # Readable is the list of connections that have data that needs to be read
    readable, writable, errors = select.select(read_list, [], [], 0)
    if s in readable:
        # If data is being sent from Omniverse, the connection is shut down
        print("Shutting Down")
        # Exits the loop so the code can stop
        break
    # Reads the current data from the Arduino chip
    data = arduino_port.readline()
    # Decodes the encrypted data
    txtData = data.decode('utf-8')
    # Determines if the status has changed sense the last message
    if old_status != txtData:
        # If the status has changed a message is sent to Omniverse
        s.sendall(data)
        # Stores the current status of the light switch
        old_status = txtData