import math
import serial
import serial.tools.list_ports
import time
import sys
import pickle
from tkinter import *
from tkinter import filedialog

class Pool_Matrix:
    """
    Class for the Duration of a pool-testing run.
    """
    sampleNum = 1 #The plate number the user is on
    dim = 0 #Width or height of the pooling matrix
    numSamples = 0 #Total number of samples. May be dim^2.
    readFile = None #Location of file to read
    inputMatrix = None
    useFile = False

    arduino = None #Serial information
    arduinoPort = None

    #Tkinter variables
    mainwindow = None
    readInputWindow = None
    readDimensionWindow = None
    showSampleNum = None
    plusButton = None
    sampleNumString = None #Later established as Tkinter string var that displays on main window
    startButton = None
    dimensionInput = None

    def establish_connection(self):
        '''
        Sets up serial communication with the arduino board
        '''
        self.sampleNumString.set("Establishing Connection...")
        self.mainwindow.update()
        try:
            #Defines some communication objects. Maybe increasing baud rate will make the delay smaller?
            self.arduinoPort = [a.device for a in serial.tools.list_ports.comports() if "USB-SERIAL" in a.description][0]
            self.arduino = serial.Serial(self.arduinoPort, 9600)
            self.sampleNumString.set("Backlight Found. Initializing...")
            self.mainwindow.update()
            time.sleep(2)
            return True
        except:
            #Maybe put in some flag or exception or pop-up or something
            return False

    def read_from_file(self):
        '''
        Uses Tkinter Filedialog to ask the user for a file and processes the 
        input from the file
        '''
        #Uses tkinter to ask user for a file location
        self.readFile = filedialog.askopenfilename()

        #Kills The input window because we don't need it anymore
        self.readInputWindow.destroy()

        #This is all stuff to process the file. It reads as a nested list.
        f = open(self.readFile, 'r')
        self.inputMatrix = eval(f.read())

        #Reset some PIV's and status variables.
        self.numSamples = int(len(self.inputMatrix)*len(self.inputMatrix[0])/3)
        self.useFile = True
        
        
    def collect(self):
        '''
        Collects input from the user in the case that they want to input the 
        scheme by hand
        '''
        self.dim = int(self.dimensionInput.get())
        self.numSamples = self.dim**2
        self.readDimensionWindow.destroy()

    def input_scheme(self):
        '''
        Creates the window for asking the user for the dimension if they
        want to input by hand.
        '''
        #This stuff just makes some Tkinter nonsense
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

        #Create a button underneath the dropdown and loop the window
        go = Button(self.readDimensionWindow, text = "Go", command = self.collect, font = ("TkDefaultFont", 15))
        go.place(anchor = 'n', rely = .5, relx = .5)
        self.readDimensionWindow.mainloop()

    def read_inputs(self):
        """
        Reads input from GUI windows.
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
        Increases the sample number by 1, and calls the necessary functions to send to the Arduino
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
        '''
        Searches the matrix we got from Origami Assays in the file for the three locations where
        states are high.
        '''
        return [i+1 for i in range(len(self.inputMatrix)) if self.sampleNum in self.inputMatrix[i]]

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
        
        #Creates the anode, cathode pair from the raw numbers
        anodes = [i%12 if i%12 != 0 else 12 for i in leds]
        cathodes = [i//12+1 if i%12!=0 else i//12 for i in leds]

        #Constructs the string we need to send to the arduino
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
        
        #Send to the arduino. If that fails, then save stuff to pickle file and quit.
        try:
            #print(sendString)
            self.arduino.write(sendString.encode())
        except serial.serialutil.SerialException:
            pickle_dump = {'dim':self.dim, 'sampleNum':self.sampleNum}
            pickle_file = open("pool_testing_backup", "wb")
            pickle.dump(pickle_dump, pickle_file)
            pickle_file.close()


            #print("Sending data failed! The serial connection was terminated. Recovery data saved to pickle file.")
            sys.exit(0)
        return True
    
    def matrixStart(self):
        '''
        Starting the matrix needs special instructions that cant be done from __init__
        '''
        if self.establish_connection():
            if(self.useFile):
                #print(self.arduinoPort)
                #print(self.arduino)
                #self.arduino.write("010101020202".encode())
                self.send_to_arduino(self.get_test_from_file())
            else:
                self.send_to_arduino(self.get_tests())
            self.startButton.destroy()
            self.plusButton["state"] = "active"
            self.sampleNumString.set(f"On Sample: {self.sampleNum} out of {self.numSamples}")
        else:
            self.sampleNumString.set("No Backlight Found")

    def __init__(self, dim=31, sampleNum=1, readFile=None):

        self.dim = dim
        self.sampleNum = sampleNum
        self.readFile = readFile

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
