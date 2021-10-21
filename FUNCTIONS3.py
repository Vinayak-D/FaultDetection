# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 10:52:04 2020

@author: vinay
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
plt.rcParams['font.size']=14

#The function that plots everything

def PLOTTING(STATES,OUTPUTS,INPUTS,FAULT_VEC,dT,k_f):
    
    t = np.linspace(0,k_f*dT,k_f)

    plt.figure("STATES") #---------------------------------------------------#
    
    plt.subplot(1,3,1)
    plt.plot(t,STATES[0,:],color='k',label='True')
    plt.plot(t,STATES[3,:],color='b',linestyle='dashdot',label='Estimated')
    plt.xlabel('Time (s)')
    plt.ylabel('STATE $X_1$')
    plt.tight_layout() 
 
    plt.subplot(1,3,2)
    plt.plot(t,STATES[1,:],color='k',label='True')
    plt.plot(t,STATES[4,:],color='b',linestyle='dashdot',label='Estimated')
    plt.xlabel('Time (s)')
    plt.ylabel('STATE $X_2$')
    plt.tight_layout()
    
    plt.subplot(1,3,3)
    plt.plot(t,STATES[2,:],color='k',label='True')
    plt.plot(t,STATES[5,:],color='b',linestyle='dashdot',label='Estimated')
    plt.xlabel('Time (s)')
    plt.ylabel('STATE $X_3$')
    plt.tight_layout()
    
    
    plt.figure("INPUTS") #---------------------------------------------------#
    
    plt.subplot(1,2,1)
    plt.plot(t,INPUTS[0,:],color='b')
    plt.xlabel('Time (s)')
    plt.ylabel('INPUT CMD $U_1$')
    plt.tight_layout()

    plt.subplot(1,2,2)
    plt.plot(t,INPUTS[1,:],color='b')
    plt.xlabel('Time (s)')
    plt.ylabel('INPUT CMD $U_2$')
    plt.tight_layout()
    
    plt.figure("EFFECTIVE INPUTS/NORMS, OBTAIN FAULT PARAMETERS FROM HERE") #-----------------------------------------#
    
    plt.subplot(1,2,1)
    plt.plot(t,FAULT_VEC[2,:],color='r',linestyle='dashdot',label='Input Effective')
    plt.xlabel('Time (s)')
    plt.ylabel(r'EFFECTIVE - $\theta_1\ (U_1)$')
    plt.tight_layout()

    plt.subplot(1,2,2)
    plt.plot(t,FAULT_VEC[3,:],color='r',linestyle='dashdot',label='Input Effective')
    plt.xlabel('Time (s)')
    plt.ylabel(r'EFFECTIVE - $\theta_2\ (U_2)$')
    plt.tight_layout()
    
    plt.figure("ESTIMATION OF LOSS OF EFFECTIVENESS (FAULT PARAMETER)")
    
    plt.subplot(1,2,1)
    plt.plot(t,FAULT_VEC[4,:],color='k',label=r'$\gamma_1$')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel(r'LOE FACTOR - $U_1$')
    plt.tight_layout()

    plt.subplot(1,2,2)
    plt.plot(t,FAULT_VEC[5,:],color='k',label=r'$\gamma_2$')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel(r'LOE FACTOR - $U_2$')
    plt.tight_layout()    

    
    
    return None