def usr(robot):
	import struct
	import math
	import timeit


	if robot.assigned_id==0:
		robot.set_led(100,0,0)
	elif robot.assigned_id==1:
		robot.set_led(0,100,0)
	else:
		robot.set_led(0,0,100)
		
	robot.set_vel(30,80)