def usr(robot):
	import struct
	import math

	desired_distance = 0.17 #use this variable to set desired distance of orbit
	i = 0
	while i <= 100:
		i += 1

		pose_t=robot.get_pose()

		if pose_t: 
			pose=pose_t
			robot.send_msg(struct.pack('ffi', pose[0], pose[1],robot.id))
			
		msgs = robot.recv_msg()
		if len(msgs) > 0:
			pose_rxed= struct.unpack('ffi', msgs[0][:12])
			position = robot.get_pose()
			if position:
				rID = robot.id
				if rID == 1
			## this if allows me to know if robot 1 is to the right or left of robot 0 because position of robot 0 will always be subtracted from robot 1
					xdif = position[0] - pose_rxed[0]
					ydif = position[1] - pose_rxed[1]

					distance = math.sqrt(xdif**2 + ydif**2)

					distDif = desired_distance - distance

					print(position[0],rID,position[1])
					print('robot ',rID,' received position ',pose_rxed[0],pose_rxed[1],' from robot ', pose_rxed[2],i)
					print(distDif)

