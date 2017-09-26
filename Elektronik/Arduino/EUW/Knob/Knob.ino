/*
 Controlling a servo position using a potentiometer (variable resistor)
 by Michal Rinott <http://people.interaction-ivrea.it/m.rinott>

 modified on 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Knob
*/

#include <Servo.h>

Servo gripper;  // create servo object to control a servo
Servo locking;  // create servo object to control a servo
Servo rotation;  // create servo object to control a servo

int tasterstatus1 = 0;
int tasterstatus2 = 0;

void setup() {
  gripper.attach(2);  // attaches the servo on pin 9 to the servo object
   locking.attach(4);  // attaches the servo on pin 9 to the servo object
    rotation.attach(5);  // attaches the servo on pin 9 to the servo object

    pinMode(12, INPUT);
     pinMode(11, INPUT);
}

void loop() {

  tasterstatus1=digitalRead(11);
  if (tasterstatus1 == HIGH){

   locking.writeMicroseconds(1550);
    delay(2000);
    
  }

   tasterstatus2=digitalRead(12);
  if (tasterstatus2 == HIGH){

   locking.writeMicroseconds(1200);
    delay(2000);
    
  }

 
   

  /*

  
  //openlock
  locking.writeMicroseconds(1550);
   delay(300);
  //opengripper
  gripper.writeMicroseconds(700);
 delay(4000);
    gripper.writeMicroseconds(2300);
   delay(1500);

   locking.writeMicroseconds(1200);
   delay(2000);

   
rotation.attach(5);
    delay(100);
   
 rotation.writeMicroseconds(2400);
   delay(500);
rotation.detach();
    delay(3500);
   

    locking.writeMicroseconds(1550);
   delay(300);
  //opengripper
  gripper.writeMicroseconds(700);
 delay(4000);
    gripper.writeMicroseconds(2300);
   delay(1500);

   locking.writeMicroseconds(1200);
   delay(2000);

 rotation.attach(5);
    delay(100);
   
 rotation.writeMicroseconds(600);
   delay(500);
rotation.detach();
    delay(3500);
   
   */

 
  
}

