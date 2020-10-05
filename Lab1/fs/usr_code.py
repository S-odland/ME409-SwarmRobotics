def usr(robot):
	import struct
	import math

	desired_distance = 0.19 #use this variable to set desired distance of orbit
	
	while True:

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
				if rID == 1:
					xdif = position[0] - pose_rxed[0]
					ydif = position[1] - pose_rxed[1]

					distance = math.sqrt(xdif**2 + ydif**2)

					distDif = desired_distance - distance

					if distDif > 0.015:
						robot.set_vel(69,43)
						robot.set_led(100,0,0)
					elif distDif < -0.015:
						robot.set_vel(71,41)
						robot.set_led(0,100,0)
					elif 0.015 > distDif > 0:
						robot.set_vel(70,43)
						robot.set_led(100,0,0)
					elif 0 > distDif > -0.015:
						robot.set_vel(70,41)
						robot.set_led(0,100,0)
					elif distDif == 0:
						robot.set_vel(70,42)

					robot.send_msg(struct.pack('ff', distDif,distance))

			if robot.id == 0:
				msg = robot.recv_msg()
				distns = struct.unpack(msg[0][:8])

			print(distns[1])

