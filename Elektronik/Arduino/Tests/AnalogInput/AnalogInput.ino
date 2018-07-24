/*
  Analog Input
 Demonstrates analog input by reading an analog sensor on analog pin 0 and
 turning on and off a light emitting diode(LED)  connected to digital pin 13.
 The amount of time the LED will be on and off depends on
 the value obtained by analogRead().

 The circuit:
 * Potentiometer attached to analog input 0
 * center pin of the potentiometer to the analog pin
 * one side pin (either one) to ground
 * the other side pin to +5V
 * LED anode (long leg) attached to digital output 13
 * LED cathode (short leg) attached to ground

 * Note: because most Arduinos have a built-in LED attached
 to pin 13 on the board, the LED is optional.


 Created by David Cuartielles
 modified 30 Aug 2011
 By Tom Igoe

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/AnalogInput

 */

int sensorPin = A6;    // select the input pin for the potentiometer

int sensorValue = 0;  // variable to store the value coming from the sensor

float ACS712read(int mitteln) {
// Den ACS712 Stromsensor auslesen
// Sens ist im Datenblatt auf Seite 2 mit 185 angegeben.
// Für meinen Sensor habe ich 186 ermittelt bei 5.0V Vcc.
// Sens nimmt mit ca. 38 pro Volt VCC ab.
//
// 3,3V muss zu Analog Eingang 5 gebrückt werden.
// Der Sensoreingang ist Analog 1
//
// Parameter mitteln : die Anzahl der Mittlungen
// 
// Matthias Busse 9.5.2014 Version 1.0

float sense=100.0;           // mV/A Datenblatt Seite 2
float sensdiff=39.0;         // sense nimmt mit ca. 39/V Vcc ab. 
float vcc, vsensor, amp, ampmittel=0;
int i;
  
  for(i=0;i< mitteln;i++) {
   vcc = (float) 3.30 / analogRead(A5) * 1023.0;    // Versorgungsspannung ermitteln
    vsensor = (float) analogRead(A1) * vcc / 1023.0; // Messwert auslesen
    vsensor = (float) vsensor - (vcc/2);            // Nulldurchgang (vcc/2) abziehen
    sense = (float) 100 - ((5.00-vcc)*sensdiff);  // sense für Vcc korrigieren 
    amp = (float) vsensor /sense *1000 ;            // Ampere berechnen
    ampmittel += amp;                               // Summieren
  }
  return ampmittel/mitteln;
}

float batread(int mitteln,int opt) {

float vcc, value, volt, voltmittel=0;
int i;

  for(i=0;i< mitteln;i++) {
    vcc = 5.5;
    if(opt==1){
      value = analogRead(sensorPin);
      }
    else{
      value = analogRead(A2);
      }
    volt = ((value / 1023.0) * vcc)*2; // only correct if Vcc = 5.0 volts
    voltmittel += volt;                               // Summieren
  }
  return voltmittel/mitteln;
}

void setup() {
  // declare the ledPin as an OUTPUT:
Serial.begin(9600);
}

void loop() {
  // read the value from the sensor:
  
  // turn the ledPin on
 
  // stop the program for <sensorValue> milliseconds:
  
  Serial.print("sendana##");
  Serial.println(batread(100,1),3);

  delay(2000);

  Serial.print("sendamp##");
  Serial.println(ACS712read(100),3);
 
  // turn the ledPin off:
  delay(2000);
 
  
}
