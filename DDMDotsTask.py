import sys, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import hddm

def fit_subject(data, quantiles):

    """
    Simulates stim-coded data.
    """

    subj_idx = np.unique(data['subj_idx'])
    print(subj_idx)
    #m = hddm.HDDMStimCoding(data, stim_col='stim', split_param='v',  p_outlier=0,
    #                        depends_on={'v':'age', 'a':'age', 't':'age', })
    m = hddm.HDDM(data,depends_on={'v':'age'})
    m.optimize('gsquare', quantiles=quantiles, n_runs=8)
    res = pd.concat((pd.DataFrame([m.values], index=[subj_idx]), pd.DataFrame([m.bic_info], index=[subj_idx])), axis=1)
    return res


# settings

os.chdir('/fs03/ep52/MeadhbhProject/')
os.getcwd()
dfs = hddm.load_csv('Data/MData.csv')

# combine in one dataframe:
df_emp = dfs
df_emp.loc[df_emp["response"]==2, 'response'] = 0
df_emp.loc[df_emp["correct"]==2, 'correct'] = 0
df_emp.loc[df_emp["age"]==2, 'age'] = 'young'
df_emp.loc[df_emp["age"]==1, 'age'] = 'old'
df_emp.loc[df_emp["age"]==3, 'age'] = 'old'
df_emp.rt = df_emp.rt/1000
if go_nogo:
    df_emp.loc[df_emp["response"]==0, 'rt'] = np.NaN


quantiles = [.1, .3, .5, .7, .9]
params_fitted = pd.concat(fit_subject(data[1], quantiles) for data in df_emp.groupby('subj_idx'))
params_fitted.to_csv(r'DDM_OldYoung.csv')