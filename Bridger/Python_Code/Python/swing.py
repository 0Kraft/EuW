#!/usr/bin/env python
 
import time
 
import pigpio
 
servos = [14,15,18,23] #GPIO number
 
pigpio.start()
#pulsewidth can only set between 500-2500
try:
    while True:
 
        pigpio.set_servo_pulsewidth(servos[1], 1000) #servo 1 to 0 degree
        print("Servo {} {} micro pulses".format(servos, 1000))
        time.sleep(1)
        pigpio.set_servo_pulsewidth(servos[3], 600) #servo 2 to 90 degree
        print("Servo {} {} micro pulses".format(servos, 600))
        time.sleep(3)
		pigpio.set_servo_pulsewidth(servos[1], 2400) #servo 1 to 0 degree
        print("Servo {} {} micro pulses".format(servos, 2400))
        time.sleep(1)
		pigpio.set_servo_pulsewidth(servos[2], 1000) #servo 1 to 0 degree
        print("Servo {} {} micro pulses".format(servos, 1000))
        time.sleep(1)
	    pigpio.set_servo_pulsewidth(servos[0], 2200)
        print("Servo {} {} micro pulses".format(servos, 2200))
        time.sleep(3)
        pigpio.set_servo_pulsewidth(servos[2], 2500)
        print("Servo {} {} micro pulses".format(servos, 2500))
        time.sleep(1)
		
		
 
   # switch all servos off
except KeyboardInterrupt:
    for s in servos:
 
        pigpio.set_servo_pulsewidth(s, 0);
 
pigpio.stop()