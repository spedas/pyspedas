# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

# TPLOT_MATH
#   List of various mathematical functions for TVar manipulation.
#        add_data: add TVar1/2 data
#        sub_data: subtract TVar1/2 data
#        mult_data: multiply TVar1/2 data
#        div_data: divide TVar1/2 data, NaN for division by 0
#        deriv_data: take derivative w.r.t. of TVar data
#        flatten_data: divide each data column by column average over specified time
#        full_flatten: divide each data column by column average
#        interp_gap: interpolate through NaN data
#        fn_interp: linear interpolation, subfunction called in add/sub/mult/div
#        crop_data: shortens arrays to same timespan, subfunction called in fn_interp

import pytplot
import pydivide
import numpy as np
import pandas as pd
from scipy import interpolate
from scipy.interpolate import interp1d
from blaze import nan

#ADD
#add two tvar data arrays, store in new_tvar
def add_data(tvar1,tvar2,new_tvar,interp='linear'):
    #interpolate tvars
    tv1,tv2 = fn_interp(tvar1,tvar2,interp=interp)
    #separate and add data
    time = pytplot.data_quants[tv1].data.index
    data1 = pytplot.data_quants[tv1].data[0]
    data2 = pytplot.data_quants[tv2].data[0]
    data = data1 + data2
    #store added data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar

#SUBTRACT
#subtract two tvar data arrays, store in new_tvar
def sub_data(tvar1,tvar2,new_tvar,interp='linear'):
    #interpolate tvars
    tv1,tv2 = fn_interp(tvar1,tvar2,interp=interp)
    #separate and subtract data
    time = pytplot.data_quants[tv1].data.index
    data1 = pytplot.data_quants[tv1].data[0]
    data2 = pytplot.data_quants[tv2].data[0]
    data = data1 - data2
    #store subtracted data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar

#MULTIPLY
#multiply two tvar data arrays, store in new_tvar
def mult_data(tvar1,tvar2,new_tvar,interp='linear'):
    #interpolate tvars
    tv1,tv2 = fn_interp(tvar1,tvar2,interp=interp)
    #separate and multiply data
    time = pytplot.data_quants[tv1].data.index
    data1 = pytplot.data_quants[tv1].data[0]
    data2 = pytplot.data_quants[tv2].data[0]
    data = data1*data2
    #store multiplied data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar

#DIVIDE
#divide two tvar data arrays, store in new_tvar
def div_data(tvar1,tvar2,new_tvar,interp='linear'):
    #interpolate tvars
    tv1,tv2 = fn_interp(tvar1,tvar2,interp=interp)
    #separate and divide data
    time = pytplot.data_quants[tv1].data.index
    data1 = pytplot.data_quants[tv1].data[0]
    data2 = pytplot.data_quants[tv2].data[0]
    data = data1/data2
    #if division by 0, replace with NaN
    data = data.replace([np.inf,-np.inf],np.nan)
    #store divided data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar

#DERIVE
#take derivative w.r.t. time, store in new_tvar
def deriv_data(tvar1,new_tvar):
    #separate and derive data
    time = pytplot.data_quants[tvar1].data.index
    data1 = pytplot.data_quants[tvar1].data[0]
    data = np.diff(data1)/np.diff(time)
    time = np.delete(time,0)
    #store differentiated data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar

#PARTIAL FLATTEN
#take average of each column of data, divide column by average over specified time
def flatten_data(tvar1,start_t,end_t):
    df = pytplot.data_quants[tvar1].data
    time = df.index
    #if time given not an index, choose closest time
    if start_t not in time:
        tdiff = abs(time - start_t)
        start_t = time[tdiff.argmin()]
    if end_t not in time:
        tdiff = abs(time - end_t)
        end_t = time[tdiff.argmin()]
    df_index = list(df.columns)
    #divide by specified time average
    for i in df_index:
        df[i] = df[i]/((df.loc[start_t:end_t])[i]).mean()
    return

#FULL FLATTEN
#take average of each column of data, divide column by column average
def full_flatten(tvar1):
    df = pytplot.data_quants[tvar1].data
    df_index = list(df.columns)
    #divide by column average
    for i in df_index:
        df[i] = df[i]/df[i].mean()
    return

#LINEAR INTERPOLATION
#interpolate over NaN data
def interp_gap(tvar1):
    tv1 = pytplot.data_quants[tvar1].data
    print(tv1.dtypes)
    tv1 = tv1.astype(float)
    tv1 = tv1.interpolate(method='linear')
    tv1 = tv1.astype(object)
    return

#TVAR INTERPOLATION
#interpolate tvar2 to tvar1 cadence
def fn_interp(tvar1,tvar2,interp='linear'):
    #crop data
    tv1_t,tv1_d,tv2_t,tv2_d = crop_data(tvar1,tvar2)
    #interpolate to tvar1 cadence
    if interp == 'linear':
        print("linear interpolation")
        f = interp1d(tv2_t,tv2_d,fill_value="extrapolate")
        name1 = tvar1 + "_interp"
        name2 = tvar2 + "_interp"
        #store interpolated tvars as 'X_interp'
        pytplot.store_data(name1, data={'x':tv1_t,'y':tv1_d})
        pytplot.store_data(name2, data={'x':tv1_t,'y':f(tv1_t)})
    elif interp == 'cubic':
        print("cubic interpolation")
        f = interp1d(tv2_t,tv2_d,fill_value="extrapolate",kind='cubic')
        name1 = tvar1 + "_interp"
        name2 = tvar2 + "_interp"
        #store interpolated tvars as 'X_interp'
        pytplot.store_data(name1, data={'x':tv1_t,'y':tv1_d})
        pytplot.store_data(name2, data={'x':tv1_t,'y':f(tv1_t)})
    elif interp == 'spline':
        print("spline interpolation")
        tck = interpolate.splrep(tv2_t, tv2_d, s=0)
        ynew = interpolate.splev(tv1_t, tck, der=0)
        name1 = tvar1 + "_interp"
        name2 = tvar2 + "_interp"
        #store interpolated tvars as 'X_interp'
        pytplot.store_data(name1, data={'x':tv1_t,'y':tv1_d})
        pytplot.store_data(name2, data={'x':tv1_t,'y':ynew})

    return name1,name2

#DATA CROPPING
#crop tvar arrays to same timespan
def crop_data(tvar1,tvar2):
    #grab time and data arrays
    tv1_t = np.asarray(pytplot.data_quants[tvar1].data.index.tolist())
    tv1_d = np.asarray(pytplot.data_quants[tvar1].data[0].tolist())
    tv2_t = np.asarray(pytplot.data_quants[tvar2].data.index.tolist())
    tv2_d = np.asarray(pytplot.data_quants[tvar2].data[0].tolist())
        
    #find first and last time indices
    t0_1 = tv1_t[0]
    t0_2 = tv2_t[0]
    tx_1 = tv1_t[-1]
    tx_2 = tv2_t[-1]
    
    #find cut locations
    cut1 = max([t0_1, t0_2])
    cut2 = min([tx_1, tx_2])
    
    #trim data
    while tv1_t[-1] > cut2:
            tv1_t = np.delete(tv1_t,-1)
            tv1_d = np.delete(tv1_d,-1)
    while tv1_t[0] < cut1:
        tv1_t = np.delete(tv1_t,0)
        tv1_d = np.delete(tv1_d,0)
    while tv2_t[-1] > cut2:
        tv2_t = np.delete(tv2_t,-1)
        tv2_d = np.delete(tv2_d,-1)
    while tv2_t[0] < cut1:
        tv2_t = np.delete(tv2_t,0)
        tv2_d = np.delete(tv2_d,0)
    
    #return time and data arrays
    return tv1_t,tv1_d,tv2_t,tv2_d