#start!/usr/bin/env python
import time
import scipy
import sys
import numpy as np
import openravepy
from openravepy import *
from math import *
from environment_force_humanoid import *
from environment_force_humanoid_contact_world import *
from cbirrtpy import *

from deformation_naive import *
from deformation_potentials import *
from deformation_stretchpull import *
from trajectory_bspline import *
import numpy as np
from motion_planner_geometrical import MotionPlannerGeometrical
from motion_planner_kinodynamic import MotionPlannerKinodynamic
from util_humanoid import *
from gik_interface import *

#sys.path.append(os.environ["MPP_PATH"]+"mpp-robot/mpp")
#sys.path.append(os.environ["OPENRAVE_WPI_PATH"]+"ros_msgs")
#from SurfaceMeshes import *


def waitrobot(robot):
    """busy wait for robot completion"""
    while not robot.GetController().IsDone():
        time.sleep(0.1)

if __name__ == "__main__":

        env = EnvironmentHumanoidContactWorld()
        env.DrawAxes()
        robot = env.GetRobot()
        surfaces = env.GetSurfaces()
        time.sleep(0.5)

        print surfaces.shape
        for i in arange(surfaces.shape[0]):
                et = surfaces[i,4,0]
                eo = surfaces[i,5,0]
                print "Surface",i,
                if et <= 0.01:
                        print "no extension",
                if eo <= 0.01:
                        print "no extension",
                print

        from surface_module import *
        M = surfaces.shape[0]

        S = SurfaceModule(surfaces)
        robot = env.GetRobot()

        com = robot.GetCenterOfMass()

        left_leg_tf = robot.GetManipulator('l_leg').GetTransform()
        right_leg_tf = robot.GetManipulator('r_leg').GetTransform()
        left_arm_tf = robot.GetManipulator('l_arm').GetTransform()
        right_arm_tf = robot.GetManipulator('r_arm').GetTransform()

        foot_surface = 4
        left_hand_surface = 13
        right_hand_surface = 26

        left_leg_tf = S.GetNearestContactTransform(env, 
                        left_leg_tf, 
                        foot_surface)
        right_leg_tf = S.GetNearestContactTransform(env, 
                        right_leg_tf, 
                        foot_surface)
        left_arm_tf = S.GetNearestContactTransform(env, 
                        left_arm_tf,
                        left_hand_surface)
        right_arm_tf = S.GetNearestContactTransform(env, 
                        right_arm_tf,
                        right_hand_surface)

        env.DrawFootContactPatchFromTransform(left_leg_tf)
        env.DrawFootContactPatchFromTransform(right_leg_tf)
        env.DrawFootContactPatchFromTransform(left_arm_tf)
        env.DrawFootContactPatchFromTransform(right_arm_tf)

        #S.SampleSurface(100,right_hand_surface,env)
        #S.SampleSurface(100,left_hand_surface,env)
        #S.SampleSurface(100,foot_surface,env)

        with env.env:
                #env.env.GetPhysicsEngine().SetGravity([0,0,-9.81])
                robot.GetLinks()[0].SetStatic(True)
                gik = GIKInterface(env)
                q = gik.fromContactTransform(robot, left_leg_tf, right_leg_tf, left_arm_tf, None)
                #q = gik.fromContactTransform(robot, left_leg_tf, right_leg_tf, left_arm_tf, right_arm_tf)
                #q = gik.fromContactTransform(robot, left_leg_tf, right_leg_tf, None, None)
                #q = gik.fromContactTransform(robot, left_leg_tf, right_leg_tf, None, None)

        #robot.WaitForController(0)
        #time.sleep(20)

