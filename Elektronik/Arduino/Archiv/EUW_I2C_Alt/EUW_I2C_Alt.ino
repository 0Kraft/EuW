#include <Arduino.h>
#include <Servo.h>
#include <Wire.h>

char t[10]={};//empty array where to put the numbers comming from the slave
volatile int Val; // varaible used by the master to sent data to the slave
long counter_ic=0;
#include <EasyTransferI2C.h>

//create object
EasyTransferI2C ET;

struct SEND_DATA_STRUCTURE{
  //put your variable definitions here for the data you want to send
  //THIS MUST BE EXACTLY THE SAME ON THE OTHER ARDUINO
  int16_t value;

};


//give a name to the group of data
SEND_DATA_STRUCTURE mydata;


//define slave i2c address
#define I2C_SLAVE_ADDRESS_A 9
#define I2C_SLAVE_ADDRESS_B 8
#define PIN_RPI_5V 10
#define PIN_BAT_MOT A1
#define PIN_BAT_CON A2

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
            value = analogRead(PIN_BAT_CON);
            }
          else{
            value = analogRead(PIN_BAT_MOT);
            }
          volt = ((value / 1023.0) * vcc)*2.82; // only correct if Vcc = 5.0 volts
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

void makegrab(String chkstring){

 
  if(chkstring.endsWith("A")) {
    Val = 3;
    Wire.beginTransmission (I2C_SLAVE_ADDRESS_A);
    Wire.write (Val);
     Wire.endTransmission ();

  

  }else{
 Val = 3;
    Wire.beginTransmission (I2C_SLAVE_ADDRESS_B);
    Wire.write (Val);
     Wire.endTransmission ();

  }





  sendstatus();
  delay(100);

  Serial.println("ROGER$");
 



}




void opengrab(String chkstring){
  
 
  if(chkstring.endsWith("A")) {
     Val = 2;
    Wire.beginTransmission (I2C_SLAVE_ADDRESS_A);
    Wire.write (Val);
     Wire.endTransmission ();
    
  
  }else{
     Val = 2;
    Wire.beginTransmission (I2C_SLAVE_ADDRESS_B);
    Wire.write (Val);
     Wire.endTransmission ();
    
   
  }
          
  sendstatus();
  delay(100);
  Serial.println("ROGER$");


}

void swap(){

    Val = 4;
    Wire.beginTransmission (8);
    Wire.write (Val);
     Wire.endTransmission ();
    
   delay(100);
   Val = 4;
    Wire.beginTransmission (9);
    Wire.write (Val);
     Wire.endTransmission ();
    
   delay(30);
  
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




mydata.value = 1001;

if(chkstring.endsWith("A")) {
     Val = 1;
    Wire.beginTransmission (I2C_SLAVE_ADDRESS_A);
    Wire.write (Val);
     Wire.endTransmission ();

}else{
    Val = 1;
    Wire.beginTransmission (I2C_SLAVE_ADDRESS_B);
    Wire.write (Val);
     Wire.endTransmission ();

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
  Wire.begin();
  //start the library, pass in the data details and the name of the serial port. Can be Serial, Serial1, Serial2, etc.
//  ET.begin(details(mydata), &Wire);
  
  
  Serial.begin(9600);

// in der Setup-Routine

 pinMode(PIN_RPI_5V, OUTPUT);
 digitalWrite(PIN_RPI_5V, HIGH);   //start RPI



 pinMode(A3, OUTPUT);

 pinMode(11, OUTPUT);
 pinMode(12, OUTPUT);


 pinMode(3, OUTPUT);
 pinMode(2, OUTPUT);

 pinMode(2, OUTPUT);




 delay(1000);




//  servoA1.attach(6); //analog pin 0   gripper
//  servoA2.attach(5); //analog pin 0   locking




Serial.println("START####$");







}





void loop()
{

     

     
      Wire.requestFrom(I2C_SLAVE_ADDRESS_A, 3);    // request 3 bytes from slave device #8
      bool question = false;
      //gathers data comming from slave
      int i=0; //counter for each bite as it arrives
        while (Wire.available()) { 
          t[i] = Wire.read(); // every character that arrives it put in order in the empty array "t"
          i=i+1;
        }
         String chk = t;
       if(chk.startsWith("100")) {
        question=true;
            
        Serial.println("I2C MESSAGE RETURN SUCCESS");
       
      }
      

      
     delay(50);
         chk = " ";
         t[10]={};
      Wire.requestFrom(I2C_SLAVE_ADDRESS_B, 3);    // request 3 bytes from slave device #8
      
      //gathers data comming from slave
        i=0; //counter for each bite as it arrives
        while (Wire.available()) { 
          t[i] = Wire.read(); // every character that arrives it put in order in the empty array "t"
          i=i+1;
        }

      
       chk = t;
       if(chk.startsWith("200")) {
         
          question=true;
         Serial.println("I2C MESSAGE RETURN SUCCESS 2");
         counter_ic=0;
        
      }

    
    
     if(question){
         delay(50);
         Val=5;
         Wire.beginTransmission (8);
         Wire.write (Val);
         Wire.endTransmission ();
         delay(50);
         
         Wire.beginTransmission (9);
         Wire.write (Val);
         Wire.endTransmission ();
         question=false;
     }
      

  /*
  
  int swapcheck =0;
  swapcheck = digitalRead(2);
  swapcheck = swapcheck + digitalRead(12);
  if(swapcheck>0){
  
     //checkswap
       mydata.value=1005;
            ET.sendData(I2C_SLAVE_ADDRESS_A);
            ET.sendData(I2C_SLAVE_ADDRESS_B);
            sendstatus();
            Serial.println("ROGER$");
      
  }
      //checkswap
      */

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



