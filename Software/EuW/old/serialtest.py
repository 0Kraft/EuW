from jsonsocket import Client
import time
import os
import serial

host = 'LOCALHOST'
port = 8080

ser = serial.Serial('/dev/ttyS0', 9600)
ser.close()
ser.open()
i=0
time.sleep(1)
try:
    while 1:
        time.sleep(.3)
        client = Client()
        client.connect(host, port).send({'command':1})
        s_response = client.recv()
	client.close()
        
	if s_response["response"]==2:
           print "will send command"
           ser.write('readamp\n\r')
           time.sleep(.4)   
           response = ser.readline()
           print response
           while response.find('$')==-1:
               response = ser.readline()
               print response

       
           print "checking commands"
           if response.find('PI_SHU')!=-1:
                print "Das Wesen schaltet seine Sicht ab" 
                #client = Client()
                #client.connect(host, port).send({'test':i})
                #i+=1
                #client.close()
                os.system("sudo shutdown -h now")
    
except KeyboardInterrupt:
    ser.close()
