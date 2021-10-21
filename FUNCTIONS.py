# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 08:44:02 2020

@author: vinay
"""
import numpy as np
import scipy.linalg as LA
np.set_printoptions(precision=3, suppress=True)
 
    
    
def obsv(L, D, A, B, C, U, YN, x_1hat, x_2hat, t1_hat, t2_hat, k):
    
    d1 = D[0]
    d2 = D[1]
    
    b1 = B[:,0]
    b2 = B[:,1]
    
    u1 = U[0]
    u2 = U[1]
    
    #errors and norms
    e_y =  C@x_1hat - YN
    e_y2 = C@x_2hat - YN
    #norms
    N1 = LA.norm(e_y)**2
    N2 = LA.norm(e_y2)**2
    
    #for first fault
    
    x_1hat = A @ x_1hat - L @ (e_y) + b2 * u2 + b1 * t1_hat
    
    t1_hat += -2.0*(e_y.T @ d1.T) 
    
    #for second fault
    
    x_2hat = A @ x_2hat - L @ (e_y2) + b1 * u1 + b2 * t2_hat
    
    t2_hat += -2.0*(e_y2.T @ d2.T)

    
    return x_1hat, x_2hat, t1_hat, t2_hat, N1, N2




    