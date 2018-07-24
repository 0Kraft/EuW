const int motorPin1 = 8;  // Blue   - In 1
const int motorPin2 = 9;  // Pink   - In 2
const int motorPin3 = 10; // Yellow - In 3
const int motorPin4 = 11; // Orange - In 4
                          // Red    - pin 5 (VCC)

int start = 0;

unsigned int lowSpeed  = 6000; // Notabene: nicht über 16000
unsigned int highSpeed =  2000;
void setup() {
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
}

void loop()
{ unsigned long n = millis() / 3000; // 3 Sekunden


  switch(n % 8)
  { case 0: stop();    start=0;            break;
    case 1: rechtsrum(highSpeed);  break;
    case 2: stop(); start=0;              break;
    case 3: linksrum(highSpeed);   break;
    case 4: stop();   start=0;             break;
    case 5: rechtsrum(highSpeed); break;
    case 6: stop();    start=0;            break;
    case 7: linksrum(highSpeed);  break;
  }
}

void rechtsrum(unsigned int motorSpeed)
{ // 1
start++;
  if(start<6)
  {
    motorSpeed=lowSpeed;
  }else{
    motorSpeed=highSpeed;
  }
   
  digitalWrite(motorPin4, HIGH);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin1, LOW);
  delayMicroseconds(motorSpeed);

  // 2
  digitalWrite(motorPin4, HIGH);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin1, LOW);
  delayMicroseconds(motorSpeed);

  // 3
  digitalWrite(motorPin4, LOW);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin1, LOW);
  delayMicroseconds(motorSpeed);

  // 4
  digitalWrite(motorPin4, LOW);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin2, HIGH);
  digitalWrite(motorPin1, LOW);
  delayMicroseconds(motorSpeed);

  // 5
  digitalWrite(motorPin4, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin2, HIGH);
  digitalWrite(motorPin1, LOW);
  delayMicroseconds(motorSpeed);

  // 6
  digitalWrite(motorPin4, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin2, HIGH);
  digitalWrite(motorPin1, HIGH);
  delayMicroseconds(motorSpeed);

  // 7
  digitalWrite(motorPin4, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin1, HIGH);
  delayMicroseconds(motorSpeed);

  // 8
  digitalWrite(motorPin4, HIGH);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin1, HIGH);
  delayMicroseconds(motorSpeed);
}

void linksrum(unsigned int motorSpeed)
{ // 1

  start++;
  if(start<6)
  {
    motorSpeed=lowSpeed;
  }else{
    motorSpeed=highSpeed;
  }
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
  delayMicroseconds(motorSpeed);

  // 2
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, HIGH);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
  delayMicroseconds(motorSpeed);

  // 3
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, HIGH);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
  delayMicroseconds(motorSpeed);

  // 4
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, HIGH);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin4, LOW);
  delayMicroseconds(motorSpeed);

  // 5
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin4, LOW);
  delayMicroseconds(motorSpeed);

  // 6
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin4, HIGH);
  delayMicroseconds(motorSpeed);

  // 7
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, HIGH);
  delayMicroseconds(motorSpeed);

  // 8
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, HIGH);
  delayMicroseconds(motorSpeed);
}

void stop()
{ digitalWrite(motorPin4, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin1, LOW);
}
