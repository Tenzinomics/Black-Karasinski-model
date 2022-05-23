#!/usr/bin/env python
# coding: utf-8

# ## The python code of BK model 

# In[1]:

import numpy as np
#import matplotlib.pyplot as plt

def bk_model(a,k,sigma,multi_var_norm, tH, base_case):

    t_0 = 0 # define model parameters
   
    length = 10 #len(multi_var_norm)

    t = np.linspace(t_0,tH,length) # define time axis
    dt = np.mean(np.diff(t))
    y = np.zeros(length)
    z = np.zeros(length)
    y[0] = np.log(base_case) #np.log(0.05) # initial condition
    drift = lambda y: k +(y-k)*np.exp(-a*dt) # define drift term, using python lambda function
    hx = lambda x: np.sqrt(1-np.exp(-x))/np.sqrt(x) # 
   
    noise = multi_var_norm*sigma #define iid random normal noise

    # simulate one path multi-time-step OU process
    for i in np.arange(1,length):
       y[i] = drift(y[i-1]) + np.sqrt(dt)*hx(2*a*dt)*noise[i]
       z[i] = np.exp(y[i])

    return z[1:]


