#!/usr/bin/env python
import time
import scipy
import sys
import numpy as np
import openravepy
from openravepy import *
from math import *
from environment_force_humanoid import *
from cbirrtpy import *

from deformation_naive import *
from deformation_potentials import *
from deformation_stretchpull import *
from trajectory_bspline import *
import numpy as np
from motion_planner_geometrical import MotionPlannerGeometrical
from motion_planner_kinodynamic import MotionPlannerKinodynamic
from util_humanoid import *
#import statsmodels.api as sm

def waitrobot(robot):
    """busy wait for robot completion"""
    while not robot.GetController().IsDone():
        time.sleep(0.1)

if __name__ == "__main__":

        env = EnvironmentHumanoid()
        env.DisplayForces()
        time.sleep(0.5)
        robot = env.GetRobot()

        #######################################################################
        ### READ GEOMETRICAL PATH FROM XML
        #######################################################################
        tname = 'misc/trajectory.xml'

        fhandle = open(tname, 'r')
        trajdata = fhandle.read()
        fhandle.close()
        rave_path = RaveCreateTrajectory(env.env,'').deserialize(trajdata)

        rave.planningutils.RetimeActiveDOFTrajectory(rave_path,robot)
        rave.planningutils.SmoothActiveDOFTrajectory(rave_path,robot)

        M = rave_path.GetNumWaypoints()
        N = len(robot.GetActiveDOFValues())

        [q_original, COM_original] = COM_from_path( rave_path, robot, env)

        #######################################################################
        ### COMPUTE NEW COM
        #######################################################################

        COM_linear = COM_interpolate(COM_original[:,0],COM_original[:,-1],M)

        T = arange(0,M)
        C = float(M/5)

        scale=0.0

        while scale<1.0:

                COM_offset = np.zeros((3,M))
                COM_offset += COM_linear
                COM_offset[0,:]+=0.00*exp(-(T-M/2)**2/(2*C*C))
                COM_offset[1,:]+=-scale*exp(-(T-M/2)**2/(2*C*C))
                COM_offset[2,:]+=-scale*0.1*exp(-(T-M/2)**2/(2*C*C))

                env.DrawAxes()

                tmp_handle=[]

                [COM_zig_zag, footpos, dfootpos] = COM_compute_zig_zag_motion(COM_offset, env)

                with env.env:
                        h=env.env.drawlinestrip(points=COM_offset.T,linewidth=6,colors=np.array((0,1,0)))
                        tmp_handle.append(h)
                        h=env.env.drawlinestrip(points=COM_zig_zag.T,linewidth=6,colors=np.array((0,1,0)))
                        tmp_handle.append(h)

                scale+=0.05
                time.sleep(0.1)

        #[q_gik, COM_gik] = GIK_from_COM_and_FOOTPOS( COM_zig_zag, footpos, dfootpos, robot, env, recompute=True)
        [q_gik, COM_gik] = GIK_from_COM_and_FOOTPOS( COM_zig_zag, footpos, dfootpos, robot, env)
        #[q_gik, COM_gik] = GIK_from_COM( COM_zig_zag, q_original, robot, env, recompute=True)

        #######################################################################
        ### RECOMPUTE GIK FROM NEW COM
        #######################################################################

        #q_gik_fname = 'tmp/q_gik.numpy'
        #COM_gik_fname = 'tmp/COM_gik.numpy'
        #q_gik = np.load(q_gik_fname+'.npy')
        #COM_gik = np.load(COM_gik_fname+'.npy')

        tmp_handle=[]
        with env.env:
                #h=env.env.drawlinestrip(points=COM_original.T,linewidth=6,colors=np.array((1,0,0)))
                #tmp_handle.append(h)
                h=env.env.drawlinestrip(points=COM_gik.T,linewidth=8,colors=np.array((0,1,0)))
                tmp_handle.append(h)
                h=env.env.drawlinestrip(points=COM_offset.T,linewidth=8,colors=np.array((0.8,0,0.8,0.3)))
                tmp_handle.append(h)
                robot.SetActiveDOFValues(q_gik[:,0])

        #time.sleep(0.5)
        #visualize_configurations(q_original, robot, env)
        #sys.exit(0)
        ###############################################################################
        ##### CREATE A NEW RAVE TRAJ FROM NEW CONFIGURATIONS AND RETIME
        ###############################################################################
        M = COM_gik.shape[1]
        print "WAYPOINTS: ",M
        traj = RaveCreateTrajectory(env.env,'')
        traj.Init(robot.GetActiveConfigurationSpecification())
        i=0
        while i < M:
                traj.Insert(i,q_gik[:,i])
                i=i+1

        Nl = len(robot.GetLinks())

        ##forcetorquemap = np.zeros((Nl,6))
        #forcetorquemap = {x: np.zeros(6) for x in np.arange(Nl)}
        ### create forcetorquemap dictionary
        #link = robot.GetLink('torso')
        #iTorso = link.GetIndex()
        #Ftorso = np.array((0,0.0,0,0,0,0))
        #forcetorquemap[iTorso]=Ftorso

        #controller = RaveCreateController(env.env,'odevelocity')
        #robot.SetController(controller,range(robot.GetDOF()),0)
        with env.env:
                rave.planningutils.SmoothActiveDOFTrajectory(traj,robot)
                rave.planningutils.RetimeActiveDOFTrajectory(traj,robot,hastimestamps=False,maxvelmult=0.75)

        robot.GetController().SetPath(traj)
        robot.WaitForController(0)
        robot.GetController().Reset()
        raw_input('Enter any key to quit. ')
