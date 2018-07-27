import pytplot
import pydivide
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import pandas as pd

#MULTIPLY
#multiply two tvar data arrays, store in new_tvar
def multiply(tvar1,tvar2,new_tvar,interp='linear'):
    #interpolate tvars
    tv1,tv2 = pytplot.interpolate(tvar1,tvar2,interp=interp)
    #separate and multiply data
    time = pytplot.data_quants[tv1].data.index
    data1 = pytplot.data_quants[tv1].data
    data2 = pytplot.data_quants[tv2].data
    data = data1*data2
    #store multiplied data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar