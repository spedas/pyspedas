import pytplot
import pydivide
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import pandas as pd

#SPLIT TVAR
#store columns of TVar into new TVars
def split_vec(tvar,newtvars,columns):
    #separate and add data
    time = pytplot.data_quants[tvar].data.index
    data = pytplot.data_quants[tvar].data
    df = pytplot.data_quants[tvar]
    #grab column data
    for i,val in enumerate(columns):
        #if not a list
        if isinstance(val,int):
            range_start = val
            range_end = val
        else:
            range_start = val[0]
            range_end = val[1]
        split_col = list(range(range_start,range_end+1))
        #store split data
        pytplot.store_data(newtvars[i],data={'x':time, 'y':data[split_col]})
    return newtvars
