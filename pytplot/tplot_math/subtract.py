import pytplot
import pydivide
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import pandas as pd

#SUBTRACT
#subtract two tvar data arrays, store in new_tvar
def subtract(tvar1,tvar2,new_tvar,interp='linear'):
    #interpolate tvars
    tv1,tv2 = pytplot.interpolate(tvar1,tvar2,interp=interp)
    #separate and subtract data
    time = pytplot.data_quants[tv1].data.index
    data1 = pytplot.data_quants[tv1].data
    data2 = pytplot.data_quants[tv2].data
    data = data1 - data2
    #store subtracted data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar