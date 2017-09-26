#include "Arduino.h"



static char buffer[80];
static char mess[4];
unsigned long time;
static int pos = 0;
int p_state = 0;

const int buttonPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin
const int P_SHUT =  13;
// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status
int hstate=0;
int event=0;

int counter=0;





void setup() {
    Serial.begin(9600);
    Serial.println("Power On$");
  
   
       // in der Setup-Routine
  
    pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);

    digitalWrite(ledPin, HIGH);
 

  buttonState=LOW;
  event=0;
  delay(1000);
 Serial.println("Power On$");
    
}

int readline(int readch, char *buffer, int len)
{

  int rpos;
  
  if (readch > 0) {
    switch (readch) {
      case '\n': // Ignore new-lines
        break;
      case '\r': // Return on CR
        rpos = pos;
        pos = 0;  // Reset position index ready for next time
        return rpos;
        break;
      default:
        if (pos < len-1) {
          buffer[pos++] = readch;
          buffer[pos] = 0;
          
       
          
        }
        break;
    }
  }
  // No end of line has been found, so return -1.
  return -1;
}


void loop()
{
  
  buttonState = digitalRead(buttonPin);
  if(buttonState!=hstate){event=1;}
  
  int b_state = analogRead(A7);
  float voltage= b_state * (4.9 / 1023.0);

  counter++;
  if(counter>100000){
  counter=0;

    
  }
      
  if(voltage>4){
    
  //Serial.println(voltage);
  
     if (p_state==1) {
       
       
      //Serial.println("PI_SHUTDOWN");
         //   delay(10000);
       
      //digitalWrite(P_SHUT, LOW); // Einschalten des MOSFET
      p_state=0;
     }else if(p_state==0) { 
     // digitalWrite(P_SHUT, HIGH); // Einschalten des MOSFET
      p_state=1;
     }  
     
  delay(800);
  
  }

   if(event==1){
  if (buttonState == HIGH) {
    // turn LED on:
        digitalWrite(ledPin, HIGH);
        Serial.println("RPION$");
  } 

   if (buttonState == LOW) {
    // turn LED on:
        Serial.println("PI_SHUTDOWN$");
        delay(10000);
         
        digitalWrite(ledPin, LOW);
    
        delay(100);
  } 

  }

  event=0;
  hstate=buttonState;
  
 
  if (readline(Serial.read(), buffer, 80) > 0) {
    Serial.print("You entered: >");
    Serial.print(buffer);
    Serial.println("<");
    
    
    
    if(strcmp(buffer,"d2on")  == 0) {
       // digitalWrite(P_SHUT, HIGH); // Einschalten des MOSFET
           Serial.println("Light on$");
      
      
    }
    
     if(strcmp(buffer,"d2off")  == 0) {
        //digitalWrite(P_SHUT, LOW); // Einschalten des MOSFET
          Serial.println("Light off$");
      
    }
    
    if(strcmp(buffer,"time")  == 0) {
      
        time= millis();
        int minutes;
        minutes=(time/1000)/60;
          Serial.print("Uptime: ");
          Serial.print(minutes);
          Serial.println(" minutes$");
    }
    
    if(strcmp(buffer,"readbat")  == 0) {
            double Vcc = 4.9; // not necessarily true
            int value = analogRead(A6);
            double volt = ((value / 1023.0) * Vcc)*2; // only correct if Vcc = 5.0 volts
          Serial.print("Battery: ");
          Serial.print(volt);
          Serial.println(" Volt$");
    }
    
    if(strcmp(buffer,"shutdown")  == 0) {
        
            Serial.println("PI_SHUTDOWN$");
            delay(10000);
            digitalWrite(P_SHUT, LOW); // Einschalten des MOSFET
            delay(10000);
           // digitalWrite(P_SHUT, HIGH); // Einschalten des MOSFET
            
    }

     if(strcmp(buffer,"opengrabbow")  == 0) {
        
            Serial.println("--- Opening Sequence Bow ---");
            Serial.println("--- -------------------- ----");
            delay(100);
            Serial.println("Opening Sequence started....   ");
            Serial.println("");
            delay(100);
            Serial.println("  Unlocking Grabs Bow:    ");
            delay(100);
            Serial.println("        done");
            delay(100);
            Serial.println("  Rotating Grabs Bow:    ");
            delay(900);
            Serial.println("        done");
            delay(100);
            Serial.println("");
            Serial.println("Opening Sequence finished successfully ---");
            Serial.println("--- ----------$---------- ----");
           
        
            
    }
    
  }
}

