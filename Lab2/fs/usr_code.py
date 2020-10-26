def usr(robot):
	import struct
	import math
	import timeit
	import time

	## the only time r1 and r2 will send out hops

	for j in range(0,500):

		# if the robot is 1 send  out a message of hop = 1 to neighbors and its ids
		if robot.assigned_id == 1:
			hop_count = [0,0]
			robot.set_led(100,0,0)
			robot.send_msg(struct.pack('ii',hop_count[0]+1,robot.assigned_id))

		#if robot is 2 send out a message of hop = 1 to neighbors and its id
		elif robot.assigned_id == 2:
			hop_count = [0,0]
			robot.set_led(100,0,0)
			robot.send_msg(struct.pack('ii',hop_count[0]+1,robot.assigned_id))

		# if robot is 0 receive a message and check which seed sent it. 
		#
		# if the seed is 1 assign hop_count[0] to be seed 1's sent hop count, if seed = 2 assign hop_count[1] to 
		# be seed 2's hop count
		#
		# if 0 doesn't get the message assign both hop counts to be 40
		#
		# i used 40 here so that the hop count would always be overwritten when it does receieve a message
		# later in the code.
		elif robot.assigned_id == 0:
			msgs = robot.recv_msg()

			if len(msgs) > 0:
				broadcast = struct.unpack('ii',msgs[0][:8]) 
				if broadcast[1] == 1:
					hop_count = [broadcast[0],40]
				elif broadcast[1] == 2:
					hop_count = [40,broadcast[0]]
			else:
				hop_count = [40,40]

# outer for loop is for recving dif seed messages
	if robot.assigned_id == 0:
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
		
	if hop_count[0] % 2 == 0:
		robot.set_led(100,0,0)
	else:
		robot.set_led(0,100,0)
	
	# if hop_count[1] % 2 == 0:
	# 	robot.set_led(100,0,0)
	# else:
	# 	robot.set_led(0,100,0)

