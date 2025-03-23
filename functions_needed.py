import statsmodels.api as sm
import numpy as np

#This function creates the a and k parameter for each riskfactor
def paramater_(rf_df):   
   
   #Getting the length of the dataframe
   n=len(rf_df[0:])
   
   #Creating lead and lagg var log Difference variable 
   zt=np.log(rf_df.values[0:n-1])
   xt=np.log(rf_df.values[1:n])

   #Replacing the infinity value with the null value
   zt = np.where(np.isinf(zt) & (zt == -np.inf), np.nan, zt) #np.where(zt==-np.Inf, np.nan,zt)
   xt = np.where(np.isinf(xt) & (xt == -np.inf), np.nan, xt)

   
   #OLS with xt as dependent variable and zt as explanatory variable and dropping the null value
   model_ols = sm.OLS(zt, sm.add_constant(xt), missing='drop')
   
   #Storing the result of ols
   model_results = model_ols.fit()

   #Getting the parameter from the result
   k=model_results.params[0]/(1-model_results.params[1])
   a=-np.log(model_results.params[1])

   return a,k

#Corrolation Matrix -- The function below is for my old BK model
# def std_multi_variate_normal(tH, num_scen, vcv_obj, rf_match):
   
#    vcv_sq=vcv_obj

#    nRF= len(vcv_sq)
#    mean=np.zeros(nRF)

#    multi_gauss_nh = np.random.default_rng().multivariate_normal(mean, vcv_sq, size=num_scen, check_valid='warn', tol=1e-8)
#    multi_gauss_nh=multi_gauss_nh*math.sqrt(tH) 

#    df_std = pd.DataFrame(columns=vcv_obj.columns)
#    for i in range(len(multi_gauss_nh)):
#       df_std.loc[i]=multi_gauss_nh[i]

#    return df_std[rf_match]  #2D DataFrame with header 
