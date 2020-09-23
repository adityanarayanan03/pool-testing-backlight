import math
import serial
import serial.tools.list_ports
import random
import time
import sys
import pickle
from tkinter import *
from tkinter import filedialog

class Pool_Matrix:
    """
    Class for the Duration of a pool-testing run.
    """
    sampleNum = 1
    dim = 0
    numSamples = 0
    readFile = None
    arduino = None
    arduinoPort = None
    inputMatrix = None
    useFile = False

    mainwindow = None
    readInputWindow = None
    readDimensionWindow = None
    showSampleNum = None
    plusButton = None
    sampleNumString = None
    startButton = None
    dimensionInput = None

    def setup(self):
        try:
            self.arduinoPort = [a.device for a in serial.tools.list_ports.comports() if "USB-SERIAL" in a.description][0]
            self.arduino = serial.Serial(self.arduinoPort, 9600)
        except:
            pass

    def read_from_file(self):
        self.readFile = filedialog.askopenfilename()
        print(self.readFile)
        self.readInputWindow.destroy()
        f = open(self.readFile, 'r')
        self.inputMatrix = eval(f.read())
        self.numSamples = int(len(self.inputMatrix)*len(self.inputMatrix[0])/3)
        print(self.numSamples)
        self.useFile = True
        
        
    def collect(self):
        self.dim = int(self.dimensionInput.get())
        self.numSamples = self.dim**2
        print(self.dim)
        self.readDimensionWindow.destroy()

    def input_scheme(self):
        self.readInputWindow.destroy()
        self.readDimensionWindow = Tk()
        self.readDimensionWindow.geometry("400x300")
        self.readDimensionWindow.title("Dimension Input")
        self.dimensionInput = StringVar(self.readDimensionWindow)
        self.dimensionInput.set("Select Sampling Dimension") #Setting Default Value
        dimensionOptions = [i for i in range(1, 32)]
        dimSelector = OptionMenu(self.readDimensionWindow, self.dimensionInput, *dimensionOptions)
        dimSelector.config(font = ("TkDefaultFont", 13))
        dimSelector.place(anchor='s', rely = .5, relx = .5)

        go = Button(self.readDimensionWindow, text = "Go", command = self.collect, font = ("TkDefaultFont", 15))
        go.place(anchor = 'n', rely = .5, relx = .5)
        self.readDimensionWindow.mainloop()

    def read_inputs(self):
        """
        Should read inputs from either the command line or a GUI
        """
        self.readInputWindow = Tk()
        self.readInputWindow.geometry("400x300")
        self.readInputWindow.title("Startup")

        self.readFileButton = Button(self.readInputWindow, text = 'Read From File', command = self.read_from_file, width = 15, height = 3, font = ("TkDefaultFont", 20))
        self.readFileButton.place(rely=.5, relx = .5, anchor = 's')

        self.inputSchemeButton = Button(self.readInputWindow, text = 'Input Scheme', command = self.input_scheme, width = 15, height = 3, font = ("TkDefaultFont", 20))
        self.inputSchemeButton.place(rely=.5, relx = .5, anchor = 'n')

        self.readInputWindow.mainloop()


    def plus_one(self):
        """
        Increases the sample number by 1.
        """

        if (self.sampleNum < self.numSamples):
            self.sampleNum += 1
            self.sampleNumString.set(f"On Sample: {self.sampleNum} out of {self.numSamples}")

        if(self.useFile):
            self.send_to_arduino(self.get_test_from_file())
        else:
            self.send_to_arduino(self.get_tests())

    def get_tests(self, cell = None):
        """
        Takes in a cell (sample number) and dim (height or width of grid). Total
        number of samples is dim^2; cell is a number from 1 to dim^2.

        Returns a list of 3 integers corresponding to the 3 tests for which 'cell'
        is part of the testing pool.

        First number corresponds to the row test (number from 1 to dim), second
        number is for col test (from dim+1 to 2*dim), third number is for
        diagonal (wrapping) test (from 2*dim+1 to 3*dim).
        """
        if not cell:
            cell = self.sampleNum

        if (cell % self.dim) >= math.ceil(cell / self.dim):
            return [
                math.ceil(cell / self.dim),
                self.dim + (cell % self.dim),
                2 * self.dim + (cell % (self.dim + 1)),
            ]
        else:
            return [
                math.ceil(cell / self.dim),
                self.dim + (cell % self.dim),
                2 * self.dim + ((cell % self.dim + math.ceil(cell / self.dim) * self.dim) % (self.dim + 1)),
            ]

    def get_test_from_file(self):
        return [i for i in range(len(self.inputMatrix)) if self.sampleNum in self.inputMatrix[i]]

    def send_to_arduino(self, leds):
        """
        Takes in the three(or really how many ever) integers from 1-96 that correspond
        to values for the 8x12 LED matrix and sends them over serial connection to the
        Arduino using a pre-described protocol

        Returns True if successful, False if error occurred, and throws errors.
        """

        if(len(leds) == 1):
            leds = leds * 3

        if (len(leds) != 3):
            raise ValueError("Function requires 3 or 1 leds")

        anodes = [i%12 if i%12 != 0 else 12 for i in leds]
        cathodes = [i//12+1 if i%12!=0 else i//12 for i in leds]

        sendString = ""
        for anode in anodes:
            if anode < 10:
                sendString += f"0{anode}"
            else:
                sendString += f"{anode}"
        
        for cathode in cathodes:
            if cathode > 8:
                raise ValueError("This format is not compatible with 96 well plate")
            sendString += f"0{cathode}"
        
        try:
            print(sendString)
            self.arduino.write(sendString.encode())
        except serial.serialutil.SerialException:
            pickle_dump = {'dim':self.dim, 'sampleNum':self.sampleNum}
            pickle_file = open("pool_testing_backup", "wb")
            pickle.dump(pickle_dump, pickle_file)
            pickle_file.close()


            print("Sending data failed! The serial connection was terminated. Recovery data saved to pickle file.")
            sys.exit(0)
        return True
    
    def matrixStart(self):
        if(self.useFile):
            self.send_to_arduino(self.get_test_from_file())
        else:
            self.send_to_arduino(self.get_tests())
        self.startButton.destroy()
        self.plusButton["state"] = "active"
        self.sampleNumString.set(f"On Sample: {self.sampleNum} out of {self.numSamples}")

    def __init__(self, dim=31, sampleNum=1, readFile=None):

        self.dim = dim
        self.sampleNum = sampleNum
        self.readFile = readFile

        self.setup()

        self.read_inputs()

        self.mainwindow = Tk()
        self.mainwindow.geometry("500x500")
        self.mainwindow.title("Pool Testing Matrix Controller")

        self.sampleNumString = StringVar(self.mainwindow)
        self.sampleNumString.set("Sampling has not been started")
        self.showSampleNum = Label(self.mainwindow, textvariable = self.sampleNumString, font = ("TkDefaultFont", 24))
        self.showSampleNum.config(height = 4)
        self.showSampleNum.pack()

        self.plusButton = Button(text = 'Plus One', command = self.plus_one, width = 15, height = 3, font = ("TkDefaultFont", 20))
        self.plusButton.place(rely=.5, relx = .5, anchor = 's')
        self.plusButton["state"] = "disabled"

        self.startButton = Button(text = 'Start', command = self.matrixStart, width = 15, height = 3, font = ("TkDefaultFont", 20))
        self.startButton.place(rely=.5, relx = .5, anchor = 'n')

        self.mainwindow.mainloop()


if __name__ == "__main__":
    run = Pool_Matrix()
