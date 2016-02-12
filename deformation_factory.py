import abc
import sys
import time
import numpy as np
from copy import copy
from trajectory import *

class Deformation():
        __metaclass__ = abc.ABCMeta

        env = []
        traj_ori = []
        traj_deformed = []
        traj_current = []

        traj_display = []
        handle = []


        def __init__(self, trajectory, environment):
                self.env = environment

                ## traj_ori : original trajectory before any calls
                ## traj_current : the current deformation
                ## traj_deformed : the working copy of current for the next iteration
                ## traj_display : the trajectory which we display at the moment
                self.traj_ori = trajectory 
                self.traj_current = copy(trajectory)
                self.traj_deformed = copy(trajectory)
                self.traj_display = copy(trajectory)

        @abc.abstractmethod 
        def deform_onestep(self):
                pass

        def deform(self, N_iter = 1):
                for i in range(0,N_iter):
                        self.deform_onestep()
                        self.traj_current = copy(self.traj_deformed)

        def GetForcesAtWaypoints(self, W):
                Nwaypoints = W.shape[1]
                F = np.zeros((3,Nwaypoints))
                for i in range(0,Nwaypoints):
                        pt = np.array(((W[0,i],W[1,i],-0.1,0.001)))
                        F[:,i] = self.env.GetForceAtX(pt)
                return F

        def GetFirstInfeasibleWaypoint(self, W, dW, F):
                Nwaypoints = W.shape[1]
                for i in range(0,Nwaypoints):
                        d = np.linalg.norm(F[:,i])
                        pt = np.array(((W[0,i],W[1,i],0.1)))
                        if d > 0.2:
                                return i


        def draw_deformation(self):
                M = 20
                L = self.traj_ori.get_length()
                dt = 0.05
                Nwaypoints = int(L/dt)

                print self.traj_display.info()
                print self.traj_current.info()

                [W0,dW] = self.traj_display.get_waypoints(N=Nwaypoints) 
                [W1,dW] = self.traj_current.get_waypoints(N=Nwaypoints) 

                for i in range(0,M):
                        k = float(i)/float(M)
                        Wk = (1-k)*W0 + k*W1
                        self.traj_current.new_from_waypoints(Wk)
                        self.handle = self.traj_current.draw(self.env, keep_handle=False)
                        #if i == 0:
                                #raw_input('Press <ENTER> to draw deformation.')
                        time.sleep(0.1)

                self.traj_display = copy(self.traj_current)


        def draw_trajectory_original(self):
                self.traj_ori.draw(self.env)

        def draw_trajectory_deformed(self):
                self.traj_current.draw(self.env)
