import statsmodels.api as sm
import numpy as np
import pandas as pd
import math
from openpyxl import Workbook
import openpyxl as pxl


#This function creates the a and k parameter for each riskfactor
def paramater_tinator(rf_df):   
   
   #Getting the length of the dataframe
   n=len(rf_df[0:])
   
   #Creating lead and lagg var log Difference variable 
   zt=np.log(rf_df.values[0:n-1])
   xt=np.log(rf_df.values[1:n])

   #Replacing the infinity value with the null value
   zt = np.where(zt==-np.Inf, np.nan,zt)
   xt = np.where(xt==-np.Inf, np.nan,xt)
   
   #OLS with xt as dependent variable and zt as explanatory variable and dropping the null value
   model_ols = sm.OLS(zt, sm.add_constant(xt), missing='drop')
   
   #Storing the result of ols
   model_results = model_ols.fit()

   #Getting the parameter from the result
   k=model_results.params[0]/(1-model_results.params[1])
   a=-np.log(model_results.params[1])

   return a,k

#Corrolation Matrix
def std_multi_variate_normal(tH, num_scen, vcv_obj, rf_match):
   
   vcv_sq=vcv_obj

   nRF= len(vcv_sq)
   mean=np.zeros(nRF)

   multi_gauss_nh = np.random.default_rng().multivariate_normal(mean, vcv_sq, size=num_scen, check_valid='warn', tol=1e-8)
   multi_gauss_nh=multi_gauss_nh*math.sqrt(tH) 

   df_std = pd.DataFrame(columns=vcv_obj.columns)
   for i in range(len(multi_gauss_nh)):
      df_std.loc[i]=multi_gauss_nh[i]

   return df_std[rf_match]  #2D DataFrame with header 


#This function creates excel sheet
def excel_send_tinator(dis_file_name, dis_sheet_name,df_values):

   workbook = Workbook()
   sheet = workbook.active

   workbook.save(filename=dis_file_name)

   filename = dis_file_name

   excel_book = pxl.load_workbook(filename)

   with pd.ExcelWriter(filename, engine='openpyxl') as writer:

      writer.book = excel_book

      book = writer.book

      #Exprting df to excel
      df_values.to_excel(writer, sheet_name=dis_sheet_name)
      

      writer.save()
      
   excel_book.close()
