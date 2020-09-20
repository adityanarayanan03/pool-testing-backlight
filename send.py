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
    if(time.time() - startTime > b*5.0):
        i += 1
        b += 1
        c = 2*i
        d = int(b**2)

        num1 = random.randint(1, 8)
        num2 = random.randint(1,8)
        num3 = random.randint(1, 8)

        if(num1<10):
            myString = f"0{num1}"
        else:
            myString = f"{num1}"

        if(num2<10):
            myString += f"0{num2}"
        else:
            myString += f"{num2}"

        if(num3<10):
            myString += f"0{num3}"
        else:
            myString += f"{num3}"
        

        if(num1<10):
            myString += f"0{num1}"
        else:
            myString += f"{num1}"

        if(num2<10):
            myString += f"0{num2}"
        else:
            myString += f"{num2}"

        if(num3<10):
            myString += f"0{num3}"
        else:
            myString += f"{num3}"

        arduino.write(myString.encode())
        print(f"sending {myString}")
    #time.sleep(5)

    #print(arduino.readline().decode('utf-8'))