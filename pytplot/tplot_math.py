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
from scipy import interpolate
from scipy.interpolate import interp1d

#ADD TWO ARRAYS
#add two tvar data arrays, store in new_tvar
def add_data(tvar1,tvar2,new_tvar,interp='linear'):
    #interpolate tvars
    tv1,tv2 = fn_interp(tvar1,tvar2,interp=interp)
    #separate and add data
    time = pytplot.data_quants[tv1].data.index
    data1 = pytplot.data_quants[tv1].data
    data2 = pytplot.data_quants[tv2].data
    data = data1+data2
    #store added data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar

#ADD ACROSS COLUMNS
#add tvar data across columns, store in new_tvar
def add_data_across(tvar1,new_tvar):
    #separate and add data
    time = pytplot.data_quants[tvar1].data.index
    data1 = pytplot.data_quants[tvar1].data
    data = data1.sum(axis=1)
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
    data1 = pytplot.data_quants[tv1].data
    data2 = pytplot.data_quants[tv2].data
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
    data1 = pytplot.data_quants[tv1].data
    data2 = pytplot.data_quants[tv2].data
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
    data1 = pytplot.data_quants[tv1].data
    data2 = pytplot.data_quants[tv2].data
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
    data1 = pytplot.data_quants[tvar1].data
    df_index = pytplot.data_quants[tvar1].data.columns
    new_df = []
    for i in df_index:
        tv1_col = data1[i]
        data = np.diff(tv1_col)/np.diff(time)
        new_df = new_df + [data]
    new_df = np.transpose((list(new_df)))
    time = np.delete(time,0)
    #store differentiated data
    pytplot.store_data(new_tvar,data={'x':time, 'y':new_df})
    return new_tvar

#PARTIAL FLATTEN
#take average of each column of data, divide column by average over specified time
def flatten_data(tvar1,start_t,end_t,new_tvar):
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
    pytplot.store_data(new_tvar,data = {'x':df.index,'y':df})
    return new_tvar

#FULL FLATTEN
#take average of each column of data, divide column by column average
def full_flatten(tvar1,new_tvar):
    df = pytplot.data_quants[tvar1].data
    df_index = list(df.columns)
    #divide by column average
    for i in df_index:
        df[i] = df[i]/df[i].mean()
    pytplot.store_data(new_tvar,data = {'x':df.index,'y':df})
    return new_tvar

def avg_res_data(tvar1,res,new_tvar):
    #grab info from tvar
    df = pytplot.data_quants[tvar1].data
    time = df.index
    start_t = df.index[0]
    end_t = df.index[-1]
    df_index = list(df.columns)
    #create list of times spanning tvar range @ specified res
    res_time = np.arange(start_t,end_t+1,res)
    new_res_time = np.array([])
    #find closest time to new resolution times
    for t in res_time:
        if t not in time:
            tdiff = abs(time-t)
            new_res_time = np.append(new_res_time,time[tdiff.argmin()])
        else:
            new_res_time = np.append(new_res_time,t)
    #make sure no duplicate times from resolution time rounding
    new_res_time = np.unique(new_res_time)
    #shift start time array
    start_t = np.roll(new_res_time,1)
    end_t = new_res_time
    start_t = np.delete(start_t,0)
    end_t = np.delete(end_t,0)
    #initialize arrays
    avg_bin_data = []
    avg_bin_time = np.array([])
    #for each time bin
    for it,t in enumerate(start_t):
        #for each data column
        data_avg_bin = np.array([])
        for i in df_index:
            #append localized bin average to data_avg_bin
            data_avg_bin = np.append(data_avg_bin,[(df.loc[start_t[it]:end_t[it]])[i].mean()])
        #append whole array of bin averages (over n columns) to avg_bin_data
        avg_bin_data = avg_bin_data + [data_avg_bin.tolist()]
        avg_bin_time = np.append(avg_bin_time,t)
    #store data in new_tvar
    pytplot.store_data(new_tvar, data={'x':avg_bin_time,'y':avg_bin_data})
    return new_tvar    
    
#LINEAR INTERPOLATION
#interpolate over NaN data
def interp_gap(tvar1):
    tv1 = pytplot.data_quants[tvar1].data
    tv1 = tv1.astype(float)
    tv1 = tv1.interpolate(method='linear')
    tv1 = tv1.astype(object)
    return tv1

#TVAR INTERPOLATION
#interpolate tvar2 to tvar1 cadence
def fn_interp(tvar1,tvar2,interp='linear'):
    #crop data
    tv1_t,tv1_d,tv2_t,tv2_d = crop_data(tvar1,tvar2)
    df_index = pytplot.data_quants[tvar1].data.columns
    #interpolate to tvar1 cadence
    if interp == 'linear':
        print("linear interpolation")
        name1 = tvar1 + "_interp"
        name2 = tvar2 + "_interp"
        new_df = []
        for i in df_index:
            tv2_col = [item[i] for item in tv2_d]
            f = interp1d(tv2_t,tv2_col,fill_value="extrapolate")
            new_df = new_df + [f(tv1_t)]
        new_df = np.transpose((list(new_df)))
        #store interpolated tvars as 'X_interp'
        pytplot.store_data(name1, data={'x':tv1_t,'y':tv1_d})
        pytplot.store_data(name2, data={'x':tv1_t,'y':new_df})
    elif interp == 'cubic':
        print("cubic interpolation")
        new_df = []
        for i in df_index:
            tv2_col = [item[i] for item in tv2_d]
            f = interp1d(tv2_t,tv2_col,kind='cubic')
            new_df = new_df + [f(tv1_t)]
        new_df = np.transpose((list(new_df)))
        name1 = tvar1 + "_interp"
        name2 = tvar2 + "_interp"
        #store interpolated tvars as 'X_interp'
        pytplot.store_data(name1, data={'x':tv1_t,'y':tv1_d})
        pytplot.store_data(name2, data={'x':tv1_t,'y':new_df})
    elif interp == 'spline':
        print("spline interpolation")
        new_df = []
        for i in df_index:
            tv2_col = [item[i] for item in tv2_d]
            tck = interpolate.splrep(tv2_t, tv2_col, s=0,k=2)
            ynew = interpolate.splev(tv1_t, tck, der=0)
            new_df = new_df + [ynew]
        new_df = np.transpose((list(new_df)))
        name1 = tvar1 + "_interp"
        name2 = tvar2 + "_interp"
        #store interpolated tvars as 'X_interp'
        pytplot.store_data(name1, data={'x':tv1_t,'y':tv1_d})
        pytplot.store_data(name2, data={'x':tv1_t,'y':new_df})
    return name1,name2

#DATA CROPPING
#crop tvar arrays to same timespan
def crop_data(tvar1,tvar2):
    #grab time and data arrays
    tv1_t = np.asarray(pytplot.data_quants[tvar1].data.index.tolist())
    tv1_d = np.asarray(pytplot.data_quants[tvar1].data)
    tv2_t = np.asarray(pytplot.data_quants[tvar2].data.index.tolist())
    tv2_d = np.asarray(pytplot.data_quants[tvar2].data)
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
        tv1_t = np.delete(tv1_t,-1,axis=0)
        tv1_d = np.delete(tv1_d,-1,axis=0)
    while tv1_t[0] < cut1:
        tv1_t = np.delete(tv1_t,0,axis=0)
        tv1_d = np.delete(tv1_d,0,axis=0)
    while tv2_t[-1] > cut2:
        tv2_t = np.delete(tv2_t,-1,axis=0)
        tv2_d = np.delete(tv2_d,-1,axis=0)
    while tv2_t[0] < cut1:
        tv2_t = np.delete(tv2_t,0,axis=0)
        tv2_d = np.delete(tv2_d,0,axis=0)
    #return time and data arrays
    return tv1_t,tv1_d,tv2_t,tv2_d
