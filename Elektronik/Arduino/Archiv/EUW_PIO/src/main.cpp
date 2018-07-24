#include <Arduino.h>
#include <Servo.h>

/// Communication with RPI
  static char buffer[80];
  unsigned long uptime;
  static int pos = 0;

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
///


/// Gripper A
  Servo servoA1; //
  int A1_ms;     // Servoposition in MS

  Servo servoA2; //
  int A2_ms;    // Servoposition in MS

  Servo servoA3; //
  int A3_ms=2350; // Servoposition in MS

  int gripperA=6; // Pin Gripper A Servo
  int lockingA=5; // Pin Locking A Servo
  int rotationA=4; // Pin Rotation A
  int sensorlockingA=3; // Pin Locking A Sensor
  int sensorgripperA=2; // Pin Locking A Sensor

  int statesensorlockingA=0; // State of Sensor Locking
  int statesensorgripperA=0; // State of Sensor Gripper

  int locking_positionA=1250;

  int lockedA = 1;
/// Gripper A

/// Gripper B
  Servo servoB1;
  int B1_ms;

  Servo servoB2;
  int B2_ms;

  Servo servoB3;
  int B3_ms=2350;

  int gripperB=11;
  int lockingB=10;
  int rotationB=9;
  int sensorlockingB=8;
  int sensorgripperB=7;
  int statesensorlockingB=0;
  int statesensorgripperB=0;

  int locking_positionB=1250;

  int lockedB= 1;

/// Greifer B


/// Servo Swap
  Servo servoC;
  int u_pos=2;
  int swap_time=2800;


long counter=0;

/// Read Battery Voltage
  float batread(int mitteln,int opt) {

      float vcc, value, volt, voltmittel=0;
      int i;

        for(i=0;i< mitteln;i++) {
          vcc = 4.43;    // Supply Voltage Arduino Nano - measured
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

void sendstatus(){
    Serial.print("UPDATE###");
    Serial.print(A1_ms);
    Serial.print(";");
    Serial.print(A2_ms);
    Serial.print(";");
    Serial.print(A3_ms);
    Serial.print(";");
    Serial.print(locking_positionA);
    Serial.print(";");
    Serial.print(lockedA);
    Serial.print(";");
    Serial.print(B1_ms);
    Serial.print(";");
    Serial.print(B2_ms);
    Serial.print(";");
    Serial.print(B3_ms);
    Serial.print(";");
    Serial.print(locking_positionB);
    Serial.print(";");
    Serial.print(lockedB);
    Serial.print(";");
    Serial.print(u_pos);
    Serial.print(";");
    Serial.print(swap_time);
    Serial.print(";");
    Serial.print(batread(100,1),3);
    Serial.print(";");
    Serial.print(batread(100,2),3);
    Serial.println(";$");

}

void sendtime(){

  uptime = millis();
  int minutes;
  minutes=(uptime/1000)/60;

  Serial.print("TIME#####"); // Send Message to RPI
  Serial.print(minutes);
  Serial.println("$"); // End of Signal

}

void sendshutdown(){

  Serial.println("SHUTDOWN#$");
  delay(10000);
  digitalWrite(A7, LOW); // Switch MOSFET / suppy voltage for RPI
  delay(10000);

}

void makegrab(String chkstring)

  {
  int checksuccess;
  int counttry; // number of grips tried

  counttry=0;

  if(chkstring.endsWith("A")) {


      while((checksuccess<2)&&(counttry<3)){

        checksuccess=0;
        counttry++;

         if(u_pos!=1){

                 servoA2.attach(lockingA);
                 delay(600);
                 servoA2.writeMicroseconds(1650);
                 A2_ms=1650;
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
        servoA1.writeMicroseconds(2360);
        A1_ms=2360;
        delay(500);
        servoA2.writeMicroseconds(locking_positionA+150);
        A2_ms=locking_positionA+150;
        delay(500);
        servoA1.detach();
        servoA2.detach();

        servoA2.attach(lockingA);
        delay(200);
        servoA2.writeMicroseconds(locking_positionA-80);
        A2_ms=locking_positionA;
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
          servoA1.writeMicroseconds(2360);
          A1_ms=2360;
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

    Serial.println("ROGER$");
    lockedA=1;

 }else{

    Serial.println("ROGER$");
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
                 servoB2.writeMicroseconds(1650);
                 B2_ms=1650;
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
        servoB2.writeMicroseconds(locking_positionB+150);
        B2_ms=locking_positionB+150;
        delay(500);
        servoB1.detach();
        servoB2.detach();

        servoB2.attach(lockingB);
        delay(200);
        servoB2.writeMicroseconds(locking_positionB-80);
        B2_ms=locking_positionB;
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

        Serial.println("ROGER$");
        lockedB=1;

     }else{

        Serial.println("ROGER$");
        lockedB=0;

    }



  }

  sendstatus();
  delay(100);

  Serial.println("ROGER$");
  lockedB=0;



}




void opengrab(String chkstring){

  if(chkstring.endsWith("A")) {


           if(u_pos!=1){

                  servoA2.attach(lockingA);

                  delay(600);
                  servoA2.writeMicroseconds(1650);
                  A2_ms=1750;
                  delay(1000);
                    servoA2.detach();
                  servoA1.attach(gripperA);
                    delay(600);
                  servoA1.writeMicroseconds(800);
                  delay(500);
                  A1_ms=800;
                  servoA1.detach();
                  lockedA=0;
                  Serial.println("ROGER$");
           }



     }else{

                if(u_pos!=2){
                  servoB2.attach(lockingB);
                  delay(600);
                  servoB2.writeMicroseconds(1650);
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
                  Serial.println("ROGER$");
                }


          }
          sendstatus();
          delay(100);
  Serial.println("ROGER$");


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
  delay(swap_time);
  servoC.detach();
  sendstatus();
  delay(100);
  Serial.println("ROGER$");

}

void set_swap(String chkstring){

  swap_time=chkstring.substring(9,13).toInt();

  sendstatus();
  delay(300);
  Serial.println("ROGER$");

}

void calibrate(String chkstring){


  opengrab(chkstring);

  if(chkstring.endsWith("A")) {

  servoA1.attach(gripperA);
  delay(200);
  servoA1.writeMicroseconds(2300);
  A1_ms=2300;
  delay(500);


  servoA1.detach();


      servoA2.attach(lockingA);
      delay(200);


      servoA2.writeMicroseconds(1300);
      A2_ms=1300;
      delay(250);

      while((A2_ms>650)&&(statesensorlockingA!=HIGH)){

        A2_ms=A2_ms-7;

        servoA2.writeMicroseconds(A2_ms);
        delay(35);
        statesensorlockingA = digitalRead(sensorlockingA);
        locking_positionA=A2_ms;

      }

      Serial.print("NEWCALA##");
      Serial.print(locking_positionA);
      Serial.println("$");
      servoA2.detach();

  }

  if(chkstring.endsWith("B")) {

  servoB1.attach(gripperB);
  delay(200);
  servoB1.writeMicroseconds(2300);
  B1_ms=2300;
  delay(500);


  servoB1.detach();


      servoB2.attach(lockingB);
      delay(200);


      servoB2.writeMicroseconds(1300);
      B2_ms=1300;
      delay(250);

      while((B2_ms>650)&&(statesensorlockingB!=HIGH)){

        B2_ms=B2_ms-5;

        servoB2.writeMicroseconds(B2_ms);
        delay(40);
        statesensorlockingB = digitalRead(sensorlockingB);
        locking_positionB=B2_ms;

      }

      Serial.print("NEWCALB##");
      Serial.print(locking_positionB);
      Serial.println("$");
      servoB2.detach();

  }

delay(100);

  Serial.println("ROGER$");


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

void init_EuW(String chkstring){



A1_ms=chkstring.substring(9,13).toInt();
A2_ms=chkstring.substring(14,18).toInt();
A3_ms=chkstring.substring(19,23).toInt();
locking_positionA=chkstring.substring(24,28).toInt();

B1_ms=chkstring.substring(29,33).toInt();
B2_ms=chkstring.substring(34,38).toInt();
B3_ms=chkstring.substring(39,43).toInt();
locking_positionB=chkstring.substring(44,48).toInt();

u_pos=chkstring.substring(49,50).toInt();

servoA3.attach(rotationA); //analog pin 0   rotation
servoB3.attach(rotationB); //analog pin 0
delay(200);
servoA3.writeMicroseconds(A3_ms);
servoB3.writeMicroseconds(B3_ms);
delay(600);
servoA3.detach(); //analog pin 0   rotation
servoB3.detach(); //analog pin 0   rotation

servoC.attach(A0);
delay(200);
if(u_pos==1){
  servoC.writeMicroseconds(2500);
}
else{
    servoC.writeMicroseconds(500);
}
delay(swap_time);
servoC.detach();




delay(100);

Serial.println("ROGER$");


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
sendstatus();
delay(100);
Serial.println("ROGER$");

}

void switchir(String chkstring){


      if(chkstring.endsWith("0")) {

          digitalWrite(13, LOW);   //disable IR


      }

      if(chkstring.endsWith("1")) {

          digitalWrite(13, HIGH);   //enable IR

      }

      delay(100);

      Serial.println("ROGER$");


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
sendstatus();
delay(100);
Serial.println("ROGER$");

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
/*
char tbs[4];

sprintf(tbs,"%04d", A3_ms);

Serial.print("POSITION#A");
Serial.print(A3_ms);
Serial.println("$");

sprintf(tbs,"%04d", B3_ms);
Serial.print("POSITION#B");
Serial.print(B3_ms);
Serial.println("$");
*/
sendstatus();
delay(100);
Serial.println("ROGER$");
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
 pinMode(13, OUTPUT);



 delay(1000);




//  servoA1.attach(6); //analog pin 0   gripper
//  servoA2.attach(5); //analog pin 0   locking




Serial.println("START####$");







}





void loop()
{


  if (readline(Serial.read(), buffer, 80) > 0) {

      String checkstring = buffer;

      if(checkstring.startsWith("readbat##"))     {
        sendbat(checkstring);
      }

      if(checkstring.startsWith("switchir#"))     {
        switchir(checkstring);
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

    if(checkstring.startsWith("calibration")) {
    calibrate(checkstring);
    }

    if(checkstring.startsWith("init#####")) {
    init_EuW(checkstring);
    }

    if(checkstring.startsWith("set_swap#")) {
    set_swap(checkstring);
    }





  }
}
