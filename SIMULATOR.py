
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 12:30:24 2020

@author: vinay
"""
import numpy as np
np.set_printoptions(precision=4,suppress=True)
from SYSTEM import sys_1, dT
from FUNCTIONS import obsv
from FUNCTIONS3 import PLOTTING
import scipy.linalg as LA
#------------------------------------------------------------------------------------------#

#capture number of states, inputs, outputs, setpoints
DIMS = sys_1.dims()
n = DIMS[0]
m = DIMS[1]
p = DIMS[2]
r = DIMS[3]
nd = DIMS[4]

#test sim
k = 0
time = 25.0
k_f = int(time/dT)

#create empty output matrices
STATES = np.zeros([2*n,k_f])
OUTPUTS = np.zeros([p,k_f])
INPUTS = np.zeros([2*m,k_f])
FAULT_VEC = np.zeros([3*m,k_f])

#initial estimate guesses (delta x - states, and fault parameters)
x_1hat = np.ones([n,1])
x_2hat = np.zeros([n,1])
t1_hat = 0.0
t2_hat = 0.0

#bank of observer parameters
I_n = np.eye(n)
L = 0.15*sys_1.C.T
Q = 4*I_n + sys_1.C.T @ sys_1.C
P = 1.0*I_n
D = np.array([[1,0],[0,1]])

#estimate of effectiveness factors
gm_hat = np.array([0.0,0.0])
tol = 1.0e-6

#simulation loop--------------------------------------------------------------#

while (k<int(k_f)):
  
    #simulate 1 time step - obtain everything 
    SIM = sys_1.sim(n,m,nd,p)
    
    #noisy outputs go into observer
    YN = sys_1.YN
    
    #Call the observer-------------------------------------------------------#
    x_1hat, x_2hat, t1_hat, t2_hat, N1, N2 = obsv(L, D, sys_1.A, sys_1.B, sys_1.C, sys_1.U, \
                                             YN, x_1hat, x_2hat, t1_hat, t2_hat ,k)

    #proceed with estimates of noise, fault parameters---------#
    if(k>=700):
        sys_1.gm[0] = -0.50
        sys_1.gm[1] = -0.70
        
    #a CONSTANT input
    sys_1.U[0] = 2.0
    sys_1.U[1] = 2.0
    
    U_efct = np.array([np.asscalar(t1_hat), np.asscalar(t2_hat)]) #effective input
    #calculate the fault parameter (gm) from here.
    
    #fault parameters gm_1 and gm_2, watch out division by 0
    gm_hat[0] = (U_efct[0]-sys_1.U[0]) / (sys_1.U[0] + tol)
    if (gm_hat[0] <= -1.0) or (gm_hat[0]>=0.0):
        gm_hat[0] = 0.0
        
    gm_hat[1] = (U_efct[1]-sys_1.U[1]) / (sys_1.U[1] + tol)
    if (gm_hat[1] <= -1.0) or (gm_hat[1]>=0.0):
        gm_hat[1] = 0.0

    
    #norms
    FAULT_VEC[0,k] = N1 #norm 1
    FAULT_VEC[1,k] = N2 #norm 2
    
    #log all states (perfect vs estimated), outputs, fault parameter vector
    for i in range (0,n):
        #states
        STATES[i,k] = sys_1.XN[i]
        STATES[i+n,k] = x_1hat[i]
    for j in range (0,p):
        #outputs (which go to sensor)
        OUTPUTS[j,k] = sys_1.YN[j]
    for v in range (0,m):
        #inputs - actual and incremental
        INPUTS[v,k] = sys_1.U[v]
        INPUTS[v+m,k] = 0.0    
    for tn in range (0,m):
        FAULT_VEC[tn+m,k] = U_efct[tn]
        FAULT_VEC[tn+2*m,k] = gm_hat[tn]
    #increment k
    k+=1

#--------------------end while------------------------------------------------------#


#Plot all the results (make sure to multiply by N^-1, to get setpoint)
#i.e. the uncompensated setpoint
PLOTTING(STATES,OUTPUTS,INPUTS,FAULT_VEC,dT,k_f)
