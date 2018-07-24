from jsonsocket import Client
import time
import os

host = 'LOCALHOST'
port = 8080

time.sleep(1)

try:
    while 1:
        testVar = raw_input("Enter Command: ")
        print testVar;
        client = Client()
        client.connect(host, port).send({'command':testVar})
        response = client.recv()
        print response['message']
        client.close()  
except KeyboardInterrupt:
    print "bye"
