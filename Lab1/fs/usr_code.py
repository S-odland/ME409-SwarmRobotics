def usr(robot):
	import struct
	import math
	
	desired_distance = 0.17 #use this variable to set desired distance of orbit
	
	while True:
		pose_t=robot.get_pose()# gets pose The syscall that returns the robot's global pose (x, t, theta).
		#Note that the onboard sensor has a limited sampling rate of 30HZ. If there is no data from received the sensor since the last time 
		# the function get_pose() is called, the syscall will return None. If there is new data received from the sensor, the syscall will 
		# return a 3-tuple (x, y, theta), which are robot's x position, y, position, and orientation, respectively.

		if pose_t: #check pose is valid before using
			pose=pose_t
			print('The x,y postion of robot ',robot.id,' is ', pose[0],pose[1])
			robot.send_msg(struct.pack('ffi', pose[0], pose[1],robot.id))# send pose x,y in message
		

		msgs = robot.recv_msg()
		if len(msgs) > 0:
			pose_rxed= struct.unpack('ffi', msgs[0][:12])
			print('robot ',robot.id,' received position ',pose_rxed[0],pose_rxed[1],' from robot ', pose_rxed[2])
			