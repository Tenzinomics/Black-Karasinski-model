import numpy as np

def black_karasinski(r0, theta, alpha, sigma, T, n):
    dt = T/n
    rt = np.zeros(n+1)
    rt[0] = r0
    dwt = np.random.normal(size=n)* np.sqrt(dt) #The drift term -- vector of random normal distribution multiplied by scalar squareroot
    for i in range(n):
        rt[i+1] = rt[i] + theta[i]*dt - alpha[i]*rt[i]*dt + sigma[i]*dwt[i]

    return rt

#The calibration is still work in progress
def calibration_obj(x, r0, r_market, T, n):
    theta, alpha, sigma = x[:n], x[n:2*n], x[2*n:]
    r_model = black_karasinski(r0, theta, alpha, sigma, T, n)
    return np.sum((r_model - r_market)**2)





#**My Old BK model**
# def bk_model(a,k,sigma,multi_var_norm, tH, base_case):

#     t_0 = 0 # define model parameters
   
#     length = len(multi_var_norm)

#     t = np.linspace(t_0,tH,length) # define time axis
#     dt = np.mean(np.diff(t))
#     y = np.zeros(length)
#     z = np.zeros(length)
#     y[0] = np.log(base_case) #np.log(0.05) # initial condition
#     drift = lambda y: k +(y-k)*np.exp(-a*dt) # define drift term, using python lambda function
#     hx = lambda x: np.sqrt(1-np.exp(-x))/np.sqrt(x) # 
   
#     noise = multi_var_norm*sigma #define iid random normal noise

#     # simulate one path multi-time-step OU process
#     for i in np.arange(1,length):
#        y[i] = drift(y[i-1]) + np.sqrt(dt)*hx(2*a*dt)*noise[i]
#        z[i] = np.exp(y[i])

#     return z[1:]
