#!/usr/bin/env python
 
import time
import pigpio
 
mg = [25,9] #GPIO number
servos = [14,15,18,23] #GPIO number
pi1 = pigpio.pi()

def open01():
	pi1.set_servo_pulsewidth(servos[0], 2500)
	time.sleep(.3)
	pi1.write(mg[0],1)
	time.sleep(.3)
	pi1.set_servo_pulsewidth(servos[0], 650) #servo 1 to 0 degree
	time.sleep(.3)
	pi1.write(mg[0],0)
	time.sleep(.5)
	pi1.set_servo_pulsewidth(servos[0], 0)
	pi1.set_servo_pulsewidth(servos[2], 0)
	print "Greifer 01 geoeffnet"
	
def close01():
	pi1.write(mg[0],1)
	time.sleep(.3)
	pi1.set_servo_pulsewidth(servos[0], 2500) #servo 1 to 0 degree
	#pi1.set_servo_pulsewidth(servos[2], 2500) #servo 1 to 0 degree
	time.sleep(1.2)
	pi1.write(mg[0],0)
	time.sleep(.5)
	pi1.set_servo_pulsewidth(servos[0], 0)
	#pi1.set_servo_pulsewidth(servos[2], 0)
	print "Greifer 01 geschlossen"
	
def open02():
	pi1.set_servo_pulsewidth(servos[2], 2500)
	time.sleep(.3)
	pi1.write(mg[1],1)
	time.sleep(.3)
	pi1.set_servo_pulsewidth(servos[2], 600) #servo 1 to 0 degree
	time.sleep(.3)
	pi1.write(mg[1],0)
	time.sleep(.5)
	pi1.set_servo_pulsewidth(servos[0], 0)
	pi1.set_servo_pulsewidth(servos[2], 0)
	print "Greifer 02 geoeffnet"
	
def close02():
	pi1.write(mg[1],1)
	time.sleep(.3)
	pi1.set_servo_pulsewidth(servos[0], 2500) #servo 1 to 0 degree
	pi1.set_servo_pulsewidth(servos[2], 2500) #servo 1 to 0 degree
	time.sleep(1.2)
	pi1.write(mg[1],0)
	time.sleep(.5)
	pi1.set_servo_pulsewidth(servos[0], 0)
	pi1.set_servo_pulsewidth(servos[2], 0)
	print "Greifer 02 geschlossen"
	
def turn02(d1,d2,d3):
	
	#for x in xrange(d1,d2,d3):
	#	pi1.set_servo_pulsewidth(servos[1], x) #servo 1 to 0 degree
		#time.sleep(.009)
	#	print x
	pi1.set_servo_pulsewidth(servos[1], d2) #servo 1 to 0 degree
	time.sleep(.5)
	pi1.set_servo_pulsewidth(servos[1], 0)
	

	print "Greifer 01 turned"
	
def turn01(d1,d2,d3):
	
	pi1.set_servo_pulsewidth(servos[3], d2) #servo 1 to 0 degree
	time.sleep(.5)
	
	pi1.set_servo_pulsewidth(servos[3], 0)
	

	print "Greifer 02 turned"
	

open01()
time.sleep(.5)
pi1.set_servo_pulsewidth(servos[3], 2500)
time.sleep(.5)
pi1.set_servo_pulsewidth(servos[3], 00)
time.sleep(.5)
close01()
time.sleep(.5)


pi1.set_servo_pulsewidth(24, 500)
time.sleep(1)





pi1.set_servo_pulsewidth(24, 0)


open02()
time.sleep(.5)
turn02(600,2320,1)
time.sleep(.5)
close02()


pi1.set_servo_pulsewidth(24, 2500)
time.sleep(1)
pi1.set_servo_pulsewidth(24, 0)

open01()
time.sleep(.5)
pi1.set_servo_pulsewidth(servos[3], 700)
time.sleep(.6)
pi1.set_servo_pulsewidth(servos[3], 00)
time.sleep(.5)
close01()


pi1.set_servo_pulsewidth(24, 500)
time.sleep(1)
pi1.set_servo_pulsewidth(24, 0)


open02()
time.sleep(.5)
turn02(2350,600,-1)
time.sleep(.5)
close02()

open02()
time.sleep(.5)
turn02(550,2350,1)
time.sleep(.5)
close02()
time.sleep(.5)


pi1.set_servo_pulsewidth(24, 2500)
time.sleep(1)
pi1.set_servo_pulsewidth(24, 0)



open01()
time.sleep(.5)
#pi1.set_servo_pulsewidth(servos[1], 2250)
pi1.set_servo_pulsewidth(servos[3], 2400)
pi1.set_servo_pulsewidth(servos[1], 0)
time.sleep(.5)
pi1.set_servo_pulsewidth(servos[3], 00)
time.sleep(.5)
close01()


pi1.set_servo_pulsewidth(24, 500)
time.sleep(1)
pi1.set_servo_pulsewidth(24, 0)


open02()
time.sleep(.5)
turn02(2450,600,-1)
time.sleep(.5)
close02()



pi1.set_servo_pulsewidth(24, 2500)
time.sleep(1)
pi1.set_servo_pulsewidth(24, 0)




open01()
time.sleep(.5)
turn01(2450,650,-1)
time.sleep(.5)

close01()
	
	


