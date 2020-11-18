def usr(robot):
	import struct
	import math
	import timeit
	import time
	import numpy as np

	if robot.assigned_id==0:
		robot.set_led(100,0,0)
		R = 0.15
	elif robot.assigned_id==1:
		robot.set_led(0,100,0)
		R = 0.30
	else:
		robot.set_led(0,0,100)
		R = 0.4
	
	def alignHeading(theta,phi):
		# if phi > math.pi:
		# 	phi = (phi % math.pi) - math.pi
		if theta < phi and abs(theta - phi) > 0.25:
			robot.set_vel(-40,40)
			return 0
		elif theta > phi and abs(theta - phi) > 0.25:
			robot.set_vel(40,-40)
			return 0
		else:
			robot.set_vel(0,0)
			return 1

	while 1:
		phi_s = 0
		neighbors = []
		i = 0
		k = 3

		state = 1
		while state == 1:
			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t
				mag_vec = math.hypot(pos[0],pos[1])
				t_vec = [-pos[0]/mag_vec,-pos[1]/mag_vec] ## gives unit vector of taxis

				state = 2

		re_vec_s = [0,0]
		while state == 2:
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

			if i > 10:
				state = 3

		while state == 3:
			rand_x = robot.random.uniform(-1,1)
			rand_y = robot.random.uniform(-1,1)
			mag = math.hypot(rand_x,rand_y)
			ra_vec = [rand_x/mag,rand_y/mag]
			state = 4
		
		while state == 4:
			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t
				tot_vec = [1.6*ra_vec[0] + t_vec[0] + re_vec_s[0],0.6*ra_vec[1] + t_vec[1] + re_vec_s[1]]
				phi = math.atan2(tot_vec[1],tot_vec[0])
				aligned = alignHeading(pos[2],phi)
				if aligned:
					state = 5

		while state == 5:
			robot.set_vel(100,100)
			time.sleep(1)
			robot.set_vel(0,0)
			state = 1
	

	
	# def getDot(phi,vel):
	# 	xdot = math.cos(phi)*vel
	# 	ydot = math.sin(phi)*vel
	# 	return xdot,ydot
	
	# def getHeading(xdot,ydot):
	# 	phi = math.asin(ydot/100)
	# 	return phi

	# while(1):

	# 	dirTaxis = taxisVec(robot)
	# 	dirRepul,magRepel = repulVec(robot)
	# 	dirRand = randVec(robot)

	# 	if dirRepul != 0:
	# 		taxisX,taxisY = getDot(dirTaxis,magRepel*0.9)
	# 		repulX,repulY = getDot(dirRepul,magRepel)
	# 		randoX,randoY = getDot(dirRand,magRepel*0.75)

	# 		xave = (taxisX + repulX + randoX)/3
	# 		yave = (taxisY + repulY + randoY)/3
	# 	else:
	# 		taxisX,taxisY = getDot(dirTaxis,100)
	# 		randoX,randoY = getDot(dirRand,100)

	# 		xave = (taxisX + randoX)/2
	# 		yave = (taxisY + randoY)/2			

	# 	phi = getHeading(xave,yave)
	# 	aligned = 0
	# 	while not aligned:
	# 		pos_t = robot.get_pose()
	# 		if pos_t:
	# 			pos = pos_t
	# 			aligned = alignHeading(pos[2],phi,100)
			
	# 	time.sleep(10)





