This project uses a physical light switch wired to an Arduino chip to control the lights inside of an Omniverse scene, Nvidia's Omniverse is a tool for building 3d worlds and digital twins. 
The 'arduino_connector' script is used to communicate with the Arduino chip and determine the current state of the light switch and the data is then sent to Omniverse using TCP sockets.
Inside Omniverse, the 'lightSwitch.py' file connects opens the port for 'arduino_connector.py' to connect to, and everytime a message is sent the 'lightSwitch' script determines if the Omniverse lights should be on or off.
Here is a quick demonstration of the code working

https://github.com/JoeRaines1/Arduino-In-Omniverse/assets/153453434/97c1da1f-8b6c-4b93-88af-3138893e2689

