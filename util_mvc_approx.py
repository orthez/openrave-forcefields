import string,time
from pylab import *
import numpy as np
from openravepy import *
import TOPP
from TOPP import Utilities
from TOPP import TOPPbindings
from TOPP import TOPPpy
from TOPP import Trajectory
from TOPP import TOPPopenravepy

def GetTrajectoryString(W, dW, ddW):
        ### get trajectory string for any R subspaces
        Ndim = W.shape[0]
        Nwaypoints = W.shape[1]
        durationVector = np.zeros((Nwaypoints-1))

        duration = 1
        for i in range(0,Nwaypoints-1):
                ds = np.linalg.norm(W[:,i+1]-W[:,i])
                dv = np.linalg.norm(dW[:,i])
                #duration = ds/dv
                #duration = 0.001
                durationVector[i] = duration
                if i==0:
                        trajectorystring = str(duration)
                else:
                        trajectorystring += "\n" + str(duration)

                trajectorystring += "\n" + str(Ndim)

                #P(t) = A + Bt1 + Ct2 + Dt3 + Et4 + Ft5
                #P'(t) = B + 2Ct1 + 3Dt2 + 4Et3 + 5Ft4
                #P''(t) = 2C + 6Dt1 + 12Et2 + 20Ft3

                #P(0) = A
                #P'(0) = B
                #P''(0) = 2C

                #P(1) = A + B + C +D + E +F
                #P'(1) = B + 2C + 3D + 4E + 5F
                #P''(1) = 2C + 6D + 12E + 20F

                A = W[:,i]
                B = dW[:,i]
                C = 0.5*ddW[:,i]

                ## solve LE
                ## D + E +F = W[:,i+1]-A-B-C = P1
                ## 3D + 4E + 5F = dW[:,i+1]-B-2C = P2
                ## 6D + 12E + 20F = ddW[:,i+1]-2C = P3

                P1 = W[:,i+1]-A-B-C
                P2 = dW[:,i+1]-B-(2*C)
                P3 = ddW[:,i+1]-(2*C)

                ## solve Zleft*x = Zright
                Zleft = np.array([[1,1,1],[3,4,5],[6,12,20]])
                Zright = np.array([P1,P2,P3])

                x = np.linalg.solve(Zleft,Zright)
                D = x[0,:]
                E = x[1,:]
                F = x[2,:]

                ### DEBUGGING
                try:
                        def g(A,B,C,D,E,F,t):
                                t1 = t
                                t2 = t*t
                                t3 = t*t*t
                                t4 = t*t*t*t
                                t5 = t*t*t*t*t
                                return (A + t1*B + t2*C + t3*D + t4*E + t5*F)

                        def dg(A,B,C,D,E,F,t):
                                t1 = t
                                t2 = t*t
                                t3 = t*t*t
                                t4 = t*t*t*t
                                t5 = t*t*t*t*t
                                return (B + 2*C*t1 + 3*D*t2 + 4*E*t3 + 5*F*t4)

                        def ddg(A,B,C,D,E,F,t):
                                t1 = t
                                t2 = t*t
                                t3 = t*t*t
                                t4 = t*t*t*t
                                t5 = t*t*t*t*t
                                return (20*F*t3 + 6*D*t1 + 12*E*t2 + 2*C)

                        if not np.allclose(np.dot(Zleft, x), Zright):
                                print "6d polynomial not approximable"
                                sys.exit(0)
                        
                        West = g(A,B,C,D,E,F,duration)
                        dWest = dg(A,B,C,D,E,F,duration)
                        ddWest = ddg(A,B,C,D,E,F,duration)

                        assert( np.linalg.norm(West - W[:,i+1]) < 1e-10)
                        assert( np.linalg.norm(dWest - dW[:,i+1]) < 1e-10)
                        assert( np.linalg.norm(ddWest - ddW[:,i+1]) < 1e-10)

                except AssertionError as e:
                        
                        print "duration:",duration
                        print "Wnext:",W[:,i+1]
                        print "West :",West
                        print "dWnext:",dW[:,i+1]
                        print "dWest :",dWest
                        print "ddWnext:",ddW[:,i+1]
                        print "ddWest :",ddWest

                        raise

                for j in range(Ndim):
                        trajectorystring += "\n"
                        #trajectorystring += string.join([str(A[j]),str(B[j]),str(C[j])])
                        trajectorystring += string.join([str(A[j]),str(B[j]),str(C[j]),str(D[j]),str(E[j]),str(F[j])])

        return [trajectorystring, durationVector]

def customPlotTrajectory(traj0):
        dt = 0.001
        tvect = arange(0, traj0.duration + dt, dt)
        qvect = np.array([traj0.Eval(t) for t in tvect])
        qdvect = np.array([traj0.Evald(t) for t in tvect])
        qddvect = np.array([traj0.Evaldd(t) for t in tvect])

        lw = 3
        fs = 22
        lloc = 'lower right'
        
        subplot(3,1,1)
        print qvect.shape
        print tvect.shape
        plot(tvect, qvect[:,0], linewidth = lw, label = "$x$")
        plot(tvect, qvect[:,1], linewidth = lw, label = "$y$")
        plot(tvect, qvect[:,2], linewidth = lw, label = "$z$")
        plot(tvect, qvect[:,3], linewidth = lw, label = "$\\theta$")
        #plot(tvect, qdvect, f, linewidth=2)
        #plot(tvect, qddvect, f, linewidth=2)
        title('Position/Velocity/Acceleration Path', fontsize=fs)
        ylabel('Position', fontsize=fs)
        legend = plt.legend(loc=lloc, shadow=True, fontsize=fs)

        subplot(3,1,2)
        ylabel('Velocity', fontsize=fs)
        plot(tvect, qdvect[:,0], linewidth = lw, label = "$\dot x$")
        plot(tvect, qdvect[:,1], linewidth = lw, label = "$\dot y$")
        plot(tvect, qdvect[:,2], linewidth = lw, label = "$\dot z$")
        plot(tvect, qdvect[:,3], linewidth = lw, label = "$\dot \\theta$")
        legend = plt.legend(loc=lloc, shadow=True, fontsize=fs)

        subplot(3,1,3)
        ylabel('Acceleration', fontsize=fs)
        plot(tvect, qddvect[:,0], linewidth = lw, label = "$\ddot{x}$")
        plot(tvect, qddvect[:,1], linewidth = lw, label = "$\ddot{y}$")
        plot(tvect, qddvect[:,2], linewidth = lw, label = "$\ddot{z}$")
        plot(tvect, qddvect[:,3], linewidth = lw, label = "$\ddot{\\theta}$")
        xlabel('Time $t$',fontsize=fs)
        legend = plt.legend(loc=lloc, shadow=True, fontsize=fs)

        plt.show()

def computeReparametrizationTrajectory(F, R, amin, amax, W, dW, ddW):
        Ndim = W.shape[0]
        Nwaypoints = W.shape[1]

        [trajstr,durationVector] = GetTrajectoryString(W, dW, ddW)

        L = np.sum(durationVector)

        traj0 = Trajectory.PiecewisePolynomialTrajectory.FromString(trajstr)

        dendpoint = np.linalg.norm(traj0.Eval(L)-W[:,-1])

        if dendpoint > 1e-10:
                print L
                print "###############"
                print "FINAL POINT on piecewise C^2 traj:",traj0.Eval(L)
                print "FINAL WAYPOINT                   :",W[:,-1]
                print "###############"
                sys.exit(1)

        ### compute a,b,c
        q = np.zeros((Ndim,Nwaypoints))
        qs = np.zeros((Ndim,Nwaypoints))
        qss = np.zeros((Ndim,Nwaypoints))
        for i in range(0,Nwaypoints):
                duration = np.sum(durationVector[0:i])
                q[:,i] = traj0.Eval(duration)
                qs[:,i] = traj0.Evald(duration)
                qss[:,i] = traj0.Evaldd(duration)

        I = np.identity(Ndim)
        G = np.vstack((I,-I))

        a = np.zeros((Nwaypoints, 2*Ndim))
        b = np.zeros((Nwaypoints, 2*Ndim))
        c = np.zeros((Nwaypoints, 2*Ndim))

        for i in range(0,Nwaypoints):
                Rmax = np.maximum(np.dot(R[:,:,i],amax),np.dot(R[:,:,i],amin))
                Rmin = np.minimum(np.dot(R[:,:,i],amax),np.dot(R[:,:,i],amin))
                H1 = F[:,i] - Rmax
                H2 = -F[:,i] + Rmin
                for j in range(Ndim):
                        #print "qvol[",j,"]=",np.linalg.norm(-H1[j]-H2[j])
                        if H2[j] > -H1[j]:
                                print H2[j],"<= q[",j,"]<=",-H1[j]
                                sys.exit(1)

                c[i,:] = np.hstack((H1,H2)).flatten()

        for i in range(0,Nwaypoints):
                a[i,:] = np.dot(G,qs[:,i]).flatten()
                b[i,:] = np.dot(G,qss[:,i]).flatten()

        vmax = 1000*np.ones(Ndim)
        durationQ = traj0.duration/Nwaypoints
        #durationQ = 1e-1
        #topp_inst = TOPP.QuadraticConstraints(traj0, durationVector[0], vmax, list(a), list(b), list(c))
        topp_inst = TOPP.QuadraticConstraints(traj0, durationQ, vmax, list(a), list(b), list(c))
        x = topp_inst.solver

        customPlotTrajectory(traj0)
        #x.integrationtimestep = 0.001
        #x.reparamtimestep = 0.001
        #x.extrareps = 10
        qproblematic= np.array([[-1.04377849, -1.02977873, -1.01911143, -1.01499959, -1.01643708,
        -1.02325269, -1.03688057, -1.05309118, -1.07583686, -1.10578633],
       [ 0.29385664,  0.30651985,  0.32203638,  0.33676218,  0.35198637,
         0.36711786,  0.38396792,  0.39809829,  0.41358129,  0.43002112]])


        try:
                print "W=",repr(W[0:2,:])
                print "q=",repr(q[0:2,:])
                print "dW=",repr(dW[0:2,:])
                print "qs=",repr(qs[0:2,:])
                print "ddW=",repr(ddW[0:2,:])
                print "qss=",repr(qss[0:2,:])
                print "a=",repr(np.around(a,decimals=2))
                print "b=",repr(np.around(b,decimals=2))
                print "c=",repr(np.around(c,decimals=2))
                print "d=",repr(durationVector)
                print durationQ*Nwaypoints,"(",durationQ,") VS. ",traj0.duration
                print trajstr
                if np.linalg.norm(q[0,:]-qproblematic[0,:]) < 0.001:
                        print traj0.duration
                        topp_inst.PlotAlphaBeta()
                        print "PROBLEMATIC Q found"
                ret = topp_inst.solver.RunComputeProfiles(0,0)
                print "DONE"

        except Exception as e:
                print "TOPP EXCEPTION: ",e
                print W
                print duration
                print durationVector
                print traj0.duration
                sys.exit(0)
                #return -1

        if ret == 1:
                return topp_inst
        else:
                return None

def getSpeedProfileRManifold( F, R, amin, amax, W, dW, ddW, ploting=False):
        topp_inst = computeReparametrizationTrajectory(F, R, amin, amax, W, dW, ddW)

        if topp_inst is not None:
                x = topp_inst.solver
                x.ReparameterizeTrajectory()

                [semin,semax] = topp_inst.AVP(0, 0)
                #ion()
                x.WriteResultTrajectory()

                traj1 = Trajectory.PiecewisePolynomialTrajectory.FromString(x.restrajectorystring)

                print "Trajectory duration before TOPP: ", traj0.duration
                print "Trajectory duration after TOPP: ", traj1.duration
                print "Velocity profile at end point:",semin,semax

                if ploting:
                        print "PLOTTING"
                        customPlotTrajectory(traj1)

                t = 0
                tstep = traj1.duration/Nwaypoints
                P = []
                while t < traj1.duration:
                        P.append(np.linalg.norm(traj1.Evald(t)))
                        t = t + tstep
                #return np.array(P)
                return traj1
        return None




def testMVCgetControlMatrix(W):
        Ndim = W.shape[0]
        Nwaypoints = W.shape[1]

        assert(Ndim == 3)
        R = np.zeros((Ndim,2,Nwaypoints))
        for i in range(0,Nwaypoints):
                t = W[2,i]
                R[0,:,i] = np.array((cos(t),0.0))
                R[1,:,i] = np.array((sin(t),0.0))
                R[2,:,i] = np.array((0.0,1.0))
        return R

from scipy.interpolate import interp1d,splev,splrep,splprep
from scipy.misc import derivative

def testMVCgetDerivWpt(W):
        Ndim = W.shape[0]
        Nwaypoints = W.shape[1]
        dW = np.zeros((W.shape))
        ddW = np.zeros((W.shape))

        traj,tmp = splprep(W,k=5,s=0.01)
        #L = getLengthWpt(W)
        d = 0.0
        for i in range(0,Nwaypoints-1):
                dW[:,i] = splev(d,traj,der=1)
                ddW[:,i] = splev(d,traj,der=2)
                #dW[:,i] = dW[:,i]/np.linalg.norm(dW[:,i])

                ds = np.linalg.norm(W[:,i+1]-W[:,i])
                dv = np.linalg.norm(dW[:,i])
                dt = ds/dv
                #ddW[:,i] = ddW[:,i]/np.linalg.norm(ddW[:,i])
                print d
                d = d + dt

        dW[:,Nwaypoints-1] = splev(d,traj,der=1)
        ddW[:,Nwaypoints-1] = splev(d,traj,der=2)

        return [dW,ddW]

if __name__ == '__main__':
        W = np.array((
                        (0.0,0.1,0.2,0.3,0.4,0.5),
                        (0.0,0.0,0.0,0.0,0.0,0.0),
                        (0.0,0.0,0.0,0.0,0.0,0.0)
                ))
        [dW,ddW] = testMVCgetDerivWpt(W)
        print W
        print dW
        print ddW
        print "######################"
        amin = np.array((-2,-5))
        amax = np.array((3,5))

        R = testMVCgetControlMatrix(W)
        print R
        F = np.zeros((W.shape))
        getSpeedProfileRManifold(F, R, amin, amax, W, dW, ddW)

