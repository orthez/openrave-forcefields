import abc
import time
import numpy as np
from scipy.interpolate import interp1d,splev,splrep,splprep
from scipy.misc import derivative
from pylab import plot,title,xlabel,ylabel
import pylab as plt

class Trajectory():
        __metaclass__ = abc.ABCMeta

        traj = []
        waypoints = []
        handle = []

        ptsize = 0.05
        FONT_SIZE = 10

        trajectory_color = np.array((0.7,0.2,0.7,0.9))

        def __init__(self, trajectory, waypoints_in = []):
                self.traj = trajectory 
                self.waypoints = waypoints_in

        def info(self):
                print "#### TRAJECTORY CLASS ######"
                print "LENGTH: ", self.get_length()

                [f0,df0] = np.around(self.evaluate_at(0),2)
                [f1,df1] = np.around(self.evaluate_at(1),2)

                print "START      : ", f0, " dir: ", df0
                print "GOAL       : ", f1, " dir: ", df1
                print "WAYPOINTS  : "
                print "             [   T   ]  [  WAYPOINT  ]"
                for tt in np.linspace(0,1,10):
                        [f,df]=self.evaluate_at(tt)
                        print "             [ ",np.around(tt,1)," ] ",np.around(f,decimals=2)

        def get_dimension(self):
                [F,dF] = self.evaluate_at(0)
                return F.shape[0]

        def get_forces_at_waypoints(self, W, env):
                Nwaypoints = W.shape[1]
                F = np.zeros((3,Nwaypoints))
                for i in range(0,Nwaypoints):
                        pt = np.array(((W[0,i],W[1,i],-0.1,0.001)))
                        F[:,i] = env.GetForceAtX(pt)
                return F

        def plot_speed_profile(self, env):

                L = self.get_length()
                dt = 0.05
                Nwaypoints = int(L/dt)
                [W,dW] = self.get_waypoints(N=Nwaypoints)

                F = self.get_forces_at_waypoints(W, env)
                print F.shape,Nwaypoints

                V = np.zeros((Nwaypoints-1))
                T = np.linspace(0.0,1.0,num=Nwaypoints-1)
                for i in range(0,Nwaypoints-1):
                        V[i] = self.get_minimum_feasible_velocity(W[:,i],W[:,i+1],F[:,i])

                plot(T,V,'or',linewidth=3,markersize=2)        
                title('Speed Profile Trajectory', fontsize=self.FONT_SIZE)
                xlabel('$\theta$', fontsize=self.FONT_SIZE)
                ylabel('$s$', fontsize=self.FONT_SIZE)
                plt.show()


        def get_minimum_feasible_velocity(self, W1, W2, F):
                d = np.linalg.norm(F)
                if d > 0.5:
                        return 0.8
                else:
                        return 0.01


        @abc.abstractmethod 
        def evaluate_at(self, t):
                pass

        @classmethod
        def from_waypoints(cls, W):
                pass

        @classmethod
        def from_ravetraj(cls, ravetraj):
                N = ravetraj.GetNumWaypoints()
                W=[]
                for i in range(0,N):
                        w = np.array((ravetraj.GetWaypoint(i)[0],ravetraj.GetWaypoint(i)[1],ravetraj.GetWaypoint(i)[2]))
                        W.append((w))
                W = np.array(W).T
                return cls.from_waypoints(W)

        def get_waypoints(self, N = 100):
                K = self.get_dimension()
                pts = np.zeros((K,N))
                dpts = np.zeros((K,N))
                ctr = 0
                for t in np.linspace(0.0, 1.0, num=N):
                        [f0,df0] = self.evaluate_at(t)
                        pts[:,ctr] = f0
                        dpts[:,ctr] = df0
                        ctr = ctr+1
                return [pts,dpts]

        def get_length(self):
                dt = 0.05
                dd = 0.0
                for t in np.linspace(0.0, 1.0-dt, num=1000):
                        [ft,df0] = self.evaluate_at(t)
                        [ftdt,df0] = self.evaluate_at(t+dt)
                        dd = dd + np.linalg.norm(ft-ftdt)
                return dd

        def draw(self, env, keep_handle=True):
                Nwaypoints=200
                [W,dW] = self.get_waypoints(N=Nwaypoints)

                tmp_handle = []
                for i in range(0,Nwaypoints):
                        pt = np.array(((W[0,i],W[1,i],W[2,i])))
                        tmp_handle.append(env.env.plot3(points=pt,
                                           pointsize=self.ptsize,
                                           colors=self.trajectory_color,
                                           drawstyle=1))
                if keep_handle:
                        self.handle = tmp_handle
                else:
                        return tmp_handle


        def draw_delete(self, env):
                self.handle = []