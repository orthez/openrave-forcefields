import abc
from deformation_module import *

class DeformationModuleCounterWrench(DeformationModule):

        def get_gradient(self, lambda_coeff):

                traj = self.DeformInfo['traj']
                env = self.DeformInfo['env']
                eta = self.DeformInfo['eta']
                Wori = self.DeformInfo['Wori']
                dWori = self.DeformInfo['dWori']
                Ndim = self.DeformInfo['Ndim']
                Nwaypoints = self.DeformInfo['Nwaypoints']
                F = self.DeformInfo['F']
                FN = self.DeformInfo['FN']

                dUtmp = np.zeros((Ndim,Nwaypoints))
                for i in range(0,Nwaypoints):
                        A = self.SmoothVector(traj,i,Wori)
                        dUtmp[:,i] += np.dot(A,( -lambda_coeff * FN.T))
                return dUtmp

        def get_name(self):
                return "counter-wrench"
