#include "Arduino.h"


int P_SHUT = 2;
static char buffer[80];
unsigned long time;
static int pos = 0;
int p_state = 0;
long current_time=0;
int under_v=0;




void setup() {
    Serial.begin(9600);
    Serial.println("Power On");
      pinMode(P_SHUT, OUTPUT);   // in der Setup-Routine
   
       // in der Setup-Routine
    digitalWrite(P_SHUT, HIGH); // Einschalten des MOSFET
                p_state=1;
   // digitalWrite(3, HIGH); // Einschalten des MOSFET
    //            p_state=1;
}


long readVcc() {
  /*
  // Read 1.1V reference against AVcc
  // set the reference to Vcc and the measurement to the internal 1.1V reference
  #if defined(__AVR_ATmega32U4__) || defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__)
    ADMUX = _BV(REFS0) | _BV(MUX4) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
  #elif defined (__AVR_ATtiny24__) || defined(__AVR_ATtiny44__) || defined(__AVR_ATtiny84__)
    ADMUX = _BV(MUX5) | _BV(MUX0);
  #elif defined (__AVR_ATtiny25__) || defined(__AVR_ATtiny45__) || defined(__AVR_ATtiny85__)
    ADMUX = _BV(MUX3) | _BV(MUX2);
  #else
    ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
  #endif  

  delay(2); // Wait for Vref to settle
  ADCSRA |= _BV(ADSC); // Start conversion
  while (bit_is_set(ADCSRA,ADSC)); // measuring

  uint8_t low  = ADCL; // must read ADCL first - it then locks ADCH  
  uint8_t high = ADCH; // unlocks both

  long result = (high<<8) | low;

  result = 1125300L / result; // Calculate Vcc (in mV); 1125300 = 1.1*1023*1000
  */
  long result = 5500;
  
  if(p_state==1) {
   result=5500; 
  }
  
  return result; // Vcc in millivolts
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

float readBat(){
  
   float Vcc = float(readVcc()); // not necessarily true
   float value = analogRead(A2);
   float volt = (float((value / 1023.0)) * float(Vcc/1000.0)); // only correct if Vcc = 5.0 volts
  
  return (volt*2.0);
}


void loop()
{
  
 
 // int b_state = analogRead(A0);
  
  
//  float voltage= b_state * (float(float(readVcc())/1000) / 1023.0);
  
  /*
  if(voltage>4){
    
            if (p_state==1) {
                 
                 
                Serial.println("PI_SHUTDOWN");
                      delay(10000);
                 
                digitalWrite(P_SHUT, LOW); // Einschalten des MOSFET
                p_state=0;
               }else if(p_state==0) { 
                digitalWrite(P_SHUT, HIGH); // Einschalten des MOSFET
                p_state=1;
               }  
               
            delay(800);
  
  }
  */
  
  
  if(millis()-current_time>12000){
  
  float rB=readBat();
  Serial.print("Battery: ");
  Serial.print(rB);
  Serial.println(" Volt");
  
  if(rB<3.78){
           under_v=under_v+1;
           Serial.println("Battery Low");
           
           if(under_v>1){
           Serial.println("Shutdown by Battery");
           delay(500);
           //Serial.println("PI_SHUTDOWN");
           delay(20000);
           //digitalWrite(P_SHUT, LOW); // Einschalten des MOSFET
           under_v=0;
           //p_state=0;
           }}else         
           {
            under_v=0; 
           }
           
  
  
  current_time=millis();
  
  }
  
  
  
  
    
 
  if (readline(Serial.read(), buffer, 80) > 0) {
    Serial.print("You entered: >");
    Serial.print(buffer);
    Serial.println("<");
    
    
    
    if(strcmp(buffer,"d2on")  == 0) {
        digitalWrite(P_SHUT, HIGH); // Einschalten des MOSFET
           Serial.println("Light on");
      
      
    }
    
     if(strcmp(buffer,"d2off")  == 0) {
        digitalWrite(P_SHUT, LOW); // Einschalten des MOSFET
          Serial.println("Light off");
      
    }
    
    if(strcmp(buffer,"time")  == 0) {
      
        time= millis();
        int minutes;
        minutes=(time/1000)/60;
          Serial.print("Uptime: ");
          Serial.print(minutes);
          Serial.println(" minutes");
    }
    
    if(strcmp(buffer,"readbat")  == 0) {
          
          Serial.print("Battery: ");
          Serial.print(readBat());
          Serial.println(" Volt");
    }
    
    if(strcmp(buffer,"shutdown")  == 0) {
        
            Serial.println("PI_SHUTDOWN");
            delay(20000);
           //digitalWrite(P_SHUT, LOW); // Einschalten des MOSFET
           
            
    }
    
  }
}

   
  
