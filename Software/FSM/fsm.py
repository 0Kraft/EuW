
import random
from time import sleep
from vision import get_course
from transitions.extensions import GraphMachine as Machine

def senddata(tdata):
    print tdata

def checkdata(tdata):
    if tdata=='time':
        print "check time"
        return 1
    elif tdata=='orientation':
        print 'check orientation'
        return 2
    else:
        print 'check batteries'
        return 0


class ungetauftes_wesen(object):
  
    states = ['idle', 'move', 'check', 'move_straight', 'move_to_side','move_forward', 'move_back', 'orientate', 'open_gripper', 'rotate_gripper_fixed','vision','rotate_gripper_free','close_gripper','check_grip']

    def __init__(self, name):

        self.name = name
        
        self.havecommand = False
        self.command = " "
        
        self.angle_of_deviation = 0.0
        
        self.forward = True
        
        self.gripA = True
        self.gripB = True

        self.orientation = [0,0,0,0,0]
        self.moves_left=5
               

        # Initialize the state machine
        self.machine = Machine(model=self, states=ungetauftes_wesen.states, initial='idle')
        
       

        self.machine.add_transition(trigger='wake_up', source='idle', dest='move')
      
        self.machine.add_transition('move_straight', 'move', 'move_forward',conditions=['is_direction_forward'])
        self.machine.add_transition('move_straight', 'move', 'move_back',unless=['is_direction_forward'])
        
        self.machine.add_transition('orientate', 'move_forward', 'orientate')
        self.machine.add_transition('orientate', 'move_back', 'orientate')
        
        self.machine.add_transition('open_gripper', 'orientate', 'open_gripper')
        self.machine.add_transition('close_gripper', 'vision', 'close_gripper')
         
        self.machine.add_transition('rotate_gripper_fixed', 'open_gripper', 'rotate_gripper_fixed')
        
        self.machine.add_transition('vision', 'rotate_gripper_fixed', 'vision')
                
           
        self.machine.add_transition('check', 'idle', 'check')

        # Sweat is a disorder that can be remedied with water.
        # Unless you've had a particularly long day, in which case... bed time!
        self.machine.add_transition('move_finished', 'close_gripper', 'idle', conditions=['is_exhausted'])
        self.machine.add_transition('move_finished', 'close_gripper', 'move',)
        
      
        #self.machine.add_ordered_transitions(['move_forward', 'orientate'])
  
## CONDITIONS  

    def is_exhausted(self):
        """ Basically a coin toss. """
        return self.moves_left < 0.5
        
    def is_direction_forward(self): return self.forward
    
## CONDITIONS 
           
        
    def on_enter_move(self):
        print("entered state move")
        self.moves_left-=1
        print str(self.moves_left)+(" moves left")
        self.move_straight()
               
    def on_enter_move_forward(self):
        print("entered state move forward flag set")
        self.forward = False
        self.orientate()
    def on_enter_move_back(self):
        print("entered state move back flag set")
        self.forward = True
        self.orientate()
        
        
    def on_enter_idle(self):
        print("entered state idle")
        
    def on_enter_orientate(self):
        print("entered state orientate")   
        self.open_gripper()
        
    def on_enter_open_gripper(self):
        print("entered state open_gripper")
        senddata("testdata")
        print str(checkdata('fever'))
        self.rotate_gripper_fixed()
        
    def on_enter_rotate_gripper_fixed(self):
        print("entered state rotate_gripper_fixed")
        print("Wait for Signal:")
        self.havecommand = True
        self.command = "rotate"
        
    def on_enter_vision(self):
        print("entered state vision")
        
        self.angle_of_deviation = get_course()
        
        print "Our course is: " + str(self.angle_of_deviation)
        
        self.close_gripper()
        
        
                    
                
    def on_enter_close_gripper(self):
        print("entered state close_gripper")
        print("Wait for Signal:")
        sleep(.5)
        print(".")
        sleep(.5)
        print(".")
        sleep(.5)
        print(".")
        
        self.move_finished()

     
