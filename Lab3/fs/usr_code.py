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

	light = (0,0)

## takes robot heading and light position to calculate movement for robot to aligh towards light
	def alignLight(light,robot_head ):


	if robot.assigned_id==0:
		robot.set_led(100,0,0)
	elif robot.assigned_id==1:
		robot.set_led(0,100,0)
	else:
		robot.set_led(0,0,100)
		
	robot.set_vel(30,80)
	while(1):
		pose_t = robot.get_pose()
		if pose_t:
			print(pose_t[2])