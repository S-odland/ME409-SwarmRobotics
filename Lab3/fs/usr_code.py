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
		R = 0.25
	else:
		robot.set_led(0,0,100)
		R = 0.35
	
	def alignHeading(theta,phi,vel):
		if phi < 0:
			if abs(theta - phi) > 0.05:
				robot.set_vel(-75,75)
				return 0
			else:
				robot.set_vel(vel,vel)
				return 1
		else:
			if abs(abs(theta) - phi) > 0.05:
				robot.set_vel(-75,75)
				return 0
			else:
				robot.set_vel(vel,vel)
				return 1

	def taxisVec(robot):
		while 1:
			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t
				phi = math.atan(abs(pos[1]/pos[0]))

				if pos[0] < 0 and pos[1] > 0:
					phi = -phi
					aligned = alignHeading(pos[2],phi,0)
				elif pos[0] > 0 and pos[1] < 0:
					phi = -phi+math.pi
					aligned = alignHeading(pos[2],phi,0)
				elif pos[0] > 0 and pos[1] > 0:
					phi = phi - math.pi
					aligned = alignHeading(pos[2],phi,0)
				else:
					aligned = alignHeading(pos[2],phi,0)

				if aligned == 1: return phi

	def repulVec(robot):
		k = 150
		phiT = 0
		neighbors = []
		i = 0
		aligned = 0
		while 1:
			i+=1
			pos_t = robot.get_pose()
			if pos_t:
				pos = pos_t
				robot.send_msg(struct.pack("ffi",pos[0],pos[1],robot.id))
			msgs = robot.recv_msg()
			if len(msgs) > 0:
				x,y,rId = struct.unpack('ffi',msgs[0][:12])
				pos_t = robot.get_pose()
				if pos_t:
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
						
						aligned = alignHeading(pos[2],phi,0)

					if aligned == 1: return phiAve,velAve
					elif len(neighbors) == 0 and i > 100: return 0,0
	
	def randVec(robot):
		phi = robot.random.uniform(-math.pi,math.pi)
		return phi
	
	def getDot(phi,vel):
		xdot = math.cos(phi)*vel
		ydot = math.sin(phi)*vel
		return xdot,ydot
	
	def getHeading(xdot,ydot):
		phi = math.asin(ydot/100)
		return phi

	while(1):

		dirTaxis = taxisVec(robot)
		dirRepul,magRepel = repulVec(robot)
		dirRand = randVec(robot)

		if dirRepul != 0:
			taxisX,taxisY = getDot(dirTaxis,50)
			repulX,repulY = getDot(dirRepul,magRepel)
			randoX,randoY = getDot(dirRand,25)

			xave = (taxisX + repulX + randoX)/3
			yave = (taxisY + repulY + randoY)/3
		else:
			taxisX,taxisY = getDot(dirTaxis,100)
			randoX,randoY = getDot(dirRand,100)

			xave = (taxisX + randoX)/2
			yave = (taxisY + randoY)/2			

		phi = getHeading(xave,yave)
		pos_t = robot.get_pose()
		if pos_t:
			pos = pos_t
			alignHeading(pos[2],phi,100)
		
			time.sleep(10)





