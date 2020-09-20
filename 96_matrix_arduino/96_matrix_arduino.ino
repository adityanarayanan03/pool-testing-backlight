//Variables for controlling the Shift Register(s)
int latchPin = 8;
int clockPin = 12;
int dataPin = 11;
int numOfRegisters = 3;
byte *registerState;

//Variables to help with data transfer from Python
String incomingString = "000000000000"; //6 Copies of 2 digits per Anode/Cathode
int anodes[] = {0, 0, 0};
int cathodes[] = {0, 0, 0}; //Zero is not a valid index for the LED Matrix

void setup()
{
  //Initialize array
  registerState = new byte[numOfRegisters];
  for (size_t i = 0; i < numOfRegisters; i++)
  {
    registerState[i] = 0;
  }

  //set pins to output so you can control the shift register
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);

  //Clear all the shift registers. Anodes go LOW, Cathodes go HIGH
  resetRegisters();

  //Set up serial communication at 9600 baud
  //Might have to go 115200 if multiplexing no good.
  Serial.begin(9600);
}

void loop()
{

  //Check for any incoming data
  if (Serial.available() > 0)
  {
    incomingString = Serial.readString();

    for (int i = 0; i < 3; i++)
    {
      //The protocol I set up here is that anode indices indexed
      //from 1 are the first 6 digits. Cathodes follow suite as next 6.
      anodes[i] = incomingString.substring(2 * i, 2 * (i + 1)).toInt();
      cathodes[i] = incomingString.substring(2 * i + 6, 2 * (i + 1) + 6).toInt();
    }
  }

  for (int i = 0; i < 3; i++)
  {
    //Sends the command to the LED array based on the incoming data.
    writeLED(anodes[i], cathodes[i], 10000 / 3);
  }

  //Serial.println(anodes[0]);
  //Serial.println(cathodes[0]);
}

void regWrite(int pin, bool state)
{
  /*
  Writes a certain pin and a certain state to the Shift registers
  */
  //Determines register
  int reg = pin / 8;
  //Determines pin for actual register
  int actualPin = pin - (8 * reg);

  //Begin session by assigning latch pin low
  PORTB &= ~_BV(PB0); //Directly write latch pin low

  for (int i = 0; i < numOfRegisters; i++)
  {
    //Get actual states for register
    byte *states = &registerState[i];

    //Update state
    if (i == reg)
    {
      bitWrite(*states, actualPin, state);
    }

    //Write
    shiftOut(dataPin, clockPin, MSBFIRST, *states);
  }

  //End session by assigning latch pin high
  PORTB |= _BV(PB0); //Directly writing the latch pin HIGH
}

void resetRegisters()
{
  /*
  Goes through and clears all the registers such that
  no LED's will be on. Anodes are written LOW and Cathodes
  are written HIGH.
  */
  for (int i = 0; i < 12; i++)
  {
    regWrite(i, LOW);
  }

  for (int i = 12; i < 20; i++)
  {
    regWrite(i, HIGH);
  }
}

void writeLED(int anode, int cathode, int microsecs)
{
  /*
  Applies the regWrite function to an anode pin, cathode pin,
  and keeps the LED on for specific microseconds. LED array
  is indexed at 1.
  */
  if (anode != 0 && cathode != 0)
  {
    regWrite(anode - 1, HIGH);
    regWrite(cathode + 12 - 1, LOW);

    delayMicroseconds(microsecs);

    regWrite(anode - 1, LOW);
    regWrite(cathode + 12 - 1, HIGH);
  }
}
