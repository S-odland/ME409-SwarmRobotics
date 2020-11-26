def usr(robot):
    import struct
    import math
    import timeit
    import time

    R = 0.25 ## radius of separation for robots

	## function to align heading of robot with desired angle -- error of 10%
    def alignHeading(theta,phi):
        
        ## the idea with this conditional is that there are four checks to see if we want left turning or right turning for the shortest degree rotation
        if ((phi < 0 and theta > phi) or (phi < 0 and phi < theta < (math.pi + phi))) or ((phi > 0 and theta > phi) or (phi > 0 and (math.pi - phi) < theta < phi)):
            turn_r = -1
            turn_l = 1
        else:
            turn_r = 1
            turn_l = -1
        
        if abs(theta - phi) > 0.1:
            #robot.set_vel(-75,75)
            robot.set_vel(75 + turn_l*25,75 + turn_r*25)
            print(turn_l,turn_r)
            ##robot.set_vel(50 + turn_l*25,50 + turn_r*25) ## makes it so that turning depends on the path of shortest rotation (may have to deal with sharper turns later)
            return 0
        else:
            robot.set_vel(0,0)
            return 1


## possibly add a conditional or a variable that scales to change how sharp a turn is?

    state = 1
    j = 0
    neighbors = []
    i = 0
    sep_vec_s = [0,0]
    com = [0,0]
    al_h = [0,0]

    ## state 1: migration vector
    ## state 2: separation, cohesion, alignment vector
    ## state 3: summation and alignment
    ## state 4: movement (we can either have swarm sense, align, move or do all of it simultaneously)
    ##
    ## If we have continuous motion, state 4 will never have a time.sleep call and will never have the velocity set to 0
    ## Would have to change align heading to be a rotation + or - a set velocity, i.e. (50 +- 25, 50 -+ 25) or something of the sort
    ## Would also have to add a case for shortest path of rotation 

    while 1:

        if state == 1:
            pos_t = robot.get_pose()
            if pos_t:
                pos = pos_t
                mag_vec = math.hypot(pos[0],pos[1])
                if mag_vec == 0:
                    mig_vec = [0,0]
                    state = 3
                else:
                    mig_vec = [-pos[0]/mag_vec,-pos[1]/mag_vec] ## gives unit vector of taxis
                    state = 3

        # if state == 2:
        #     pos_t = robot.get_pose()
        #     if pos_t:
        #         pos = pos_t
        #         robot.send_msg(struct.pack("fffi",pos[0],pos[1],pos[2],robot.id))
        #         j += 1
        #     msgs = robot.recv_msg()
        #     if len(msgs) > 0:
        #         x,y,theta,rId = struct.unpack('fffi',msgs[0][:16])
        #         pos_t = robot.get_pose()
        #         if pos_t:
        #             i += 1
        #             pos = pos_t 
        #             rAct = math.hypot(pos[0]-x,pos[1]-y)
        #             ## check virtual overlap
        #             if rAct < R:
        #                 weight = k*(R-rAct)
        #                 sep_vec = [weight*(pos[0]-x),weight*(pos[1]-y)]
        #                 #make sure that this robot hasn't been calculated in vector sum
        #                 if rId not in neighbors:
        #                     al_h[0] += math.cos(theta)
        #                     al_h[1] += math.sin(theta)
        #                     neighbors.append(rId)
        #                     com[0] += x
        #                     com[1] += y
        #                     sep_vec_s[0] += sep_vec[0]
        #                     sep_vec_s[1] += sep_vec[1]
        #     # i is the inner loop (recieved messages) j is outer loop -- ensures that lone robots dont get stuck in state 2
        #     if i > 15 or j > 350:
        #         ## center of mass of all the robots
        #         com[0] = (com[0] + pos[0])/(len(neighbors) + 1)
        #         com[1] = (com[1] + pos[1])/(len(neighbors) + 1)
        #         ## vector aligned with the average heading of the swarm
        #         aln_vec = [(al_h[0] + math.cos(pos[2]))/(len(neighbors) + 1), \
        #                    (al_h[1] + math.sin(pos[2]))/(len(neighbors) + 1)]
        #         ## vector towards the center of mass of the neighbors
        #         coh_vec = [-(pos[0] - com[0]),-(pos[1] - com[1])]
        #         j = 0
        #         i = 0
        #         neighbors = []
        #         state = 3

        if state == 3:
            # found that the repulsion vec weight to be higher made the brazil effect clearer
            pos_t = robot.get_pose()
            if pos_t:
                pos = pos_t
                # summing up vector
                #tot_vec = [coh_vec[0] + (1/(8*math.sqrt(2)))*mig_vec[0] + 1.2*sep_vec_s[0] + aln_vec[0], \
                #           coh_vec[1] + (1/(8*math.sqrt(2)))*mig_vec[1] + 1.2*sep_vec_s[1] + aln_vec[1]]
                phi = math.atan2(mig_vec[1],mig_vec[0])
                aligned = alignHeading(pos[2],phi)
                if aligned:
                    state = 4

        ## hard coding the velocity makes it converge faster
        if state == 4:
            robot.set_vel(100,100)
            time.sleep(1)
            robot.set_vel(0,0)
            sep_vec_s = [0,0]
            com = [0,0]
            coh_vec = [0,0]
            mig_vec = [0,0]
            al_h = [0,0]
            aln_vec = [0,0]
            state = 1






