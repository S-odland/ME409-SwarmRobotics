def usr(robot):
	import struct
	import math
	import timeit
	import time
	import numpy as np

	if robot.assigned_id==0:
		robot.set_led(100,0,0)
		R = 0.2
	elif robot.assigned_id==1:
		robot.set_led(0,100,0)
		R = 0.3
	else:
		robot.set_led(0,0,100)
		R = 0.4
	
	def alignHeading(theta,phi,vel):
		if phi < 0:
			if abs(theta - phi) > 0.05:
				robot.set_vel(-25,25)
				return 0
			else:
				robot.set_vel(vel,vel)
				return 1
		else:
			if abs(abs(theta) - phi) > 0.05:
				robot.set_vel(-25,25)
				return 0
			else:
				robot.set_vel(vel,vel)
				return 1

	def taxisVec(robot):
		aligned = 0
		while 1:
			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t

				phi = math.atan(abs(pos[1]/pos[0]))

				if pos[0] < 0 and pos[1] > 0:
					phi = -phi
				elif pos[0] > 0 and pos[1] < 0:
					phi = -phi+math.pi
				elif pos[0] > 0 and pos[1] > 0:
					phi = phi - math.pi
			if aligned == 1:
				return math.cos(phi)*50,math.sin(phi)*50

	def repulVec(robot):
		k = 1000
		phiT = 0
		neighbors = []
		i = 0
		while 1:
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
						phi = math.atan(abs(pos[1]-y/rAct))
						vel = k*(2*R-rAct)
						if pos[0] <= x and pos[1] >= y:
							phi = phi + math.pi/2
						elif pos[0] >= x and pos[1] < y:
							phi = -phi
						elif pos[0] <= x and pos[1] <= y:
							phi = phi - math.pi
					
						if rId not in neighbors:
							neighbors.append(rId)
							phiT += phi
							phiAve = phiT/len(neighbors)
							velAve = vel/len(neighbors)

						if i > 10: return phiAve,velAve
	
	def randVec(robot):
		phi = robot.random.uniform(-math.pi,math.pi)
		return phi
	
	def getDot(phi,vel):
		xdot = math.cos(phi)*vel
		ydot = math.sin(phi)*vel
		return xdot,ydot
	
	def getHeading(xdot,ydot):
		phi = ydot/(100)
		return phi

	while(1):

		dirTaxis = taxisVec(robot)
		dirRepul,magRepel = repulVec(robot)
		dirRand = randVec(robot)

		taxisX,taxisY = getDot(dirTaxis,50)
		repulX,repulY = getDot(dirRepul,magRepel)
		randoX,randoY = getDot(dirRand,25)

		xAve = (taxisX + repulX + randoX)/3
		yAve = (taxisY + repulY + randoY)/3

		phi = getHeading(xAve,yAve)
		
		pos_t = robot.get_pose()
		if pos_t:
			pos = pos_t 
			alignHeading(pos[2],phi,100)





