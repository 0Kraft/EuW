#include <Wire.h>
#include <EasyTransferI2C.h>
#include <Servo.h>
//create object
//EasyTransferI2C ET;

char t[10]; //empty array where to put the numbers going to the master
volatile int Val; // variable used by the master to sent data to the slave
int sendmsg = 000;
/// Gripper A
  Servo servoA1; //
  int A1_ms;     // Servoposition in MS

  Servo servoA2; //
  int A2_ms;    // Servoposition in MS
  int timertest=0;
  Servo servoA3; //
  int A3_ms=1805; // Servoposition in MS

  Servo servoswap; //

  int gripperA=4; // Pin Gripper A Servo
  int lockingA=3; // Pin Locking A Servo
  int rotationA=2; // Pin Rotation A
  int pinswap=17; // Pin Rotation A
  int sensorlockingA=7; // Pin Locking A Sensor
  int sensorgripperA=8; // Pin Locking A Sensor
  int sensorswap=9; // Pin Locking A Sensor
  int v_sensors=6; // Pin Locking A Sensor

  int statesensorlockingA=0; // State of Sensor Locking
  int statesensorgripperA=0; // State of Sensor Gripper

  int locking_positionA=2000;
  int new_ms = 2000;

  int lockedA = 1;
/// Gripper A

  int swap_direction = 1;
  bool swap_active = false;

/*
struct RECEIVE_DATA_STRUCTURE{
  //put your variable definitions here for the data you want to receive
  //THIS MUST BE EXACTLY THE SAME ON THE OTHER ARDUINO
  int16_t value;
 
  
};


//give a name to the group of data
RECEIVE_DATA_STRUCTURE mydata;
*/
//define slave i2c address
#define I2C_SLAVE_ADDRESS 9

void setup(){
  Wire.begin(I2C_SLAVE_ADDRESS);
  Serial.begin(9600);
  Serial.println("I2C Test");
  //start the library, pass in the data details and the name of the serial port. Can be Serial, Serial1, Serial2, etc. 
  
 //ET.begin(details(mydata), &Wire);
  //define handler function on receiving data
  //Wire.onReceive(receive);
 
  pinMode(sensorlockingA, INPUT);
  pinMode(sensorgripperA, INPUT);
  pinMode(v_sensors, OUTPUT);

   //servoA3.attach(rotationA);
   //          delay(2);
   //servoA3.writeMicroseconds(A3_ms);

   Wire.onRequest(requestEvent); // fucntion to run when asking for data
  Wire.onReceive(receiveEvent); // what to do when receiving data

 
   
}

void loop() {
   if(swap_active){

     int swapstate = 0;
     swapstate = digitalRead(sensorswap);
     if(swapstate==HIGH){
          // swap_active=false;
         //  servoswap.detach();
        //   digitalWrite(v_sensors, LOW);
          // swap_direction=swap_direction*(-1);
        

            sendmsg = 100; //plug a potentiometer or a resistor to pin A0, so you can see data being transfer
           
          
     }

     
     
  }
  //check and see if a data packet has come in. 
// mydata.value=0;
// if(ET.receiveData()){
if(Val!=0){
    
             Serial.println("got message");

                  if(Val == 5)// endswap
                    {  
                                                                                     
                           sendmsg = 000;
                           swap_active=false;
                          
                           digitalWrite(v_sensors, LOW);
                           swap_direction=swap_direction*(-1);

                           
                          
                           if(swap_direction==1)
                            {
                                servoswap.writeMicroseconds(2200);
                              
                            }else{
                            
                                servoswap.writeMicroseconds(900);
                            }
                            delay (350);

                             servoswap.detach();
                            
                           
                           
                   
                     }

                  if(Val == 4)// swap
                    {  
                        
                           Serial.println("swap");
                           servoswap.attach(pinswap);
                           delay(2);
                           if(swap_direction==1)
                            {
                                servoswap.writeMicroseconds(2200);
                              
                            }else{
                            
                                servoswap.writeMicroseconds(900);
                            }
                                  
                           swap_active=true;
                           digitalWrite(v_sensors, HIGH);
                   
                     }
             
                  if(Val == 1)// turn
                        {
                           Serial.println("turn_auto");
                          int turn_aim = 0;
                           if(A3_ms>1500)
                            {
                              turn_aim = 700;
                               
                            }else{
                              turn_aim = 1800;
                             
                            }

                            servoA3.attach(rotationA);

                           if(turn_aim>A3_ms) {

                            while(A3_ms<turn_aim){

                                A3_ms=A3_ms+1;
                                servoA3.writeMicroseconds(A3_ms);
                                delay(12);
                            }
                            A3_ms=turn_aim;
                             servoA3.writeMicroseconds(A3_ms);
                            delay(300);
                            
                           }else{

                            while(A3_ms>turn_aim){

                                A3_ms=A3_ms-1;
                                servoA3.writeMicroseconds(A3_ms);
                                delay(12);
                            }
                            A3_ms=turn_aim;
                             servoA3.writeMicroseconds(A3_ms);
                            delay(300);
                            
                           }
                                  
                                                    
                          
                           servoA3.detach();
                   
                   }
                    

                if(Val == 2)// endswap{
                  {        
                             Serial.println("opengrab");
                
                             servoA2.attach(lockingA);
                             delay(600);
                             servoA2.writeMicroseconds(800);
                             A2_ms=800;
                             delay(1000);
                             servoA2.detach();
                             servoA1.attach(gripperA);
                             delay(600);
                             servoA1.writeMicroseconds(500);
                             delay(650);
                             A1_ms=500;
                             servoA1.detach();
                             lockedA=0;
                 
                }

                 if(Val == 3)// endswap{
                  {
                            Serial.println("closegrab");

                             int checksuccess;
                             int counttry=0; // number of grips tried

                             while((checksuccess<2)&&(counttry<3)){

                                     checksuccess=0;
                                     counttry++;       
  
                                     servoA2.attach(lockingA);
                                     delay(600);
                                     servoA2.writeMicroseconds(800);
                                     A2_ms=800;
                                     delay(1000);
                                     servoA2.detach();
                                     servoA1.attach(gripperA);
                                     delay(600);
                                     servoA1.writeMicroseconds(550);
                                     delay(650);
                                     A1_ms=550;
                                     servoA1.detach();
                    
                                     Serial.println("Gripper A Open : GO $");
                                     digitalWrite(v_sensors, HIGH);
                                     servoA1.attach(gripperA);
                                     servoA2.attach(lockingA);
                                     delay(200);
                                     servoA1.writeMicroseconds(2250);
                                     A1_ms=2250;
                                     delay(500);
                                     servoA2.writeMicroseconds(locking_positionA);
                                     A2_ms=locking_positionA;
                                     delay(500);
                                     servoA1.detach();
                                     servoA2.detach();

                                      servoA2.attach(lockingA);
                                      delay(200);
                                      servoA2.writeMicroseconds(locking_positionA);
                                      A2_ms=locking_positionA;
                                      delay(200);
                                     
                                      delay(50);
                                      statesensorlockingA = digitalRead(sensorlockingA);
                                      servoA2.detach();
                                     

                                      if(statesensorlockingA==HIGH){
                                             checksuccess++;
                                             Serial.println("Locking A : GO $");
                                        }else{
                                             Serial.println("LOCKING A CHECK : FAIL $");
                                             delay(400);
                                        }

                                      if(checksuccess==1){

                                          servoA1.attach(gripperA);
                                          delay(200);
                                          servoA1.writeMicroseconds(2250);
                                          A1_ms=2250;
                                          delay(150);
                                         
                                          delay(50);
                                          statesensorgripperA = digitalRead(sensorgripperA);
                                          servoA1.detach();
                                          digitalWrite(v_sensors, LOW);
                                          if(statesensorgripperA==HIGH){
                                               checksuccess++;
                                                Serial.println("GRIP A CHECK : GO $");
                                          }else{
                                                Serial.println("GRIP A CHECK : FAIL $");
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

                             Val=0;
                             
           

              }
  
              
   
  
     
    
}

void requestEvent() {

dtostrf(sendmsg, 3, 0, t); //convers the float or integer to a string. (floatVar, minStringWidthIncDecimalPoint, numVarsAfterDecimal, empty array);
   
Wire.write(t);
 
           
}

// what to do when receiving data from master
void receiveEvent(int howMany)
{Val = Wire.read();}


