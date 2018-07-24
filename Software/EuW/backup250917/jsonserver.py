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
voltC="nix"
voltM="nix"

globalanswer="standard"
gotanswer=0

A3=0
B3=0

gripA=0

busy="0"

connected=False

def handle_data(data):
    global voltC
    global voltM
    global B3
    global A3
    global uptime
    global globalanswer
    global gripA
    global gripB
    global busy
    
    
    print data
    gripA="0"
    global gotanswer

    if data.find('BATTERY##C')!=-1:
        voltC=data[10:-3]
    if data.find('BATTERY##M')!=-1:
        voltM=data[10:-3]
    if data.find('POSITION#A')!=-1:
        busy="0";
        trim=data
        print "datenaction"
        print trim
        trim2 = trim[10:]
        print trim2
        trim3 = trim2[:-3]
        print trim3
        print "datenaction"
        A3=int(trim3)
        print A3
    if data.find('POSITION#B')!=-1:
        busy="0";
        B3=data[10:-3]
    if data.find('TIME#####')!=-1:
        uptime=data[9:-3]
    if data.find('GRIPA####')!=-1:
        busy="0";
        gripA=data[9:-3]
    if data.find('GRIPB####')!=-1:
        busy="0";
        gripB=data[9:-3]
    
   

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
    global B3
    global A3
    global uptime
    global globalanswer
    global gripA
    global gripB
    
    ser.write(s+'\n\r')
    time.sleep(0.4)
    #answer = "Rotation A: "
    #answer += A3
    #answer += " Rotation B: "
    #answer += B3
    
    
    
    if s.find('closegrabA')!=-1:
        
        return gripA
    elif s.find('time')!=-1:
        
        return uptime
    elif s.find('closegrabB')!=-1:
        
        return gripB
    else:
        return "nix"
        
    
   
    
    
	
def getreport():
	global voltC
	global voltM
  
   	ser.write('readbat##C\n\r')
	time.sleep(0.4)
	ser.write('readbat##M\n\r')
	time.sleep(0.4)
	answer = "Batterie Motor: " 
	answer += voltM
	answer += " Batterie Control: "
	answer += voltC
	return answer
    
    
def turnA():
    global busy
    global A3
    if(A3>1500):
        ser.write('turnslow#0600A\n\r')
    if(A3<1500):
        ser.write('turnslow#2400A\n\r')
    busy="1"
    return 1

def turnB():
    global busy
    ser.write('turnslow#0600B\n\r')
    busy="1"
    return 1
    
def closegrabA():
    global busy
    ser.write('closegrabA\n\r')
    busy="1"
    return 1
    
def checkgrabA():
    global gripA
    return gripA
    
def opengrabA():
    global busy
    ser.write('opengrab#A\n\r')
    busy="1"
    return 1
    
def opengrabB():
    global busy
    ser.write('opengrab#B\n\r')
    busy="1"
    return 1
    
def closegrabB():
    global busy
    ser.write('closegrabB\n\r')
    busy="1"
    return 1
    
def checkgrabB():
    global gripB
    return gripB
    
def busy():
    global busy
    return busy
    
    
    


server.register_function( getvolt )
server.register_function( sendcommand )
server.register_function( getreport )


server.register_function( opengrabA )
server.register_function( closegrabA )
server.register_function( checkgrabA )

server.register_function( opengrabB )
server.register_function( closegrabB )
server.register_function( checkgrabB )

server.register_function( turnA)
server.register_function( turnB)

server.register_function( busy )



# start server
try:
    while True:
        server.serve()
except KeyboardInterrupt:
 
    ser.close()

