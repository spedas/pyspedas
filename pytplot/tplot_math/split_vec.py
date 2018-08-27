import pytplot
import pydivide
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import pandas as pd

#SPLIT TVAR
#store columns of TVar into new TVars
def split_vec(tvar,newtvars=None,columns='all'):
    #separate and add data
    time = pytplot.data_quants[tvar].data.index
    data = pytplot.data_quants[tvar].data
    df = pytplot.data_quants[tvar]
    defaultlist = []
    #grab column data
    if columns == 'all':
        columns = pytplot.data_quants[tvar].data.columns.values
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
        defaultname = 'data_' + str(i)
        defaultlist = defaultlist + [defaultname]
        if newtvars is None:
            pytplot.store_data(defaultname,data={'x':time, 'y':data[split_col]})
        else:
            pytplot.store_data(newtvars[i],data={'x':time, 'y':data[split_col]})
    if newtvars is None:
        return defaultlist
    else:
        return newtvars
