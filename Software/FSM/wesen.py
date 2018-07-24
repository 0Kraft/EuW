from fsm import ungetauftes_wesen


testvar=0;
counter=0;

def communicate(i_cmd):
    print i_cmd

wesen = ungetauftes_wesen("wesen")

wesen.get_graph().draw('my_state_diagram.png', prog='dot')

wesen.wake_up()



while True:
    counter += testvar
    
    if wesen.havecommand==True:
        communicate(wesen.command)
        testvar=1
        wesen.havecommand=False
    if counter == 100:
        wesen.vision()
        testvar=0
        counter=0
       
    
