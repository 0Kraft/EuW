import jsonrpclib
import time
server = jsonrpclib.Server('http://localhost:8080')
print server.get_state()
