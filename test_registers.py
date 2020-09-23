import serial
import serial.tools.list_ports
import time
import random

for a in serial.tools.list_ports.comports():
    print(a.description)

arduino_port = [a.device for a in serial.tools.list_ports.comports() if "USB-SERIAL" in a.description][0]

arduino = serial.Serial(arduino_port,9600)

i = 0
b = 0
c = 0
startTime = time.time()
while 1:
    myString = str(input("---> "))
    arduino.write(myString.encode())
    print(f"sending {myString}")
    #time.sleep(5)

    #print(arduino.readline().decode('utf-8'))