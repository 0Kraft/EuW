#file:server.py
from jsonsocket import Server
import os
import logging
import time
logging.basicConfig(filename='euwcontrol.log',level=logging.DEBUG)
host = 'LOCALHOST'
port = 8080
count=0

statusrpi=0
volt=0
servoAG=0
servoAK=0
servoBG=0
servoBK=0
servoU=0

gripA=0
gripB=0

lockA=0
lockB=0

timeard=0

server = Server(host, port)

logging.info('server open')
os.system("sudo python /home/pi/EuW/comtoard.py &")
print "test"
while True:
    
    server.accept()
    data = server.recv()
   
    if data["command"] == 'shutdown':
        print "Das Wesen schaltet seine Sicht ab"
        logging.info("Das Wesen schaltet seine Sicht ab")
        if statusrpi==0:
            statusrpi=1
        else:
            statusrpi=0
        os.system("sudo shutdown -h now")
    if data["command"] == 2:
        server.send({'status':volt})
    if data["command"] == 3:
        volt=data["value"]
        timeard=data["time"]
    if data["command"] == 'report':
        response2 = 'Battery: ' + volt + ' Volt'
        server.send({'message':response2})
    if data["command"] == 'move':
        response2 = 'Battery: ' + volt + ' Volt'
        server.send({'message':response2})
    if data["command"] == 'time':
        response2 = 'Time: ' + timeard + ' minutes'
        server.send({'message':response2})

    
    data = None
    
server.close()
