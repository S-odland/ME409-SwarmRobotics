def usr(robot):
	import struct
	import math
	import timeit
	import time

######### START HOP COUNT CODE ############

## the only time r1 and r2 will send out hops
	hop_count = [40,40]
	for j in range(0,500):

		# if the robot is 1 send  out a message of hop = 1 to neighbors and its ids
		if robot.assigned_id == 1:
			hop_count = [0,0]
			robot.set_led(100,0,0)
			robot.send_msg(struct.pack('ii',hop_count[0]+1,robot.assigned_id))
		
		elif robot.assigned_id == 0:
			msgs = robot.recv_msg()

			if len(msgs) > 0:
				broadcast = struct.unpack('ii',msgs[0][:8]) 
				if broadcast[1] == 1:
					hop_count[0] = broadcast[0]

	for j in range(0,500):

		#if robot is 2 send out a message of hop = 1 to neighbors and its id
		if robot.assigned_id == 2:
			hop_count = [0,0]
			robot.set_led(100,0,0)
			robot.send_msg(struct.pack('ii',hop_count[0]+1,robot.assigned_id))
			
		elif robot.assigned_id == 0:
			msgs = robot.recv_msg()

			if len(msgs) > 0:
				broadcast = struct.unpack('ii',msgs[0][:8]) 
				if broadcast[1] == 2:
					hop_count[1] = broadcast[0]

# outer for loop is for recving dif seed messages
	for seed in range(0,2):
# for cycling through hop counts
		for mat in range(1,21):
# for making sure all robots that can recv a msg recv a msg
			for j in range(0,250):
# if the robot is the hop count iteration send its hop count to neighbors
				if hop_count[seed] == mat:
					robot.send_msg(struct.pack('ii',hop_count[seed]+1,robot.assigned_id))
				else:
					msgs = robot.recv_msg()
					if len(msgs) > 0:
						broadcast = struct.unpack('ii',msgs[0][:8]) 
# if the robot recvs a message and its hop is lower than the recvd hop do nothing
						if broadcast[0] > hop_count[seed]:
							pass
# otherwise reassign the hop 
						else:
							hop_count[seed] = broadcast[0]
		
	# if hop_count[0] % 2 == 0:
	# 	robot.set_led(100,0,0)
		
	# else:
	# 	robot.set_led(0,100,0)

############### HOP COUNT (GRADIENTS) ESTABLISHED ##################

############### START COORDINATE GENERATION #######################
 ## Approximate 1 hop distance to be 2 (arbitray # -> units dont matter)
 ## so d_hat = hop_count * 2

	scale = 2
	d_hat = [hop_count[0] * scale, hop_count[1] *scale]
	#pos1 = [0,0]
	pos2 = [15*scale,0] # seed to is 15 hops away from seed 1 - by inspection
	Ej = 100
	lse_x = 0
	lse_y = 0
	upboundX = 15*scale + 1
	upboundY = 18*scale + 1
	pos = [0,0]

	# finding sensor j's total error
	# set the max x value to be 15*scale and the max y value to be 18*scale

	for x in range(0,upboundX):
		for y in range(0,upboundY):

			dj1 = math.sqrt(x**2 + y**2)
			dj2 = math.sqrt((x-pos2[0])**2 + y**2)

			Ej1 = (dj1 - d_hat[0])**2
			Ej2 = (dj2 - d_hat[1])**2

			Ej_new = sum([Ej1,Ej2])

			if Ej_new < Ej:
				Ej = Ej_new
				lse_x = x
				lse_y = y
				pos = [lse_x,lse_y]

				print(pos)
	
	if pos[0] <= 15:
		robot.set_led(0,100,0)
