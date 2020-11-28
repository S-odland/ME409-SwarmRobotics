def usr(robot):
    import struct
    import math
    import timeit
    import time

    R = 5 ## radius of separation for robots

	## function to align heading of robot with desired angle -- error of 10
    def alignHeading(theta,phi):
        e = theta - phi
        ## the idea with this conditional is that there are four checks to see if we want left turning or right turning for the shortest degree rotation
        if (e < 0 and abs(e) < 180) or (e > 0 and abs(e) > 180):
            turn_r = abs(e)
            turn_l = -abs(e)
        else:
            turn_r = -abs(e)
            turn_l = abs(e)
        
        if abs(e) > 0.1:
            #robot.set_vel(-75,75)
            robot.set_vel(55 + turn_l*45,55 + turn_r*45)
            return 0
        else:
            robot.set_vel(100,100)

            return 1
    
    def normUnit(vec):
        mag_vec = math.hypot(vec[0],vec[1])
        if mag_vec == 0:
            vec = [0,0]
        else:
            vec = [vec[0]/mag_vec,vec[1]/mag_vec] ## gives unit vector of taxis
        return vec

    state = 1
    neighbors = []
    i = 0
    sep_vec_s = [0,0]
    com = [0,0]
    al_h = [0,0]

    ## state 1: migration vector
    ## state 2: separation, cohesion, alignment vector
    ## state 3: summation and alignment
    
    while 1:
        if state == 1:
            pos_t = robot.get_pose()
            if pos_t:
                pos = pos_t
                vec = [-pos[0],-pos[1]]
                mig_vec = normUnit(vec)
                robot.send_msg(struct.pack("fffi",pos[0],pos[1],pos[2],robot.id))
            msgs = robot.recv_msg()
            if len(msgs) > 0:
                x,y,theta,rId = struct.unpack('fffi',msgs[0][:16])
                pos_t = robot.get_pose()
                if pos_t:
                    i += 1
                    pos = pos_t 
                    rAct = math.hypot(pos[0]-x,pos[1]-y)
                    ## check virtual overlap
                    if rAct < R:
                        weight = 1/(R-rAct)
                        sep_vec = [round(weight*(pos[0]-x),2),round(weight*(pos[1]-y),2)]
                        #make sure that this robot hasn't been calculated in vector sum
                        if rId not in neighbors:
                            al_h[0] += math.cos(theta)
                            al_h[1] += math.sin(theta)
                            neighbors.append(rId)
                            com[0] += x
                            com[1] += y
                            sep_vec_s[0] += sep_vec[0]
                            sep_vec_s[1] += sep_vec[1]
            # i is the inner loop (recieved messages) j is outer loop -- ensures that lone robots dont get stuck in state 2
            if i > 20:
                ## center of mass of all the robots
                com[0] = com[0]/(len(neighbors) + 1)
                com[1] = com[1]/(len(neighbors) + 1)
                ## vector aligned with the average heading of the swarm
                aln_vec = [(al_h[0] + math.cos(pos[2]))/(len(neighbors) + 1), \
                           (al_h[1] + math.sin(pos[2]))/(len(neighbors) + 1)]
                ## vector towards the center of mass of the neighbors
                coh_vec = [-(pos[0] - com[0]),-(pos[1] - com[1])]
                i = 0
                neighbors = []
                state = 2

        if state == 2:
            #normalize vectors to 1 (a unit vector)
            sep_vec_s = normUnit(sep_vec_s)
            aln_vec = normUnit(aln_vec)
            coh_vec = normUnit(coh_vec)
            # found that the repulsion vec weight to be higher made the brazil effect clearer
            pos_t = robot.get_pose()
            if pos_t:
                pos = pos_t
                # summing up vector
                tot_vec = [coh_vec[0] + 1/1.5*mig_vec[0] + 1.1*sep_vec_s[0] + aln_vec[0], \
                           coh_vec[1] + 1/1.5*mig_vec[1] + 1.1*sep_vec_s[1] + aln_vec[1]]
                phi = math.atan2(tot_vec[1],tot_vec[0])
                aligned = alignHeading(pos[2],phi)
                if aligned:
                    sep_vec_s = [0,0]
                    com = [0,0]
                    coh_vec = [0,0]
                    mig_vec = [0,0]
                    al_h = [0,0]
                    aln_vec = [0,0]
                    state = 1






