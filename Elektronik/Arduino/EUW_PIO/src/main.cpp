#include <Arduino.h>
#include <Servo.h>

static char buffer[80];
unsigned long time;
static int pos = 0;

int u_pos=2;

Servo servoA1;
int A1_ms;
Servo servoA2;
int A2_ms;
Servo servoA3;
int A3_ms=2350;


Servo servoB1;
int B1_ms;
Servo servoB2;
int B2_ms;
Servo servoB3;
int B3_ms=2350;

int gripperA=6;
 int    lockingA=5;
int     rotationA=4;
int sensorlockingA=3;
int sensorgripperA=2;
int statesensorlockingA=0;
int statesensorgripperA=0;


int     gripperB=11;
int     lockingB=10;
int     rotationB=9;
int sensorlockingB=8;
int sensorgripperB=7;
int statesensorlockingB=0;
int statesensorgripperB=0;





int lockedA = 1;
int lockedB= 1;

Servo servoC;

long counter=0;

float batread(int mitteln,int opt) {

float vcc, value, volt, voltmittel=0;
int i;

  for(i=0;i< mitteln;i++) {
    vcc = 4.43;    // Versorgungsspannung ermitteln
    if(opt==1){
      value = analogRead(A1);
      }
    else{
      value = analogRead(A2);
      }
    volt = ((value / 1023.0) * vcc)*2; // only correct if Vcc = 5.0 volts
    voltmittel += volt;                               // Summieren
  }
  return voltmittel/mitteln;
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

void sendtime(){

  time= millis();
  int minutes;
  minutes=(time/1000)/60;
  Serial.print("TIME#####");
  Serial.print(minutes);
  Serial.println("$");

}

void sendshutdown(){

  Serial.println("SHUTDOWN#$");
  delay(10000);
  digitalWrite(A7, LOW); // Einschalten des MOSFET
  delay(10000);

}

void makegrab(String chkstring)

  {
  int checksuccess;
  int counttry;
  counttry=0;


  if(chkstring.endsWith("A")) {


      while((checksuccess<2)&&(counttry<3)){

        checksuccess=0;
        counttry++;

         if(u_pos!=1){

                 servoA2.attach(lockingA);
                 delay(600);
                 servoA2.writeMicroseconds(1250);
                 A2_ms=1250;
                 delay(1000);
                 servoA2.detach();
                 servoA1.attach(gripperA);
                 delay(600);
                 servoA1.writeMicroseconds(850);
                 delay(500);
                 A1_ms=850;
                 servoA1.detach();

                // Serial.println("Gripper A Open : GO $");
              }



        servoA1.attach(gripperA);
        servoA2.attach(lockingA);
        delay(200);
        servoA1.writeMicroseconds(2330);
        A1_ms=2330;
        delay(500);
        servoA2.writeMicroseconds(900);
        A2_ms=900;
        delay(500);
        servoA1.detach();
        servoA2.detach();

        servoA2.attach(lockingA);
        delay(200);
        servoA2.writeMicroseconds(850);
        A2_ms=850;
        delay(250);
        statesensorlockingA = digitalRead(sensorlockingA);
        servoA2.detach();

        if(statesensorlockingA==HIGH){
               checksuccess++;
              // Serial.println("Locking A : GO $");
          }else{
                //Serial.println("LOCKING A CHECK : FAIL $");
                  delay(400);
          }

        if(checksuccess==1){

          servoA1.attach(gripperA);
          delay(200);
          servoA1.writeMicroseconds(2330);
          A1_ms=2330;
          delay(200);
          statesensorgripperA = digitalRead(sensorgripperA);
          servoA1.detach();
          if(statesensorgripperA==HIGH){
               checksuccess++;
                //Serial.println("GRIP A CHECK : GO $");
          }else{
                //Serial.println("GRIP A CHECK : FAIL $");
                delay(400);
          }
        }

  }

  if(checksuccess==2){

    Serial.print("GRIPA####");
    Serial.print("1");
    Serial.println("$");
    lockedA=1;

 }else{

    Serial.print("GRIPA####");
    Serial.print("0");
    Serial.println("$");
    lockedA=0;
}


}




if(chkstring.endsWith("B")) {

       while((checksuccess<2)&&(counttry<3)){

        checksuccess=0;
        counttry++;

         if(u_pos!=2){

                 servoB2.attach(lockingB);
                 delay(600);
                 servoB2.writeMicroseconds(1750);
                 B2_ms=1750;
                 delay(1000);
                 servoB2.detach();
                 servoB1.attach(gripperB);
                 delay(600);
                 servoB1.writeMicroseconds(850);
                 delay(500);
                 B1_ms=850;
                 servoB1.detach();

                 //Serial.println("Gripper B Open : GO $");
              }



        servoB1.attach(gripperB);
        servoB2.attach(lockingB);
        delay(200);
        servoB1.writeMicroseconds(2330);
        B1_ms=2330;
        delay(500);
        servoB2.writeMicroseconds(1150);
        B2_ms=1150;
        delay(500);
        servoB1.detach();
        servoB2.detach();

        servoB2.attach(lockingB);
        delay(200);
        servoB2.writeMicroseconds(900);
        B2_ms=900;
        delay(250);
        statesensorlockingB = digitalRead(sensorlockingB);
        servoB2.detach();

        if(statesensorlockingB==HIGH){
               checksuccess++;
               //Serial.println("Locking B : GO $");
          }else{
                //Serial.println("LOCKING B CHECK : FAIL $");
                  delay(400);
          }

        if(checksuccess==1){

          servoB1.attach(gripperB);
          delay(200);
          servoB1.writeMicroseconds(2330);
          B1_ms=2330;
          delay(200);
          statesensorgripperB = digitalRead(sensorgripperB);
          servoB1.detach();
          if(statesensorgripperB==HIGH){
               checksuccess++;
                //Serial.println("GRIP B CHECK : GO $");
          }else{
                //Serial.println("GRIP B CHECK : FAIL $");
                delay(400);
          }
        }

      }

      if(checksuccess==2){

        Serial.print("GRIPB####");
        Serial.print("1");
        Serial.println("$");
        lockedB=1;

     }else{

        Serial.print("GRIPB####");
        Serial.print("0");
        Serial.println("$");
        lockedB=0;

    }



  }



}




void opengrab(String chkstring){

  if(chkstring.endsWith("A")) {


           if(u_pos!=1){

                  servoA2.attach(lockingA);

                  delay(600);
                  servoA2.writeMicroseconds(1550);
                  A2_ms=1550;
                  delay(1000);
                    servoA2.detach();
                  servoA1.attach(gripperA);
                    delay(600);
                  servoA1.writeMicroseconds(800);
                  delay(500);
                  A1_ms=800;
                  servoA1.detach();
                  lockedA=0;
           }



     }else{

                if(u_pos!=2){
                  servoB2.attach(lockingB);
                  delay(600);
                  servoB2.writeMicroseconds(1750);
                   delay(600);
                   servoB2.detach();
                  B2_ms=1550;
                  delay(500);

                   servoB1.attach(gripperB);
                   delay(600);
                  servoB1.writeMicroseconds(800);
                  delay(500);
                  B1_ms=800;
                  servoB1.detach();
                  lockedB=0;
                }


          }



}

void swap(){

  servoC.attach(A0);
  delay(200);
  if(u_pos==2){
    servoC.writeMicroseconds(2500);
    u_pos=1;
  }
  else{
    servoC.writeMicroseconds(500);
    u_pos=2;
  }
  delay(1800);
  servoC.detach();

}

void sendbat(String chkstring){

  if(chkstring.endsWith("C")) {

               Serial.print("BATTERY##C");
               Serial.print(batread(100,1),3);
               Serial.println("$");
  }else{
               Serial.print("BATTERY##M");
               Serial.print(batread(100,2),3);
               Serial.println("$");

  }

}


void turn(String chkstring){

  String turnval = "1500";

  turnval=chkstring.substring(9,13);

   Serial.print(turnval);
Serial.println("$");
   delay(1000);

if(chkstring.endsWith("A")) {
             int aim = turnval.toInt();
             servoA3.attach(rotationA);
             delay(500);

             int adder=0;

            if(aim<A3_ms) {adder=-7;}
            if(aim>A3_ms) {adder=7;}

             while(abs(aim-A3_ms)> 15){

              A3_ms = A3_ms+adder;
              servoA3.writeMicroseconds(A3_ms);
              delay(15);
             }

             servoA3.writeMicroseconds(aim);
             delay(1200);
             A3_ms=aim;
             servoA3.detach();

}else{
            int aim = turnval.toInt();

            servoB3.attach(rotationB);
            delay(500);

             int adder=0;

             if(aim<B3_ms) {adder=-7;}
            if(aim>B3_ms) {adder=7;}

           while(abs(aim-B3_ms)> 15 ){

              B3_ms = B3_ms+adder;
              servoB3.writeMicroseconds(B3_ms);
              delay(15);


             }

            servoB3.writeMicroseconds(aim);
            delay(1200);
            B3_ms=aim;
            servoB3.detach();

}

}

void turn_auto(String chkstring){


if(chkstring.endsWith("A")) {
            int aim =1500;
             if (A3_ms>1500){
               aim=600;
             }else{
               aim=2350;
             }

             servoA3.attach(rotationA);
             delay(500);

             int adder=0;

            if(aim<A3_ms) {adder=-9;}
            if(aim>A3_ms) {adder=9;}

             while(abs(aim-A3_ms)> 15){

              A3_ms = A3_ms+adder;
              servoA3.writeMicroseconds(A3_ms);
              delay(20);
             }

             servoA3.writeMicroseconds(aim);
             delay(1200);
             A3_ms=aim;
             servoA3.detach();

}else{
          int aim =1500;
           if (B3_ms>1500){
             aim=600;
           }else{
             aim=2350;
           }

            servoB3.attach(rotationB);
            delay(500);

             int adder=0;

             if(aim<B3_ms) {adder=-9;}
            if(aim>B3_ms) {adder=9;}

           while(abs(aim-B3_ms)> 15 ){

              B3_ms = B3_ms+adder;
              servoB3.writeMicroseconds(B3_ms);
              delay(20);


             }

            servoB3.writeMicroseconds(aim);
            delay(1200);
            B3_ms=aim;
            servoB3.detach();

}

}

void turnadder(String chkstring){

  int amount;

if(chkstring.endsWith("+")){
  amount =70;
}else{
  amount=-70;
}

if(u_pos==1) {

                servoA3.attach(rotationA);
                delay(500);
                 A3_ms = A3_ms+amount;
                    if(A3_ms>2500) A3_ms=2500;
                 servoA3.writeMicroseconds(A3_ms);
                 delay(15);



                delay(500);

                servoA3.detach();

   }else{
          servoB3.attach(rotationB);
                delay(500);

                B3_ms = B3_ms+amount;
                   if(B3_ms>2500) B3_ms=2500;
                 servoB3.writeMicroseconds(B3_ms);
                 delay(15);



                delay(500);

                servoB3.detach();

}

char tbs[4];

sprintf(tbs,"%04d", A3_ms);

Serial.print("POSITION#A");
Serial.print(A3_ms);
Serial.println("$");

sprintf(tbs,"%04d", B3_ms);
Serial.print("POSITION#B");
Serial.print(B3_ms);
Serial.println("$");

}


void sendstatus(){

Serial.print("UPDATE###");
Serial.print(batread(100,1),3);
Serial.print(";");
Serial.print(batread(100,2),3);
Serial.print(";");
Serial.print(lockedA);
Serial.print(";");
Serial.print(lockedB);
Serial.print(";");
Serial.print(A3_ms);
Serial.print(";");
Serial.print(B3_ms);
Serial.print(";");
Serial.print(u_pos);
Serial.println(";$");

}





void setup() {
  Serial.begin(9600);

// in der Setup-Routine

 pinMode(A7, OUTPUT);
 digitalWrite(A7, HIGH);   //start RPI

 pinMode(2, INPUT); //
 pinMode(3, INPUT);
 pinMode(4, OUTPUT);
 pinMode(5, OUTPUT);
 pinMode(6, OUTPUT);

 pinMode(7, INPUT);
 pinMode(8, INPUT);
 pinMode(9, OUTPUT);
 pinMode(10, OUTPUT);
 pinMode(11, OUTPUT);



 delay(1000);




//  servoA1.attach(6); //analog pin 0   gripper
//  servoA2.attach(5); //analog pin 0   locking
 servoA3.attach(4); //analog pin 0   rotation


 //servoB1.attach(11); //analog pin 0
// servoB2.attach(10); //analog pin 0
 servoB3.attach(9); //analog pin 0


servoA3.writeMicroseconds(2350);
servoB3.writeMicroseconds(2350);
delay(800);
servoA3.detach(); //analog pin 0   rotation
servoB3.detach(); //analog pin 0   rotation

  servoC.attach(A0);
                       delay(200);

                       servoC.writeMicroseconds(500);
                       delay(1800);

                       servoC.detach();
}





void loop()
{


  if (readline(Serial.read(), buffer, 80) > 0) {

      String checkstring = buffer;

      if(checkstring.startsWith("readbat##"))     {
        sendbat(checkstring);
      }


     if(checkstring.startsWith("checklock"))     {
       //checklock();
      }

      if(checkstring.startsWith("time#####"))     {
         sendtime();
       }

     if(checkstring.startsWith("shutdown#")) {
       sendshutdown();
     }


     if(checkstring.startsWith("checkgrab")) {
       //checkgrab(checkstring);
     }

     if(checkstring.startsWith("opengrab#")) {
       opengrab(checkstring);

     }

     if(checkstring.startsWith("swap#####")) {
       swap();
    }

    if(checkstring.startsWith("closegrab")) {
       makegrab(checkstring);
    }

    if(checkstring.startsWith("turnauto#")) {
       turn_auto(checkstring);
    }

    if(checkstring.startsWith("turnadder")) {
      turnadder(checkstring);
    }

    if(checkstring.startsWith("getstatus")) {
    sendstatus();
    }

    delay(100);
    Serial.println("ROGER$");


  }
}
