def usr(robot):
	import struct
	import math
	import timeit
	import time
	import numpy as np

		# this was my init pose loop for a swarm of 150 robots
	    #     y[i] = (i % 10 ) * 0.3-1
        # x[i] = (i / 10 ) * 0.3-1
        # a_ids[i] = 0
        # theta[i] = 0
        # j = i % 3
        # if j == 0:
        #     a_ids[i]=0
        # elif j == 1:
        #     a_ids[i]=1
        # else:
        #     a_ids[i] = 2

	if robot.assigned_id==0:
		robot.set_led(100,0,0)
		R = 0.1
	elif robot.assigned_id==1:
		robot.set_led(0,100,0)
		R = 0.23
	else:
		robot.set_led(0,0,100)
		R = 0.4
	
	## function to align heading of robot with desired angle -- error of 10%
	def alignHeading(theta,phi):
		if abs(theta - phi) > 0.1:
			robot.set_vel(70,-70)
			return 0
		else:
			robot.set_vel(0,0)
			return 1

	state = 1
	j = 0
	neighbors = []
	i = 0
	k = 1000
	re_vec_s = [0,0]

   # state machine functions as follows:
   # state 1: taxis vector calculation
   # state 2: repulsion vector calculation
   # state 3: random vector calculation
   # state 4: align heading with desired angle after everything summed up
   # state 5: move for a specified amount of time
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
			
			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t
				robot.send_msg(struct.pack("ffi",pos[0],pos[1],robot.id))
				j += 1
			msgs = robot.recv_msg()
			if len(msgs) > 0:
				x,y,rId = struct.unpack('ffi',msgs[0][:12])
				pos_t = robot.get_pose()
				if pos_t:
					i += 1
					pos = pos_t 
					rAct = math.hypot(pos[0]-x,pos[1]-y)
					## check virtual overlap
					if rAct < R:
						weight = k*(R-rAct)
						re_vec = [weight*(pos[0]-x),weight*(pos[1]-y)]
						#make sure that this robot hasn't been calculated in vector sum
						if rId not in neighbors:
							neighbors.append(rId)
							re_vec_s[0] += re_vec[0]
							re_vec_s[1] += re_vec[1]
			# i is the inner loop (recieved messages) j is outer loop -- ensures that lone robots dont get stuck in state 2
			if i > 20 or j > 350:
				j = 0
				i = 0
				neighbors = []
				state = 3

		if state == 3:
			rand_x = robot.random.uniform(-1,1)
			rand_y = robot.random.uniform(-1,1)
			mag = math.hypot(rand_x,rand_y)
			ra_vec = [rand_x/mag,rand_y/mag] # normalizes random vec to be a unit vec
			state = 4

		if state == 4:
			# normalizing repulsion vec to be below 8
			if math.hypot(re_vec_s[0],re_vec_s[1]) > 8:
				rat = 8/math.hypot(re_vec_s[0],re_vec_s[1])
				re_vec_s[0] = re_vec_s[0]*rat
				re_vec_s[1] = re_vec_s[1]*rat

# found that the repulsion vec weight to be higher made the brazil effect clearer
			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t
				# summing up vector
				tot_vec = [0.6*ra_vec[0] + t_vec[0] + re_vec_s[0],0.6*ra_vec[1] + t_vec[1] + re_vec_s[1]]
				tot_mag = math.hypot(ra_vec[0],ra_vec[1]) + math.hypot(t_vec[0],t_vec[1]) + math.hypot(re_vec_s[0],re_vec_s[1])
				phi = math.atan2(tot_vec[1],tot_vec[0])
				aligned = alignHeading(pos[2],phi)
				if aligned:
					state = 5

## hard coding the velocity makes it converge faster
		if state == 5:
			vel = 100*tot_mag/7.5
			#robot.set_vel(vel,vel)
			robot.set_vel(75,75)
			time.sleep(1)
			robot.set_vel(0,0)
			re_vec_s = [0,0]
			state = 1






