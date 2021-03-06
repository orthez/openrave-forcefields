from environment_force import *
import numpy as np
import math
import openravepy as rave

class AttributePassthrough(object):
    def __init__(self, getter, getAll):
        self.getter = getter
        self.getAll = getAll

    def __getattr__(self, item):
        return self.getter(item)

    def __getitem__(self, item):
        return self.getter(item)

    def __iter__(self):
        return iter(self.getAll())

class EnvironmentHumanoid(ForceEnvironment):
        surrender_pos = []
        def SetTransformRobot(self, Cll, Crl, Cla, Cra):
                #self.manip.l_arm.SetLocalToolDirection(np.array([1, 0, 0]))
                #self.manip.l_arm.SetLocalToolTransform(np.array([
                #    [-1,  0, 0, -0.036],
                #    [ 0, -1, 0, 0],
                #    [ 0,  0, 1, 0],
                #    [ 0,  0, 0, 1]])
                #)

                #self.manip.r_arm.SetLocalToolDirection(np.array([1, 0, 0]))
                with self.env:
                        if Cll is not None:
                                self.manip.l_leg.SetLocalToolTransform(Cll)
                        if Crl is not None:
                                self.manip.r_leg.SetLocalToolTransform(Crl)
                        if Cla is not None:
                                self.manip.l_arm.SetLocalToolTransform(Cla)
                        if Cra is not None:
                                self.manip.r_arm.SetLocalToolTransform(Cra)
                #self.manip.l_leg.SetLocalToolDirection(np.array([0, 0, -1]))
                #self.manip.r_leg.SetLocalToolDirection(np.array([0, 0, -1]))

        def __init__(self, xmlenv = 'environments/plane.env.xml', free_flyer_offset=np.array((0,0,0))):
                ForceEnvironment.__init__(self)
                urdf = 'robots/escher/escher_v2.kinbody.urdf'
                srdf = 'robots/escher/escher.robot.srdf'
                self.env_xml = xmlenv
                with self.env:
                        self.robot_urdf = urdf
                        self.robot_srdf = srdf

                        module = rave.RaveCreateModule(self.env, 'urdf')
                        self.robot_name = module.SendCommand('load {} {}'.format(urdf, srdf))
                        self.robot = self.env.GetRobot(self.robot_name)

                        self.manip = AttributePassthrough(self.robot.GetManipulator, self.robot.GetManipulators)
                        self.manip.l_arm.SetLocalToolDirection(np.array([1, 0, 0]))
                        self.manip.l_arm.SetLocalToolTransform(np.array([
                            [-1,  0, 0, -0.036],
                            [ 0, -1, 0, 0],
                            [ 0,  0, 1, 0],
                            [ 0,  0, 0, 1]])
                        )

                        self.manip.r_arm.SetLocalToolDirection(np.array([1, 0, 0]))
                        self.manip.r_arm.SetLocalToolTransform(np.array([
                            [ 1,  0, 0, 0.036],
                            [ 0,  1, 0, 0],
                            [ 0,  0, 1, 0],
                            [ 0,  0, 0, 1]])
                        )

                        self.manip.l_leg.SetLocalToolDirection(np.array([0, 0, -1]))
                        self.manip.r_leg.SetLocalToolDirection(np.array([0, 0, -1]))

                        l_arm_indices = self.robot.GetManipulator('l_arm').GetArmIndices()
                        r_arm_indices = self.robot.GetManipulator('r_arm').GetArmIndices()
                        l_leg_indices = self.robot.GetManipulator('l_leg').GetArmIndices()
                        r_leg_indices = self.robot.GetManipulator('r_leg').GetArmIndices()
                        additional_active_DOFs = ['x_prismatic_joint','y_prismatic_joint',
                                                'z_prismatic_joint','roll_revolute_joint',
                                                'pitch_revolute_joint' ,'yaw_revolute_joint',
                                                'waist_yaw']
   
                        additional_active_DOF_indices = [None]*len(additional_active_DOFs)
                        for index,j in enumerate(additional_active_DOFs):
                                additional_active_DOF_indices[index] = self.robot.GetJoint(j).GetDOFIndex()
    
                        robot_z = 0.9
                        whole_body_indices = np.concatenate((l_arm_indices, r_arm_indices, l_leg_indices, r_leg_indices, additional_active_DOF_indices),axis=0)

                        self.robot.SetActiveDOFs(whole_body_indices)
                        T = np.array([[1,0,0,-0.5],[0,1,0,0],[0,0,1,robot_z],[0,0,0,1]])

                        #T[0:3,3] += free_flyer_offset
                        self.robot.SetTransform(T)

                        ### surrender posture
                        DOFValues = self.robot.GetDOFValues()
                        DOFValues[6] = math.pi/4
                        DOFValues[19] = math.pi/4
                        DOFValues[24] = -math.pi/4
                        DOFValues[37] = -math.pi/4
                        #DOFValues[6] = math.pi/2
                        #DOFValues[19] = math.pi/2
                        #DOFValues[24] = -math.pi/2
                        #DOFValues[37] = -math.pi/2
                        self.robot.SetDOFValues(DOFValues)

                        self.surrender_pos = self.robot.GetActiveDOFValues()
                        #self.surrender_pos[0:3] += free_flyer_offset

                        dof = self.robot.GetDOF()
                        v = np.ones(dof)
                        self.robot.SetDOFVelocityLimits(1 * v)
                        #self.rave.SetDOFTorqueLimits(tunings.torque_limits)

                        OriginalDOFValues = self.robot.GetDOFValues()
                        self.env.Load(self.env_xml)


        def EnforceLimits(self, q, qlimL, qlimU):
                ### EnforceLimits is only checking for rounding errors
                ### function returns error if joint limits are too far outside
                ### (specified by epsilon) => this case means that there is some
                ### general problem with another functions which provides the q
                epsilon=1e-5
                for i in range(0,q.shape[0]):
                        #print "DOF",i,":",qlimL[i],"<=",q[i],"<=",qlimU[i]
                       if ( q[i] <= qlimL[i]):
                               q[i] = qlimL[i]+epsilon
                               if q[i] < (qlimL[i]-epsilon):
                                       print "!q[i]=",q[i]," (<",qlimL[i],") epsilon neighborhood:",epsilon
                                       print "ERROR: joint value is too far outside joint limits"
                                       sys.exit(1)
                       if ( q[i] >= qlimU[i] ):
                               q[i] = qlimU[i]-epsilon
                               if q[i] > (qlimU[i]+epsilon):
                                       print "!q[i]=",q[i]," (>",qlimU[i],") epsilon neighborhood:",epsilon
                                       print "ERROR: joint value is too far outside joint limits"
                                       sys.exit(1)
                return q

        def GetCells(self):
                C = self.GetCellsAll()
                self.cells = C[0:2]
                return self.cells

        def GetForces(self):
                ##
                self.forces = np.array((0.0,0.0,0.0))
                self.forces = np.vstack([self.forces,(0.0,2.0,0.0)])
                return self.forces

        def RobotGetInitialPosition(self):
                return [-2.5,0.0,0.1,-pi,0,0,0,0]

        def RobotGetGoalPosition(self):
                return [-4.5,-0.0,0.1,-pi,0,0,0,0]

        def GetRobot(self):
                with self.env:
                        return self.robot

        def DisplayForces(self):
                if self.forces is None:
                        self.forces = self.GetForces()
                if self.cells is None:
                        self.cells = self.GetCells()

                #with self.env:
                assert(len(self.forces)==len(self.cells))

                self.ResetForceHandles()
                for i in range(0,len(self.cells)):
                        C = self.cells[i]
                        G1 = C.GetGeometries()[0]
                        B = G1.GetBoxExtents()
                        T = G1.GetTransform()
                        T[2,3] = 1.0
                        B[2] = 1.0
                        ######
                        h = self.DrawBoxMesh(T,B)
                        self.AddForceHandles([h])
                        ######
                        F = self.forces[i]
                        h = self.DrawForceArrowsInBox(T, B, F)
                        self.AddForceHandles(h)

        def AddForceAtTorso(self, robot, F):
                #link = robot.GetLink('l_foot')
                link = robot.GetLink('torso')
                P = link.GetLocalCOM()
                print "found TORSO"
                link.SetForce(F,P,True)

                self.env.GetPhysicsEngine().SetBodyForce(link,F,P,True)
                ### color in the geometries
                for geom in link.GetGeometries():
                        c = np.array((1,0,0))
                        geom.SetAmbientColor(c) 
                        geom.SetDiffuseColor(c) 

        def AddForcesToRobot(self, robot):
                for link in robot.GetLinks():
                        print "######################"
                        for geom in link.GetGeometries():
                                print geom
                                robotIsInCollision = env.env.CheckCollision(link, outercells[i]) 

                        for i in range(0,len(self.cells)):
                                C = self.cells[i]
                                G1 = C.GetGeometries()[0]
                                B = G1.GetBoxExtents()
                                T = G1.GetTransform()
                                T[2,3] = 1.0
                                B[2] = 1.0
                                ######
                        env.AddForcesToRobot(robot)
                        P = link.GetLocalCOM()
                        link.SetForce(F,P,True)


if __name__ == "__main__":
        env = EnvironmentHumanoid()
