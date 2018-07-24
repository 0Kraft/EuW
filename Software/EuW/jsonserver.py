# create a JSON-RPC-server
import jsonrpc
import time
import threading
import serial
import checklines_pi
import pickle

ser = serial.Serial('/dev/ttyS0', 9600, timeout=10)
ser.close()
ser.open()
time.sleep(1)
server = jsonrpc.Server(jsonrpc.JsonRpc20(), jsonrpc.TransportTcpIp(addr=("127.0.0.1", 31415), logfunc=jsonrpc.log_file("myrpc.log")))
voltC="nix"
voltM="nix"

commandbuffer=['#'];

#state={"A1_ms":800,"A2_ms":1200,"A3_ms":2400,"locking_positionA":1200,"B1_ms":800,"B2_ms":1200,"B3_ms":2400,"locking_positionB":1200,"u_pos":1}

#file = open('state.txt', 'w')
#pickle.dump(state, file)
#file.close()

file = open('state.txt', 'r')
state = pickle.load(file)
file.close()
init=""
init+="init#####"
init+=str(state["A1_ms"]).zfill(4)
init+="#"
init+=str(state["A2_ms"]).zfill(4)
init+="#"
init+=str(state["A3_ms"]).zfill(4)
init+="#"
init+=str(state["locking_positionA"]).zfill(4)
init+="#"
init+=str(state["B1_ms"]).zfill(4)
init+="#"
init+=str(state["B2_ms"]).zfill(4)
init+="#"
init+=str(state["B3_ms"]).zfill(4)
init+="#"
init+=str(state["locking_positionB"]).zfill(4)
init+="#"
init+=str(state["u_pos"])
init+="\n\r"
print init

#commandbuffer.insert(0,init)       # Calibration 



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
    global state
    
    screen = "Nachtricht empfangen: "
    screen += data
    print screen
    
    gripA="0"
    global gotanswer

    if data.find('BATTERY##C')!=-1:
        voltC=data[10:-3]
    if data.find('BATTERY##M')!=-1:
        voltM=data[10:-3]
    if data.find('POSITION#A')!=-1:
        busy="0"
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
        busy="0"
        B3=data[10:-3]
    if data.find('TIME#####')!=-1:
        uptime=data[9:-3]
    if data.find('GRIPA####')!=-1:
        busy="0"
        gripA=data[9:-3]
    if data.find('GRIPB####')!=-1:
        busy="0"
        gripB=data[9:-3]
    if data.find('ROGER')!=-1:
        busy="0"
        print busy
        print "Wesen: Ready!"
    if data.find('CALA#')!=-1:
        print "gotcalib"
        trim=data
        trim2 = trim[9:]
        trim3 = trim2[:-3]
        print trim3
        state["locking_positionA"] = int(trim3)
        file = open('state.txt', 'w')
        pickle.dump(state, file)
        file.close()
    if data.find('CALB#')!=-1:
        print "gotcalibB"
        trim=data
        trim2 = trim[9:]
        trim3 = trim2[:-3]
        print trim3
        state["locking_positionB"] = int(trim3)
        file = open('state.txt', 'w')
        pickle.dump(state, file)
        file.close()
    if data.find('START####')!=-1:
        file = open('state.txt', 'r')
        state = pickle.load(file)
        file.close()
        init=""
        init+="init#####"
        init+=str(state["A1_ms"]).zfill(4)
        init+="#"
        init+=str(state["A2_ms"]).zfill(4)
        init+="#"
        init+=str(state["A3_ms"]).zfill(4)
        init+="#"
        init+=str(state["locking_positionA"]).zfill(4)
        init+="#"
        init+=str(state["B1_ms"]).zfill(4)
        init+="#"
        init+=str(state["B2_ms"]).zfill(4)
        init+="#"
        init+=str(state["B3_ms"]).zfill(4)
        init+="#"
        init+=str(state["locking_positionB"]).zfill(4)
        init+="#"
        init+=str(state["u_pos"])

        init+="\n\r"
        print init
        commandbuffer.insert(0,init)     
    if data.find('UPDATE###')!=-1:
        trim=data[9:]
        update_data=trim.split(";")
        
        state["A1_ms"]=int(update_data[0])
        state["A2_ms"]=int(update_data[1])
        state["A3_ms"]=int(update_data[2])
        state["locking_positionA"]=int(update_data[3])
        state["lockedA"]=int(update_data[4])
        
        state["B1_ms"]=int(update_data[5])
        state["B2_ms"]=int(update_data[6])
        state["B3_ms"]=int(update_data[7])
        state["locking_positionB"]=int(update_data[8])
        state["lockedB"]=int(update_data[9])
        state["u_pos"]=int(update_data[10])
        state["swaptime"]=int(update_data[11])
        
        print "<-- UPDATE -->"
        print " "
        print "lockedA:  " + str(state["lockedA"]) + "      Status of Lock A"
        print "lockedA:  " + str(state["lockedB"]) + "      Status of Lock B"
        print "u_pos:    " + str(state["u_pos"]) + "      Status of Slide"
        print "swaptime: " + str(state["swaptime"]) + "      Time for Swap"
        print " "
        print "<--       -->"
       
        
        
        file = open('state.txt', 'w')
        pickle.dump(state, file)
        file.close()
        
        
        
    
   

def read_from_port(seri):
    while True:
        reading = seri.readline()
        handle_data(reading)
        
def mainloop(seris):
    global busy
    global commandbuffer
    while True:
        if commandbuffer[0]!='#' and busy!="1":
            print " Befehl wird ausgefuehrt "
            print commandbuffer[len(commandbuffer)-2]
            if commandbuffer[len(commandbuffer)-2] == 'shot':
                seris.write('switchir#1\n\r')
                result = checklines_pi.shot("shot1")
                seris.write('switchir#0\n\r')
                result = checklines_pi.shot("shot2")
                
            elif commandbuffer[len(commandbuffer)-2] == 'cv':
                result = checklines_pi.get_cv2()
            elif commandbuffer[len(commandbuffer)-2] == 'orientation':
                time.sleep(6)
                result = checklines_pi.get_cv2()
                course = float(result)
                if course == 200.0:
                    course = 0.0
                print "Orientierung"
                print course
                while course>12.0 or course<-12.0:
                
                    if course>12.0:
                        seris.write('turnadder+\n\r')
                    if course<12.0:
                        seris.write('turnadder-\n\r')    
                        
                    result = checklines_pi.get_cv()
                    course = float(result)
            else:
                seris.write(commandbuffer[len(commandbuffer)-2])
                print "Gesendet"
                busy="1"
            print " Befehl wurde ausgefuehrt "
            
            commandbuffer.pop(len(commandbuffer)-2)
            print commandbuffer
        
        
thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()
thread2 = threading.Thread(target=mainloop, args=(ser,))
thread2.start()

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
    global commandbuffer
    commandbuffer.insert(0,'turnauto#A\n\r')     
    
    print commandbuffer
    return 1

def turnB():
    global commandbuffer
    commandbuffer.insert(0,'turnauto#B\n\r')     
    print commandbuffer    
    return 1   
    
def closegrabA():
    global commandbuffer
    commandbuffer.insert(0,'closegrabA\n\r')     
    print commandbuffer    
    return 1   
       
def checkgrabA():
    global gripA
    return gripA
    
def opengrabA():
    global commandbuffer
    commandbuffer.insert(0,'opengrab#A\n\r') 
    print commandbuffer    
    return 1
    
def opengrabB():
    global commandbuffer
    commandbuffer.insert(0,'opengrab#B\n\r') 
    print commandbuffer    
    return 1
    
def closegrabB():
    global commandbuffer
    commandbuffer.insert(0,'closegrabB\n\r')   
    print commandbuffer    
    return 1
    
def swap():
    global commandbuffer
    commandbuffer.insert(0,'swap#####\n\r')    
    return 1 
    
def checkgrabB():
    global gripB
    return gripB
    
def busy():
    global busy
    return busy
    
def orientation():
    global commandbuffer
    commandbuffer.insert(0,'orientation');
    return 1  

def calibrate_lockA():
    global commandbuffer
    commandbuffer.insert(0,'calibrationA\n\r');
    return 1

def calibrate_lockB():
    global commandbuffer
    commandbuffer.insert(0,'calibrationB\n\r');
    return 1     
    
def cv():
    global commandbuffer
    commandbuffer.insert(0,'cv');
    return 1    

def shot():
    global commandbuffer
    commandbuffer.insert(0,'shot');
    print commandbuffer   
    return 1     
    
def set_swap(swaptime):
    global commandbuffer
    cmd_tmp = 'set_swap#'
    cmd_tmp += str(swaptime)
    cmd_tmp += '\n\r'
    commandbuffer.insert(0,cmd_tmp);
    print commandbuffer   
    return 1     
    


server.register_function( getvolt )
server.register_function( sendcommand )
server.register_function( getreport )


server.register_function( opengrabA )
server.register_function( closegrabA )
server.register_function( checkgrabA )

server.register_function( opengrabB )
server.register_function( closegrabB )
server.register_function( checkgrabB )

server.register_function( orientation )
server.register_function( swap )

server.register_function( turnA)
server.register_function( turnB)

server.register_function( busy )

server.register_function( calibrate_lockA )
server.register_function( calibrate_lockB )

server.register_function( cv )
server.register_function( shot )

server.register_function( set_swap )



# start server
try:
    while True:
        print "test"
        server.serve()
               
        
            
except KeyboardInterrupt:
 
    ser.close()

