import abc
import time
import numpy as np

from trajectory import *
#from trajectory_utils import *

class TrajectoryDeformation():
        __metaclass__ = abc.ABCMeta

        env = []
        traj_ori = []
        traj_deformed = []
        handle = []


        def __init__(self, trajectory, environment):
                self.env = environment
                self.traj_ori = trajectory 
                self.traj_deformed = trajectory 

        @abc.abstractmethod 
        def deform_onestep(self):
                pass

        def deform(self, N_iter = 1):
                for i in range(0,N_iter):
                        self.deform_onestep()


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
                print Nwaypoints

                #[W0,dW] = TrajectoryToWaypoints(self.traj_ori,N=Nwaypoints)
                #[W1,dW] = TrajectoryToWaypoints(self.traj_deformed,N=Nwaypoints)
                [W0,dW] = self.traj_ori.get_waypoints(N=Nwaypoints) 
                [W1,dW] = self.traj_deformed.get_waypoints(N=Nwaypoints) 

                
                for i in range(0,M):
                        k = float(i)/float(M)
                        Wk = (1-k)*W0 + k*W1
                        Tk = Trajectory.from_waypoints(Wk)
                        self.handle = Tk.draw(self.env, keep_handle=False)
                        time.sleep(0.01)

        def draw_waypoints(self, Win):
                Nwaypoints = Win.shape[1]

                self.handle = []
                for i in range(0,Nwaypoints):
                        pt = np.array(((Win[0,i],Win[1,i],0.1)))
                        self.handle.append(self.env.env.plot3(points=pt,
                                           pointsize=self.ptsize,
                                           colors=np.array(((0.1,0.7,0.1,0.9))),
                                           drawstyle=1))


        def draw_trajectory_original(self):
                self.traj_ori.draw(self.env)

        def draw_trajectory_deformed(self):
                self.traj_deformed.draw(self.env)



        #def DrawRedPoint(self,env,X):
        #        self.handles.append(env.env.plot3(points=X,
        #                           pointsize=self.ptsize,
        #                           colors=np.array(((0.8,0.0,0.0,0.9))),
        #                           drawstyle=1))

        #def DrawRedArrow(self,env,X,dX):
        #        A = env.env.drawarrow(X,X+dX,linewidth=0.02,color=np.array((1,0,0)))
        #        self.handles.append(A)

        #def DrawGreenPoint(self,env,X):
        #        self.handles.append(env.env.plot3(points=X,
        #                           pointsize=self.ptsize,
        #                           colors=np.array(((0.0,0.8,0.0,0.9))),
        #                           drawstyle=1))

