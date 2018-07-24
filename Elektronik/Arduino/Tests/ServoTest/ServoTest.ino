#include <Servo.h>

Servo myservo; 
int pos = 600;    // variable to store the servo position



String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

void setup() {
  // initialize serial:
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
  myservo.attach(9); 
  myservo.writeMicroseconds(pos);  
}

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    Serial.println(inputString);
    myservo.attach(9);
    int adder=1;
    int aim = inputString.toInt();
    // clear the string:
    if(aim>pos){
      adder=30;
      Serial.println("+");
    }else{
      adder=-30;
      Serial.println("-");
      }
      
    Serial.println(abs(aim-pos));
    
    while(abs(aim-pos)>22){
    pos=pos+adder;
    myservo.writeMicroseconds(pos);  
    delay(5);
    Serial.println(abs(aim-pos));
     Serial.println(pos);
      Serial.println(aim);
      Serial.println("##");
    
    }
    myservo.writeMicroseconds(aim);  
    Serial.println(pos);
    pos = aim;
    inputString = "";
    stringComplete = false;
    delay(500);
    myservo.detach();
  }
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}


