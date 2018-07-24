#file:client.py
from jsonsocket import Client
import time

host = 'LOCALHOST'
port = 8080

i=1
while True:
    client = Client()
    client.connect(host, port).send({'test':i})
    i+=1
    response = client.recv()
    print response
    tt = response["response"]["test"]
    print tt
    client.close()
    time.sleep(1)

