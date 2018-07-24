#include <ESP8266WiFi.h>
 
const char* ssid = "FirstAidNet";
const char* password = "tempnet19";
 static char buffer[80];
unsigned long time2;
static int pos = 0;
String buf="buf";

int ledPin = 13; // GPIO13
WiFiServer server(80);

float val=0;
float valamp=0;

/// Read Battery Voltage
  float batread(int mitteln) {

      float vcc, value, volt, voltmittel=0;
      int i;

        for(i=0;i< mitteln;i++) {
          vcc = 5.3;    // Supply Voltage Arduino Nano - measured
         
          value = analogRead(A0);
            
          volt = ((value / 1023.0) * vcc)*17.3; // only correct if Vcc = 5.0 volts
          voltmittel += volt;                               // Summieren
        }

        return voltmittel/mitteln;
  }
 
void setup() {


  Serial.begin(9600);
  delay(10);
 
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
 
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
 
  IPAddress ip(192, 168, 2, 99); // where xx is the desired IP Address
IPAddress gateway(192, 168, 2, 1); // set gateway to match your network
Serial.print(F("Setting static ip to : "));
Serial.println(ip);
IPAddress subnet(255, 255, 255, 0); // set subnet mask to match your
WiFi.config(ip, gateway, subnet);
WiFi.begin(ssid, password);
Serial.println("");
Serial.println("Connecting to WiFi");
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
 
  // Start the server
  server.begin();
  Serial.println("Server started");
 
  // Print the IP address
  Serial.print("Use this URL to connect: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");

     pinMode(16, OUTPUT);
   digitalWrite(16, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(1000);                       // wait for a second
      digitalWrite(16, LOW);    // turn the LED off by making the voltage LOW
      delay(1000);   
 
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
 
void loop() {
  
 if (readline(Serial.read(), buffer, 80) > 0) {

      String checkstring = buffer;
      String turnval = "1500";
      
    buf = checkstring;
      if(checkstring.startsWith("sendana##"))     {
        
        digitalWrite(16, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(100);                       // wait for a second
      digitalWrite(16, LOW);    // turn the LED off by making the voltage LOW
      delay(100);    
        turnval=checkstring.substring(9,12);
            
            // val = turnval.toFloat();
   
      }

       if(checkstring.startsWith("sendamp##"))     {
        
          digitalWrite(16, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(100);                       // wait for a second
      digitalWrite(16, LOW);    // turn the LED off by making the voltage LOW
      delay(100);    
         digitalWrite(16, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(100);                       // wait for a second
      digitalWrite(16, LOW);    // turn the LED off by making the voltage LOW
      delay(100);    
        turnval=checkstring.substring(9,12);
            
           //  valamp = turnval.toFloat();
   
      }
      
      
      
      }

  
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

   digitalWrite(16, HIGH);   // turn the LED on (HIGH is the voltage level)
                       // wait for a second
      
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
 
  // Read the first line of the request
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();
 
  // Match the request
 
  int value = LOW;
  if (request.indexOf("/LED=ON") != -1)  {
    
   value = HIGH;
    val = batread(50);
  }
  if (request.indexOf("/LED=OFF") != -1)  {
    val = batread(50);
    value = LOW;
  }
 
// Set ledPin according to the request
//digitalWrite(ledPin, value);
 
  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  do not forget this one
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
 
  client.print("Voltage: ");
  client.print(val);
   client.print(" V<br><br>Amp: ");
  client.print(valamp);
   client.print(" A<br><br>MESSAGE: ");
   client.print(buf);
  
  client.println("<br><br>");
  client.println("<a href=\"/LED=ON\"\"><button>Update </button></a>");
  client.println("<a href=\"/LED=OFF\"\"><button>Turn Off </button></a><br />");  
  client.println("</html>");
 
  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");
  digitalWrite(16, LOW);    // turn the LED off by making the voltage LOW
    
 
}
