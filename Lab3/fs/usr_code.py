## 1 shell = 100 robots
## 2 shells = 100 robots (50/50)
## 3 shells = 150 robots (50/50/50)

## HINTS ##
## Process of robot action;
##     1. Robots sense
##     2. Robots turn to desired angle
##     3. Robots move forward for certain amount of time
## 	   4. Go to 1
##
## Break into subproblems:
##     1. Have 1 robot move to light (0,0 in arena)
##     2. Have many robots move to light
##     3. Have 2 robots move away from each other if closer than R
##     4. Have many robots move away from each other
##     5. Have 1 robot move randomly
##     6. Put everything together

def usr(robot):
	import struct
	import math
	import timeit
	import time

	if robot.assigned_id==0:
		robot.set_led(100,0,0)
	elif robot.assigned_id==1:
		robot.set_led(0,100,0)
	else:
		robot.set_led(0,0,100)
	
	def alignHeading(theta,phi):
		if phi < 0:
			if abs(theta - phi) > 0.05:
				robot.set_vel(-25,25)
				return 0
			else:
				robot.set_vel(100,100)
				return 1
		else:
			if abs(abs(theta) - phi) > 0.05:
				robot.set_vel(-25,25)
				return 0
			else:
				robot.set_vel(100,100)
				return 1

	def taxis(robot):
		aligned = 0
		while not aligned:

			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t

				phi = math.atan(abs(pos[1]/pos[0]))
				theta = pos[2]

				if pos[0] < 0 and pos[1] > 0:
					phi = -phi
					aligned = alignHeading(theta,phi)
				elif pos[0] > 0 and pos[1] < 0:
					phi = -phi+math.pi
					aligned = alignHeading(theta,phi)
				elif pos[0] > 0 and pos[1] > 0:
					phi = phi - math.pi
					aligned = alignHeading(theta,phi)
				else:
					aligned = alignHeading(theta,phi)

	#def repulsion(robot):


		




