import serial
import serial.tools.list_ports
import time

arduino_port = [a.device for a in serial.tools.list_ports.comports() if "Arduino" in a.description][0]

arduino = serial.Serial(arduino_port,9600)

i = 0
b = 0
c = 0
startTime = time.time()
while 1:
    if(time.time() - startTime > b*3.0):
        i += 1
        b += 1
        c = 2*i
        d = int(b**2)

        if(i<10):
            myString = f"0{i}"
        else:
            myString = f"{i}"

        if(c<10):
            myString += f"0{c}"
        else:
            myString += f"{c}"

        if(d<10):
            myString += f"0{d}"
        else:
            myString += f"{d}"

        arduino.write(myString.encode())
    #time.sleep(5)

    print(arduino.readline().decode('utf-8'))