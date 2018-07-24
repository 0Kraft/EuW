from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

commandbuffer=['#'];
logbuffer=['#','#','#','#','#','#','#','#','#','#','#','#','#']
state_data='none'

def send_cmd(s):
    global commandbuffer,logbuffer
    s_tmp=s
    s_tmp+='\n\r'
    print s_tmp
    commandbuffer.insert(0,s_tmp)
    logbuffer.insert(0,s_tmp)  
    del logbuffer[-1]
    print commandbuffer
    return 1
    
def get_cmd():
    global commandbuffer
    result='none'
    if commandbuffer[0]!='#':
        result=commandbuffer[len(commandbuffer)-2]
        commandbuffer.pop(len(commandbuffer)-2)
    return result
    
def set_state(s):
    global state_data
    state_data = s
    return 1
    
def get_state():
    global state_data
    return state_data
    
def get_log():
    global logbuffer
    return logbuffer
    

server = SimpleJSONRPCServer(('localhost', 8080))
server.register_function(send_cmd, 'send_cmd')
server.register_function(get_cmd, 'get_cmd')
server.register_function(get_state, 'get_state')
server.register_function(set_state, 'set_state')
server.register_function(get_log, 'get_log')

server.serve_forever()