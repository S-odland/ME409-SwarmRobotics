def usr(robot):
	import struct
	import math
	import timeit
	import time

	## the only time r1 and r2 will send out hops

	for j in range(0,500):
		if robot.assigned_id == 2:
			hop_count = 0
			s_hop = 1
			robot.set_led(100,0,0)
			robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))

		elif robot.assigned_id == 1:
			hop_count = 0
			# s_hop = 1
			# robot.set_led(100,0,0)
			# robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))

		elif robot.assigned_id == 0:
			msgs = robot.recv_msg()

			if len(msgs) > 0:
				broadcast = struct.unpack('ii',msgs[0][:8]) 
				hop_count= broadcast[0]
			else:
				hop_count = 40

	for mat in range(1,21):
		for j in range(0,250):
			if robot.assigned_id == 0 and hop_count == mat:
				robot.send_msg(struct.pack('ii',hop_count+1,robot.assigned_id))
			elif robot.assigned_id == 0:
				msgs = robot.recv_msg()
				if len(msgs) > 0:
					broadcast = struct.unpack('ii',msgs[0][:8]) 
					if broadcast[0] > hop_count:
						pass
					else:
						hop_count = broadcast[0]

	if hop_count % 2 == 0:
		robot.set_led(100,0,0)
	else:
		robot.set_led(0,100,0)

	# for mart in range(0,100):
	# 	if robot.assigned_id == 0 and i_hop == 2:
	# 		robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))
	# 	elif robot.assigned_id == 0 and i_hop > 2:
	# 		msgs = robot.recv_msg()
	# 		if len(msgs) > 0:
	# 			broadcast = struct.unpack('ii',msgs[0][:8]) 
	# 			i_hop = broadcast[0]
	# 			s_hop = i_hop +1
	# 		else:
	# 			i_hop = 4

	# for j in range(0,250):
	# 	if robot.assigned_id == 0 and i_hop == 3:
	# 		robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))
	# 	elif robot.assigned_id == 0 and i_hop > 3:
	# 		msgs = robot.recv_msg()
	# 		if len(msgs) > 0:
	# 			broadcast = struct.unpack('ii',msgs[0][:8]) 
	# 			i_hop = broadcast[0]
	# 			s_hop = i_hop +1
	# 			print(i_hop)
	# 		else:
	# 			i_hop = 5
	
	# for j in range(0,250):
	# 	if robot.assigned_id == 0 and i_hop == 4:
	# 		robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))
	# 	elif robot.assigned_id == 0 and i_hop > 4:
	# 		msgs = robot.recv_msg()
	# 		if len(msgs) > 0:
	# 			broadcast = struct.unpack('ii',msgs[0][:8]) 
	# 			i_hop = broadcast[0]
	# 			s_hop = i_hop +1
	# 			print(i_hop)
	# 		else:
	# 			i_hop = 6


	# for j in range(0,250):
	# 	if robot.assigned_id == 0 and i_hop == 5:
	# 		robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))
	# 	elif robot.assigned_id == 0 and i_hop > 5:
	# 		msgs = robot.recv_msg()
	# 		if len(msgs) > 0:
	# 			broadcast = struct.unpack('ii',msgs[0][:8]) 
	# 			i_hop = broadcast[0]
	# 			s_hop = i_hop +1
	# 			print(i_hop)
	# 		else:
	# 			i_hop = 7

	# for j in range(0,250):
	# 	if robot.assigned_id == 0 and i_hop == 6:
	# 		robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))
	# 	elif robot.assigned_id == 0 and i_hop > 6:
	# 		msgs = robot.recv_msg()
	# 		if len(msgs) > 0:
	# 			broadcast = struct.unpack('ii',msgs[0][:8]) 
	# 			i_hop = broadcast[0]
	# 			s_hop = i_hop +1
	# 			print(i_hop)
	# 		else:
	# 			i_hop = 8

	# for j in range(0,250):
	# 	if robot.assigned_id == 0 and i_hop == 7:
	# 		robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))
	# 	elif robot.assigned_id == 0 and i_hop > 7:
	# 		msgs = robot.recv_msg()
	# 		if len(msgs) > 0:
	# 			broadcast = struct.unpack('ii',msgs[0][:8]) 
	# 			if i_hop < broadcast[0]:
	# 				pass
	# 			else:
	# 				i_hop = broadcast[0]
	# 				s_hop = i_hop +1
	# 				print(i_hop)
	# 		else:
	# 			i_hop = 9

	# for j in range(0,250):
	# 	if robot.assigned_id == 0 and i_hop == 8:
	# 		robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))
	# 	elif robot.assigned_id == 0 and i_hop > 8:
	# 		msgs = robot.recv_msg()
	# 		if len(msgs) > 0:
	# 			broadcast = struct.unpack('ii',msgs[0][:8]) 
	# 			if i_hop < broadcast[0]:
	# 				pass
	# 			else:
	# 				i_hop = broadcast[0]
	# 				s_hop = i_hop +1
	# 				print(i_hop)
	# 		else:
	# 			i_hop = 10

	# for j in range(0,250):
	# 	if robot.assigned_id == 0 and i_hop == 9:
	# 		robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))
	# 	elif robot.assigned_id == 0 and i_hop > 9:
	# 		msgs = robot.recv_msg()
	# 		if len(msgs) > 0:
	# 			broadcast = struct.unpack('ii',msgs[0][:8]) 
	# 			if i_hop < broadcast[0]:
	# 				pass
	# 			else:
	# 				i_hop = broadcast[0]
	# 				s_hop = i_hop +1
	# 				print(i_hop)
	# 		else:
	# 			i_hop = 11

	# # for mar in range(1,4):
	# # 	for j in range(0,300):
	# # 		if robot.assigned_id == 0 and i_hop == mar:
	# # 			robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))
	# # 		elif robot.assigned_id == 0 and i_hop > mar:
	# # 			msgs = robot.recv_msg()
	# # 			if len(msgs) > 0:
	# # 				broadcast = struct.unpack('ii',msgs[0][:8]) 
	# # 				if i_hop < broadcast[0]:
	# # 					pass
	# # 				else:
	# # 					i_hop = broadcast[0]
	# # 					s_hop = i_hop +1
	# # 			else:
	# # 				i_hop = mar+2

	# # for mar in range(4,7):
	# # 	for j in range(0,300):
	# # 		if robot.assigned_id == 0 and i_hop == mar:
	# # 			robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))
	# # 		elif robot.assigned_id == 0 and i_hop > mar:
	# # 			msgs = robot.recv_msg()
	# # 			if len(msgs) > 0:
	# # 				broadcast = struct.unpack('ii',msgs[0][:8]) 
	# # 				if i_hop < broadcast[0]:
	# # 					pass
	# # 				else:
	# # 					i_hop = broadcast[0]
	# # 					s_hop = i_hop +1
	# # 			else:
	# # 				i_hop = mar+2

	# if robot.assigned_id == 0 and hop_count == 1:
	# 	robot.set_led(0,100,0)
	# elif robot.assigned_id == 0 and hop_count == 2:
	# 	robot.set_led(100,0,0)
	# elif robot.assigned_id == 0 and hop_count == 3:
	# 	robot.set_led(0,100,0)
	# elif robot.assigned_id == 0 and hop_count == 4:
	# 	robot.set_led(100,0,0)
	# elif robot.assigned_id == 0 and hop_count == 5:
	# 	robot.set_led(0,100,0)
	# elif robot.assigned_id == 0 and hop_count == 6:
	# 	robot.set_led(100,0,0)
	# elif robot.assigned_id == 0 and i_hop == 7:
	# 	robot.set_led(0,100,0)
	# elif robot.assigned_id == 0 and i_hop == 8:
	# 	robot.set_led(100,0,0)
	# elif robot.assigned_id == 0 and i_hop == 9:
	# 	robot.set_led(0,100,0)

	

	# for j in range(0,200):
	# 	if robot.assigned_id == 0 and i_hop % 2 == 0:
	# 		robot.set_led(0,100,0)
	



# 	while True:



# 		tic = time.time()
# 		msgs = robot.recv_msg()
# 		toc = time.time()

# 		if len(msgs) > 0:

# 			time_elapsed = abs(tic - toc)
# 			broadcast = struct.unpack('ii',msgs[0][:8]) 
			
# ############ 1 HOP = 0.0004 = TIME_ELAPSED #################
# ############ 12 HOPS IN TOTAL ##############################

# 			if robot.assigned_id == 0 and time_elapsed <= 0.0019:	
# 				print(broadcast[0],broadcast[1])			
# 				i_hop = broadcast[0]
# 				s_hop = i_hop + 1
# 				robot.set_led(0,100,0)
# 				robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))