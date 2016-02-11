from environment_force import *
import openravepy

class EnvironmentTheStream(ForceEnvironment):
        def __init__(self):
                ForceEnvironment.__init__(self)
                xmlenv='environments/the_stream.env.xml'
                xmlrobot='robots/pointrobot.robot.xml'
                self.setrobotenv(xmlrobot,xmlenv)

        def GetCells(self):
                C = self.GetCellsAll()
                self.cells = C[0:3]
                return self.cells

        def GetForces(self):
                ##
                self.forces=[]
                self.forces.append(numpy.array((0.0,0.0,0.0)))
                self.forces.append(numpy.array((0.0,-0.5,0.0)))
                self.forces.append(numpy.array((0.0,0.0,0.0)))
                return self.forces

        def RobotGetInitialPosition(self):
                return [-4.0,-2.5,0.15,pi,0,0,0,0]

        def RobotGetGoalPosition(self):
                return [4.0,1.7,0.15,0,0,0,0,0]


if __name__ == "__main__":
        env = EnvironmentTheStream()