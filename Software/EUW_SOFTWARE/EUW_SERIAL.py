import jsonrpclib
import time
import serial
import threading

server = jsonrpclib.Server('http://localhost:8080')


ser = serial.Serial('/dev/ttyS0', 9600, timeout=10)
ser.close()
ser.open()
time.sleep(.5)

busy='0'

def handle_data(data):
    global busy
    if data!="":
        screen = "Nachtricht empfangen: "
        screen += data
        #print screen
    
    if data.find('ROGER')!=-1:
        busy="0"
        #print "Wesen: Ready!"
 
    if data.find('UPDATE###')!=-1:
        
        trim=data[9:]
        server.set_state(trim)
  

def read_from_port(seri):
    while True:
        reading = seri.readline()
        handle_data(reading)
        
thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()
update_count=0
 
try:
    while True:
        time.sleep(.1)
        update_count += 1
        if update_count>50:
                ser.write("getstatus\n\r")
                update_count=0
        if busy=='0':
            thread.lock()          
            tmp_cmd = server.get_cmd()
            thread.unlock()
            if tmp_cmd!='none':
                #print tmp_cmd
                busy='1'
                ser.write(tmp_cmd)
                
        
except KeyboardInterrupt:
    ser.close()
    print "exit"