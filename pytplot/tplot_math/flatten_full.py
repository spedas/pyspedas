import pytplot
import pydivide
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import pandas as pd

#FULL FLATTEN
#take average of each column of data, divide column by column average
def flatten_full(tvar1,new_tvar):
    df = pytplot.data_quants[tvar1].data
    df_index = list(df.columns)
    #divide by column average
    for i in df_index:
        df[i] = df[i]/df[i].mean()
    pytplot.store_data(new_tvar,data = {'x':df.index,'y':df})
    return new_tvar