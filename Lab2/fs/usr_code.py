def usr(robot):
	import struct
	import math
	import timeit
	import time

	## the only time r1 and r2 will send out hops

	for j in range(0,500):
		if robot.assigned_id == 1:
			hop_count = 0
			s_hop = 1
			robot.set_led(100,0,0)
			robot.send_msg(struct.pack('ii',s_hop,robot.assigned_id))

		elif robot.assigned_id == 2:
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

