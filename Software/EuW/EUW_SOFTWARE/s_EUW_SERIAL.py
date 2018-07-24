import jsonrpclib
import time
import serial
import threading
import sys

server = jsonrpclib.Server('http://localhost:8080')

if sys.argv[1:]==[0]:
    sim_mode=0
else:
    sim_mode=1
    
print sim_mode

if sim_mode==0:
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=10)
    ser.close()
    ser.open()
    time.sleep(.5)

busy='0'
trim=0

def handle_data(data):
    global busy
    print data
    if data!="":
        screen = "Nachtricht empfangen: "
        screen += data
        #print screen
        busy="0"
    
    if data.find('ROGER')!=-1:
        busy="0"
        #print "Wesen: Ready!"
 
    if data.find('UPDATE###')!=-1:
        global trim
        trim=data[9:]
        
        busy="0"
        print trim
  

def read_from_port(seri):
    while True:
        reading = seri.readline()
        handle_data(reading)

if sim_mode==0:        
    thread = threading.Thread(target=read_from_port, args=(ser,))
    thread.start()
update_count=0
 
try:
    while True:
        time.sleep(.5)
        
        #if update_count>50:
                #ser.write("getstatus\n\r")
                #update_count=0
        if busy=='0':
           
            tmp_cmd = server.get_cmd()
            
            if tmp_cmd!='none':
                #print tmp_cmd
                busy='1'
                if sim_mode==0:
                    ser.write(tmp_cmd)
                else:
                    print tmp_cmd
                    busy='0'
        else:
            #ser.write("getstatus\n\r")
            server.set_state(trim)
            
            
                
        
except KeyboardInterrupt:
    if sim_mode!=1:
        ser.close()
    print "exit"