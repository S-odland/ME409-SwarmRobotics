def usr(robot):
    import struct
    import math
    import timeit

    R = 0.25 ## radius of separation for robots

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
    sep_vec_s = [0,0]
    com = [0,0]

    ## state 1: migration vector
    ## state 2: separation vector
    ## state 3: cohesion vector
    ## state 4: alignment vector

    while 1:

        if state == 1:
            pos_t = robot.get_pose()
            if pos_t:
                pos = pos_t
                mag_vec = math.hypot(pos[0],pos[1])
                if mag_vec == 0:
                    mig_vec = [0,0]
                    state = 2
                else:
                    mig_vec = [-pos[0]/mag_vec,-pos[1]/mag_vec] ## gives unit vector of taxis
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
                    pos = pos_t 
                    rAct = math.hypot(pos[0]-x,pos[1]-y)
                    ## check virtual overlap
                    if rAct < R:
                        i += 1
                        weight = k*(R-rAct)
                        sep_vec = [weight*(pos[0]-x),weight*(pos[1]-y)]
                        #make sure that this robot hasn't been calculated in vector sum
                        if rId not in neighbors:
                            neighbors.append(rId)
                            com[0] += x
                            com[1] += y
                            sep_vec_s[0] += sep_vec[0]
                            sep_vec_s[1] += sep_vec[1]
            # i is the inner loop (recieved messages) j is outer loop -- ensures that lone robots dont get stuck in state 2
            if i > 15 or j > 350:
                com[0] = (com[0] + pos[0])/len(neighbors)
                com[1] = (com[1] + pos[1])/len(neighbors)

                coh_vec = [pos[0] - com[0],pos[1] - com[1]]

                j = 0
                i = 0
                neighbors = []
                state = 3

        if state == 3:
            # normalizing repulsion vec to be below 8
            if math.hypot(sep_vec_s[0],sep_vec_s[1]) > 8:
                rat = 8/math.hypot(sep_vec_s[0],sep_vec_s[1])
                sep_vec_s[0] = sep_vec_s[0]*rat
                sep_vec_s[1] = sep_vec_s[1]*rat

        # found that the repulsion vec weight to be higher made the brazil effect clearer
            pos_t = robot.get_pose()
            if pos_t:
                pos = pos_t
                # summing up vector
                tot_vec = [coh_vec[0] + mig_vec[0] + sep_vec_s[0],coh_vec[1] + mig_vec[1] + sep_vec_s[1]]
                phi = math.atan2(tot_vec[1],tot_vec[0])
                aligned = alignHeading(pos[2],phi)
                if aligned:
                    state = 4

        ## hard coding the velocity makes it converge faster
        if state == 4:
            robot.set_vel(75,75)
            time.sleep(1)
            robot.set_vel(0,0)
            sep_vec_s = [0,0]
            com = [0,0]
            coh_vec = [0,0]
            mig_vec = [0,0]
            state = 1






