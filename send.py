import serial
import serial.tools.list_ports
import time

arduino_port = [a.device for a in serial.tools.list_ports.comports() if "Arduino" in a.description][0]

arduino = serial.Serial(arduino_port,9600)

while 1:
    arduino.write("hi".encode())
    #time.sleep(.5)

    print(arduino.readline().decode('utf-8'))