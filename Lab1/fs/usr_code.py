## Through looking through the code and figuring out how docker works, I realized that
## each robot runs this code seperately and only communicates with the other the send_msg
## and recv_msg. So this code happens twice; once for robot.id == 0 and once for robot.id == 1

def usr(robot):
	import struct
	import math

	desired_distance = 0.19 #use this variable to set desired distance of orbit
	
	while True:

		pose_t=robot.get_pose() #gets the position of each robot

		if pose_t: ## a position recieved is not always valid due to the rate at which each 
			## robot sends broadcasts its position

			pose=pose_t ## creates an instance of the position
			robot.send_msg(struct.pack('ffi', pose[0], pose[1],robot.id)) ## robot sends 
			
		msgs = robot.recv_msg() ## since there are two robots in the swarm, the robot to receive 
		## the message will be the robot that didn't send it.
		## This is how the robots know about the other.

		if len(msgs) > 0: ## checks that a message contains data
			pose_rxed= struct.unpack('ffi', msgs[0][:12]) ## unpacks message recieved
			position = robot.get_pose() ## gets the position of the current robot -- the robot
			## that just recieved the message from the other robot
			if position and pose_rxed[2] == 0: ## checks that the position is valid, i.e new and that
				## the message being recieved is from robot.id == 0
				rID = robot.id ## creates an instance of the robot id
				if rID == 1: ## makes sure that the following is in robot.id == 1's environment

					xdif = position[0] - pose_rxed[0] ## calculates the x distance between 1 and 0
					ydif = position[1] - pose_rxed[1] ## calculates the y distance between 1 and 0

					distance = math.sqrt(xdif**2 + ydif**2) ## calculates the straight line distance

					distDif = desired_distance - distance ## difference between the desired distance and
					## the actual distance

## In trial and error I found that the best speed ratio was for the right wheel to be about 67% the speed of the left wheel.
## If the actual distance is less than the desired distance, ratio is changed to about 65% and if the the actual distance is
## greater than the desired distance the ratio is changed to about 69%

## This method works for about the first minute or so. For longer orbit times, actual motor control and not
## guess and check would be necessary

## LEDs are set accordingly

					if distDif > 0:
						robot.set_vel(71,43)
						robot.set_led(100,0,0)
					elif 0 > distDif: 
						robot.set_vel(69,41)
						robot.set_led(0,100,0)
					elif distDif == 0:
						robot.set_vel(70,42)

## below code checks that the robot 0 is receiving a message from robot 1. Then does an equivalent
## calculation the robot 1 did to set its own LED, then outputs the distance between the two robots

			if position and pose_rxed[2] == 1:
				rID = robot.id
				if rID == 0:
					xdif = position[0] - pose_rxed[0]
					ydif = position[1] - pose_rxed[1]

					distance = math.sqrt(xdif**2 + ydif**2)

					distDif = desired_distance - distance

					if distDif > 0:
						robot.set_led(100,0,0)
					elif 0 > distDif:
						robot.set_led(0,100,0)
					print(distance)



