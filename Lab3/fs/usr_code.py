def usr(robot):
	import struct
	import math
	import timeit
	import time
	import numpy as np

	if robot.assigned_id==0:
		robot.set_led(100,0,0)
		R = 0.1
	elif robot.assigned_id==1:
		robot.set_led(0,100,0)
		R = 0.31
	else:
		robot.set_led(0,0,100)
		R = 0.4
	
	def alignHeading(theta,phi):
		if abs(theta - phi) > 0.1:
			robot.set_vel(40,-40)
			return 0
		else:
			robot.set_vel(0,0)
			return 1

	state = 1
	j = 0
	neighbors = []
	i = 0
	k = 150
	re_vec_s = [0,0]
	while 1:
		if state == 1:
			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t
				mag_vec = math.hypot(pos[0],pos[1])
				if mag_vec == 0:
					t_vec = [0,0]
					state = 2
				else:
					t_vec = [-pos[0]/mag_vec,-pos[1]/mag_vec] ## gives unit vector of taxis
					state = 2
		if state == 2:
			j += 1
			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t
				robot.send_msg(struct.pack("ffi",pos[0],pos[1],robot.id))
			msgs = robot.recv_msg()
			if len(msgs) > 0:
				x,y,rId = struct.unpack('ffi',msgs[0][:12])
				pos_t = robot.get_pose()
				if pos_t:
					i += 1
					pos = pos_t 
					rAct = math.hypot(pos[0]-x,pos[1]-y)
					if rAct < R:
						weight = k*(R-rAct)
						re_vec = [weight*(pos[0]-x),(pos[1]-y)]
						if rId not in neighbors:
							neighbors.append(rId)
							re_vec_s[0] += re_vec[0]
							re_vec_s[1] += re_vec[1]
			if j > 100 and len(neighbors) ==0:
				neighbors = []
				re_vec_s = [0,0]
				j = 0
				i = 0
				state = 3
			if i > 20:
				j = 0
				i = 0
				neighbors = []
				state = 3
		if state == 3:
			rand_x = robot.random.uniform(-1,1)
			rand_y = robot.random.uniform(-1,1)
			mag = math.hypot(rand_x,rand_y)
			ra_vec = [rand_x/mag,rand_y/mag]
			state = 4
		if state == 4:
			if math.hypot(re_vec_s[0],re_vec_s[1]) > 5:
				re_vec_s[0] = re_vec_s[0]/mag
				re_vec_s[1] = re_vec_s[1]/mag
			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t
				tot_vec = [1.4*ra_vec[0] + t_vec[0] + re_vec_s[0],1.4*ra_vec[1] + t_vec[1] + re_vec_s[1]]
				phi = math.atan2(tot_vec[1],tot_vec[0])
				aligned = alignHeading(pos[2],phi)
				if aligned:
					state = 5
		if state == 5:
			robot.set_vel(100,100)
			time.sleep(1)
			robot.set_vel(0,0)
			state = 1






