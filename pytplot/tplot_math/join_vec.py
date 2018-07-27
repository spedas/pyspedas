import pytplot
import pydivide
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import pandas as pd

#JOIN TVARS
#join TVars into single TVar with multiple columns
def join_vec(tvars,newtvar):
    df = pytplot.data_quants[tvars[0]].data
    for i,val in enumerate(tvars):
        if i == 0:
            pass
        else:
            df = pd.concat([df,pytplot.data_quants[val].data],axis=1)
    pytplot.store_data(newtvar,data={'x':df.index,'y':df})
    return newtvar