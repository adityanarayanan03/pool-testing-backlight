# Pool Testing Backlight
The pool testing backlight offers an efficient way to perform pool/group testing on a 96 well plate, without robotic pipetting machine or paper templates.

## Hardware
The Pool Testing Backlight (pictured below) is a enclosed device with a seat for a standard 96-well plate. The backlight contains an 8x12 LED array underneath a polycarbonate window. When a well plate is placed into its seat, individual LED's on the array can be turned on to indicate certain desired wells on the well plate. 

<img src="https://adityanarayanan03.github.io/images/pool_testing_backlight.JPG">

The LED array is built around an Arduino Nano, and uses three 8-bit shift register IC's as a serial-to-parallel converter to achieve mulitplexing on the LED array. The driver software communicates with the Arduino Nano through a USB-Serial connection, which also supplies the necessary 5V to the Arduino Nano.  
## Software

The software for the pool testing backlight is a driver program that serves a couple of purposes:

- Load and interpret multiple data formats
- Send LED-lighting information to the backlight device
- Interact with users through a Graphical interface

The software was written in Python 3.6 and the GUI was built using the TKinter module. The module cx_freeze was used to create executable files from the original Python script.
## How to use the pool testing backlight
### 1. Installation
The driver software for the pool-testing-backlight can be downloaded [here](https://adityanarayanan03.github.io/projects/pool_testing_backlight/pool_testing_backlight.html). The program itself is located at ```"Pool Testing Backlight"/Executables/backlight.exe```. The exe file should not be removed from the Executables directory. I recommend adding backlight.exe to your PATH or system variables, but that is purely optional. An alternative is to simply create a shortcut for ```backlight.exe``` somewhere accessible, such as on your desktop.

### 2. Preparing the testing matrix
The pool testing backlight offers two methods to load a specific testing scheme: through text file or by selecting a sample size.

- **Through Text File**:
Loading your testing scheme through a text file is as simple as saving your testing matrix to a text file. A sample input is available [here](https://github.com/adityanarayanan03/pool-testing-backlight/blob/master/sample_input.txt). Pre made lists containing the matrix data can be found at [Origami Assays](https://www.smarterbetter.design/origamiassays/default/choose_assay).
- **Through sample dimension**:
The pool-testing-backlight software allows you to select the length/width of an array containing patient samples. For example, to pool 400 patients' samples, I would select "20" when prompted by the software, and the program will generate a scheme to pool the 400 patients' samples into wells 1-60 on the well plate.


### 3. Using the software
- **Run backlight.exe**
- **Ensure the backlight is connected to your computer via USB**. If the program does not detect a backlight, try different USB ports and check Device Manager to identfiy if a serial device is found.
- **Follow the prompts given by the software**

## Issues?
Follow any troubleshooting steps listed in the instructions. If that doesn't fix the issue, open an issue through GitHub.
