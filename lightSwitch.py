import socket
import select
from omni.kit.scripting import BehaviorScript

class LightSwitch(BehaviorScript):
    def on_init(self):
        host = ''
        port = 3009
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Makes the socket non-blocking to allow Omniverse to update
        self.s.setblocking(False)
        # Binds the socket to the provided port
        self.s.bind((host,port))
        self.s.listen(1)
        # List of connections to read from
        self.read_list = [self.s]

    # Executes every update while the scene is playing
    def on_update(self, current_time: float, delta_time: float):
        light = self.stage.GetPrimAtPath("/Environment/DiskLight")
        light1 = self.stage.GetPrimAtPath("/Environment/DiskLight_01")
        # Retrieves the current brightness of the light
        attribute = light.GetAttribute("intensity")
        attribute1 = light1.GetAttribute("intensity")
        # Readable is the list of connections that have data that needs to be read
        readable, writable, errors = select.select(self.read_list, [], [], 0)
        # Loops over each connection
        for connection in readable:
            if connection is self.s:
                # Connects to the socket if it is currently readable
                conn, addr = connection.accept()
                # Adds the connection to the list of connections to be read
                self.read_list.append(conn)
            else:
                # Retrieves any data from the connected port
                data = connection.recv(1024)
                # Decodes the encrypted data
                txtData = data.decode('utf-8')
                # Eliminates any special charactes and line breaks
                txtData = txtData.replace('\r', '')
                txtData = txtData.replace('\n', '')
                # Determines which state the lights should be in
                if int(txtData[-1]) == 0:
                    # Turns off the lights
                    attribute.Set(0)
                    attribute1.Set(0)
                elif int(txtData[-1]) == 1:
                    # Turns on the lights
                    attribute.Set(60000)
                    attribute1.Set(60000)

    def on_destroy(self):
        print("Closing Connections")
        # Sends a message to anything connected to the same port
        self.s.sendall(b"Close this connection!")
        # Closes the socket
        self.s.close()