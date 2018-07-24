from jsonsocket import Client
import time
import os
import serial

host = 'LOCALHOST'
port = 8080

ser = serial.Serial('/dev/ttyS0', 9600, timeout=5)
ser.close()
ser.open()
i=0
time.sleep(1)

timeard=0
volt=0

try:
    while 1:
        
        time.sleep(1)

        ser.write('readbat\n\r')
        response = ser.readline()
        
        while response.find('$')==-1:
            response = ser.readline()
            print response
        if response.find('PI_SHU')!=-1:
            print "sent command"
            client = Client()
            client.connect(host, port).send({'command':1})
            client.close()
        if response.find('Battery')!=-1:
            volt=response[9:-7]
                         
        ser.write('time\n\r')
        response = ser.readline()
        while response.find('$')==-1:
            response = ser.readline()
            print response
        if response.find('PI_SHU')!=-1:
            print "sent command"
            client = Client()
            client.connect(host, port).send({'command':1})
            client.close()
        if response.find('Uptime')!=-1:
            timeard=response[8:-9]
            client = Client()
            client.connect(host, port)
            client.send({'command':3,'value':volt,'time':timeard})
            client.close()

           
except KeyboardInterrupt:
    client.close()
    ser.close()
