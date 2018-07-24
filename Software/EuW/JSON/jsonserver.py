# create a JSON-RPC-server
import jsonrpc
import time
import threading
import serial

ser = serial.Serial('/dev/ttyS0', 9600, timeout=10)
ser.close()
ser.open()
time.sleep(1)
server = jsonrpc.Server(jsonrpc.JsonRpc20(), jsonrpc.TransportTcpIp(addr=("127.0.0.1", 31415), logfunc=jsonrpc.log_file("myrpc.log")))
volt=""
connected=False

def handle_data(data):
	global volt
	print data
	
	if data.find('BATTERY##C')!=-1:
		volt=data[11:-1]
	if data.find('BATTERY##M')!=-1:
		volt=data[11:-1]
   

def read_from_port(seri):
    while True:
        reading = seri.readline()
        handle_data(reading)

thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()

# define some example-procedures and register them (so they can be called via RPC)
def getvolt(s):
    global volt
    ser.write('readbat\n\r')
    time.sleep(0.2)
    return volt
	
def sendcommand(s):
	ser.write(s+'\n\r')
	print s
	return "sentcommand"
    


server.register_function( getvolt )
server.register_function( sendcommand )


# start server
try:
    while True:
        server.serve()
except KeyboardInterrupt:
 
    ser.close()

