int latchPin = 8;
int clockPin = 12;
int dataPin = 11;

int numOfRegisters = 3;
byte* registerState;

void setup() {
  //Initialize array
  registerState = new byte[numOfRegisters];
  for (size_t i = 0; i < numOfRegisters; i++) {
    registerState[i] = 0;
  }

  //set pins to output so you can control the shift register
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);

  resetRegisters();

  Serial.begin(9600);
}

void loop() {
  writeLED(3,3,10000/3);
  writeLED(5,5,10000/3);
  writeLED(7,7,10000/3);
}

void regWrite(int pin, bool state){
  //Determines register
  int reg = pin / 8;
  //Determines pin for actual register
  int actualPin = pin - (8 * reg);

  //Begin session
  PORTB &= ~_BV(PB0); //Directly write latch pin low

  for (int i = 0; i < numOfRegisters; i++){
    //Get actual states for register
    byte* states = &registerState[i];

    //Update state
    if (i == reg){
      bitWrite(*states, actualPin, state);
    }

    //Write
    shiftOut(dataPin, clockPin, MSBFIRST, *states);
  }

  //End session
  PORTB |= _BV(PB0); //Directly writing the latch pin HIGH
}

void resetRegisters(){
  for(int i = 0; i<12; i++){
    regWrite(i, LOW);  
  }

  for(int i=12; i<20; i++){
    regWrite(i, HIGH);  
  }
}

void writeLED(int anode, int cathode, int microsecs){
  regWrite(anode-1, HIGH);
  regWrite(cathode+12-1, LOW);

  delayMicroseconds(microsecs);

  regWrite(anode-1, LOW);
  regWrite(cathode+12-1, HIGH);
}
