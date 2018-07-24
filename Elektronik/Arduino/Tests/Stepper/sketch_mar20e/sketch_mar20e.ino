#define NrOfMotorOutputs 4 //Anzahl der Ausgänge zur Ansteuerung des Motors
#define NrOfPatternsOneStep 8 //Anzahl der Muster zur Ansteuerung eines Schritts

//Variabeln für Drehrichtung definieren
const byte MotorOff = 0;
const byte DirMotorRight = 1;
const byte DirMotorLeft = 2;

unsigned int ActStepNr = 0; //Aktueller Schritt
unsigned int lowSpeed = 2000; //Aktueller Schritt

//Schrittmuster definieren
byte StepPattern[NrOfPatternsOneStep][NrOfMotorOutputs] =
{
{ 0, 0, 0, 1 },
{ 0, 0, 1, 1 },
{ 0, 0, 1, 0 },
{ 0, 1, 1, 0 },
{ 0, 1, 0, 0 },
{ 1, 1, 0, 0 },
{ 1, 0, 0, 0 },
{ 1, 0, 0, 1 },
} ;

//Motor Pins für Ausgänge 1-4 definieren
byte MotorOutputPin[NrOfMotorOutputs] = {8,9,10,11};

void setup()
{
//Alle Pins als Ausgänge setzen und auf LOW schalten
for (byte i=0; i < NrOfMotorOutputs; i++)
{
pinMode((MotorOutputPin[i]), OUTPUT);
digitalWrite(MotorOutputPin[i], LOW);
}
}

// the loop routine runs over and over again forever:

void loop()
{

//Beispielprogramm zur Ansteuerung
MotorMove(DirMotorRight,3000, 2048); // MotorMove(Drehrichtung, MotorSpeed, Anzahl Schritte)
delay(1000);
MotorMove(DirMotorLeft,3000, 2084);
MotorMove(MotorOff,0, 0); //Motor stromlos Pin 1-4 = LOW
delay(1000);

}

/////////////// Funktion für Motoransteuerung Anfang //////////////////
void MotorMove(byte MotorDir, unsigned int MotorSpeed, unsigned int StepsToGo)
{

//Motor Stop alle Ausgänge auf LOW schalten
if (MotorDir == MotorOff)
{
for (byte i=0; i < NrOfMotorOutputs; i++)
{
digitalWrite(MotorOutputPin[i], LOW);
}
}

//Motor Rechtsdrehung
else if (MotorDir == DirMotorRight)
{
for (int i=0; i < StepsToGo; i++)
{
ActStepNr++;
if (ActStepNr == NrOfPatternsOneStep) ActStepNr = 0;
for (byte j=0; j < NrOfMotorOutputs; j++)
{
digitalWrite(MotorOutputPin[j], StepPattern[ActStepNr][j]);
}
delayMicroseconds(MotorSpeed); //Verweilzeit um die Geschwindigkeit zu beeinflussen, für schnellere Ansteuereung ev. delayMicroseconds
}
if(MotorSpeed>lowSpeed)MotorSpeed=MotorSpeed-200;
}

//Motor Linksdrehung
else if (MotorDir == DirMotorLeft)
{
for (int i=0; i < StepsToGo; i++)
{
if (ActStepNr == 0){
  ActStepNr=NrOfPatternsOneStep-1;
  }else{
    ActStepNr--;}
for (byte j=0; j < NrOfMotorOutputs; j++)
{
digitalWrite(MotorOutputPin[j], StepPattern[ActStepNr][j]);
}
delayMicroseconds(MotorSpeed);
}
if(MotorSpeed>lowSpeed)MotorSpeed=MotorSpeed-200;
}
}
/////////////// Funktion für Motoransteuerung Ende //////////////////
