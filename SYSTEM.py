# -*- coding: utf-8 -*-
"""
Created on Mon May 18 08:28:30 2020

@author: vin
"""

#to import
import numpy as np
np.set_printoptions(precision=3,suppress=True)
import control as ct

class LinearDisturbedSystem:
    #initialize method
    def __init__(self,A,B,C,X,U,Y,Bd,gm):
        self.A = A
        self.B = B
        self.C = C
        self.XP = X # states (perfect)
        self.U = U # inputs
        self.YP = Y # outputs (perfect)
        self.Bd = Bd #disturbance matrix for states
        self.gm = gm

    #function to give you dimensions (n,m,p)
    def dims(self):
        B_size = np.shape(self.B)
        n_s = B_size[0] #no. of states
        n_i = B_size[1] #no. of inputs
        C_size = np.shape(self.C)
        n_o = C_size[0] #no. of outputs
        r = n_i
        n_d = 2
        return n_s,n_i,n_o,r,n_d

    #simulation function (WITH NOISE - assume nd = p)
    def sim(self,n_s,n_i,n_d,n_o):
        
        #Bf = fault matrix
        self.Bf = sys_1.B @ (np.eye(n_i)+np.diag(self.gm))
        
        #noise vector w (process) and v (measurement)
        w = np.random.normal(0,0.003,3)
        v = np.random.normal(0,0.0045,n_o)
        
        #simulation of perfect states
        self.XP = self.A @ np.reshape(self.XP,(n_s,1)) + self.Bf @ np.reshape(self.U,(n_i,1))  
        self.YP = self.C @ np.reshape(self.XP,(n_s,1))
        
        #now, add noise to these states
        self.XN = self.XP + self.Bd @ np.reshape(w,(3,1)) 
        #now from the noisy states, get the noisy outputs
        self.YN = self.C @ np.reshape(self.XN,(n_s,1)) + np.reshape(v,(n_o,1))        

    

##RELEVANT PARAMETERS FOR SYSTEM--------------------------------------------------#
        
#The Linear Model (Continuous) and the Discretization Time

A_c = np.array([[-2.00 , 0.00 , 0.00], \
                [0.00 , -2.00 , 0.00], \
                [0.00 , 0.00 , -2.00]])
    
B_c = np.array([[1.0 , 1.0],\
                [0.0 , 1.0],\
                [1.0 , 0.0]])

C_c = B_c.T


D_c = np.zeros((np.shape(C_c)[0],np.shape(B_c)[1]))

#sampling time
dT = 0.01

sys = ct.ss(A_c,B_c,C_c,D_c)

#The Linear Model (Discrete - ZOH sample) - This is your discrete system to use
LIN = sys.sample(dT,method='zoh')
(A_sys,B_sys,C_sys,D_sys) = ct.ssdata(LIN)

#Disturbance parameters
Bd = np.eye(3)

#Initial delta_X (states)
X_i = np.array([0.3,0.3,0.3])

#Initial Inputs 
U_o = np.array([0.0,0.0])

#Initial Outputs (delta_Y) (hard-code this)
Y_o = C_sys @ X_i

#RELEVANT PARAMETERS FOR FTC--------------------------------------------------#
    
#fault-vector (-1<gm[i]<0) - zero initially
gm = np.array([0.00,0.00])    

#DEFINE YOUR SYSTEM
sys_1 = LinearDisturbedSystem(A_sys,B_sys,C_sys,X_i,U_o,Y_o,Bd,gm)



    
        