# create JSON-RPC client
import jsonrpc
import time
import checklines_pi

server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(), jsonrpc.TransportTcpIp(addr=("127.0.0.1", 31415)))

# call a remote-procedure (with positional parameters)



import os

host = 'LOCALHOST'
port = 8080

time.sleep(1)

try:
    while 1:
        testVar = raw_input("Enter Command: ")
        if testVar=="report":
            result=server.getreport()
        elif testVar=="1":
            result = server.sendcommand("opengrab#A")
        elif testVar=="2":
            result = server.sendcommand("closegrabA")
        elif testVar=="3":
            result = server.sendcommand("turnslow#0500A")
        elif testVar=="4":
            result = server.sendcommand("turnslow#2500A")
        elif testVar=="5":
            result = server.sendcommand("opengrab#B")
        elif testVar=="6":
            result = server.sendcommand("closegrabB")
        elif testVar=="7":
            result = server.sendcommand("turnslow#0600B")
        elif testVar=="8":
            result = server.sendcommand("turnslow#2400B")
        elif testVar=="s":
            result = server.sendcommand("swap#####")
        elif testVar=="+":
            result = server.sendcommand("turnadder")
        elif testVar=="-":
            result = server.sendcommand("turnminus")
        elif testVar=="c":
            result = server.calibrate_lockB();                  
        elif testVar=="t":
            result = server.calibrate_lockA();                              
        elif testVar=="z":
            
            result=server.closegrabA()
            
        elif testVar=="u":
            
            result=server.turnA()
            
        elif testVar=="i":
            
            result=server.turnB()
            
            
        elif testVar=="g":
        
            text = server.sendcommand("opengrab#A")
            print "open"
            time.sleep(.5)
            
            text01 = server.sendcommand("turnslow#2300B")
            print "turn"
            time.sleep(2)
        
            result = checklines_pi.get_orientation()
            course = float(result)
            while course>8.0 or course<-8.0:
                
                if course>8.0:
                    text03 = server.sendcommand("turnadder")
                    print "+"
                if course<8.0:
                    text03 = server.sendcommand("turnminus")
                    print "-"
                result = checklines_pi.get_orientation()
                course = float(result)
                print result
                time.sleep(.5)
                
            time.sleep(2)
            print "check"
            
            check01 = server.sendcommand("closegrabA")
            time.sleep(2)
            print check01
            
            
            if check01.find('1$')!=-1:
                result02 = server.sendcommand("swap#####")
                time.sleep(2)
                
                text = server.sendcommand("opengrab#B")
                print "open"
                time.sleep(.5)
            
                text01 = server.sendcommand("turnslow#600A")
                print "turn"
                time.sleep(2)
        
                result = checklines_pi.get_orientation()
                course = float(result)
                while course>8.0 or course<-8.0:
                
                    if course>8.0:
                        text03 = server.sendcommand("turnadder")
                        print "+"
                    if course<8.0:
                        text03 = server.sendcommand("turnminus")
                        print "-"
                    result = checklines_pi.get_orientation()
                    course = float(result)
                    print result
                    time.sleep(.5)
                
                time.sleep(2)
                print "check"
            
                check01 = server.sendcommand("closegrabB")
                time.sleep(2)
                print check01
            
            
                if check01.find('1$')!=-1:
                    result02 = server.sendcommand("swap#####")
                    time.sleep(2)
                
                
                
                
                    
                
        else:
            result = server.sendcommand(testVar)
        print result
except KeyboardInterrupt:
    print "bye"

