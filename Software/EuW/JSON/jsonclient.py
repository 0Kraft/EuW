# create JSON-RPC client
import jsonrpc
import time
server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(), jsonrpc.TransportTcpIp(addr=("127.0.0.1", 31415)))

# call a remote-procedure (with positional parameters)



import os

host = 'LOCALHOST'
port = 8080

time.sleep(1)

try:
    while 1:
		testVar = raw_input("Enter Command: ")
		result = server.sendcommand(testVar)
		print result
except KeyboardInterrupt:
    print "bye"

