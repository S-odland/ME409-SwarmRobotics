def usr(robot):
	import struct
	import math
	import timeit
	import time
	import numpy as np

	## TODO: change phi calculations to vectors --> will be a lot easier to sum up dif direction headings this way

	if robot.assigned_id==0:
		robot.set_led(100,0,0)
		R = 0.25
	elif robot.assigned_id==1:
		robot.set_led(0,100,0)
		R = 0.35
	else:
		robot.set_led(0,0,100)
		R = 0.35
	
	def alignHeading(theta,phi):
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

		k = 600
		phi_s = 0
		neighbors = []
		i = 0
		state = 1

		while state == 1:
			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t
				phi_t = math.atan(abs(pos[1]/pos[0]))

				if pos[0] < 0 and pos[1] > 0:
					phi_t = -phi_t
				elif pos[0] > 0 and pos[1] < 0:
					phi_t = -phi_t + math.pi
				elif pos[0] > 0 and pos[1] > 0:
					phi_t = phi_t - math.pi
				elif pos[0] < 0 and pos[1] == 0:
					phi_r = 0
				elif pos[0] > 0 and pos[1] == 0:
					phi_r = -math.pi
				elif pos[0] == 0 and pos[1] < 0:
					phi_r = math.pi/2
				elif pos[0] == 0 and pos[1] > 0:
					phi_r = -math.pi/2

				state = 2

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
						phi_r = math.asin(abs((pos[1]-y)/rAct)) 
						weight = k*(2*R-rAct)

						if pos[0] < x and pos[1] == y:
							phi_r = math.pi
						elif pos[0] > x and pos[1] == y:
							phi_r = 0
						elif pos[0] == x and pos[1] < y:
							phi_r = -math.pi/2
						elif pos[0] == x and pos[1] > y:
							phi_r = math.pi/2					
						elif pos[0] < x and pos[1] > y:
							phi_r = -phi_r + math.pi
						elif pos[0] > x and pos[1] < y:
							phi_r = -phi_r
						elif pos[0] < x and pos[1] < y:
							phi_r = phi_r - math.pi

						if rId not in neighbors:
							neighbors.append(rId)
							phi_s += phi_r
							if phi_s < -math.pi:
								phi_s = phi_s % -math.pi 
							if phi_s > math.pi:
								phi_s = phi_s % math.pi
							weight = weight/len(neighbors)
					if i > 25:
						state = 3

		phi_rand = robot.random.uniform(-math.pi,math.pi)
		aligned = 0
		while state == 3:
			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t
				phi_total = phi_s+phi_rand+phi_t
				if phi_total < -math.pi:
					phi_total = (phi_total % -math.pi) + math.pi
				elif phi_total > math.pi:
					phi_total = (phi_total % math.pi) - math.pi

				aligned = alignHeading(pos[2],phi_total)
				if aligned == 1:
					state = 4
		
		while state == 4:
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





