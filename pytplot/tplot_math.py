# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

# TPLOT_MATH
#   List of various mathematical functions for TVar manipulation.
#        add_data:
#        sub_data:
#        mult_data:
#        div_data:
#        deriv_data:
#        flatten_data:
#        interp_gap:
#        lin_interp: linear interpolation, subfunction called in add/sub/mult/div
#        crop_data: shortens arrays to same timespan, subfunction called in lin_interp



import pytplot
import pydivide
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
        
insitu = pydivide.read('2017-06-19')
t = insitu['Time']
data = insitu['SPACECRAFT']['ALTITUDE']
lat = insitu['SPACECRAFT']['SUB_SC_LATITUDE']
lon = insitu['SPACECRAFT']['SUB_SC_LONGITUDE']
pytplot.store_data('sc_lon', data={'x':t, 'y':lon})
pytplot.store_data('sc_alt', data={'x':t, 'y':data})
pytplot.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
pytplot.store_data('b', data={'x':[2,5,8,11,14,17,20], 'y':[1,2,3,4,5,6,7]})

#print(pytplot.data_quants['sc_lon'].data.head(1))
#print(pytplot.data_quants['sc_alt'].data.head(1))
#print(pytplot.data_quants['sc_lon'].data.tail(1))
#print(pytplot.data_quants['sc_alt'].data.tail(1))

#ADD
#add two tvar data arrays, store in new_tvar
def add_data(tvar1,tvar2,new_tvar):
    #interpolate tvars
    tv1,tv2 = lin_interp(tvar1,tvar2)
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
def sub_data(tvar1,tvar2,new_tvar):
    #interpolate tvars
    tv1,tv2 = lin_interp(tvar1,tvar2)
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
def mult_data(tvar1,tvar2,new_tvar):
    #interpolate tvars
    tv1,tv2 = lin_interp(tvar1,tvar2)
    #separate and add data
    time = pytplot.data_quants[tv1].data.index
    data1 = pytplot.data_quants[tv1].data[0]
    data2 = pytplot.data_quants[tv2].data[0]
    data = data1*data2
    #store added data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar

## WILL NEED DIV BY 0 ERROR HANDLING
#DIVIDE
#divide two tvar data arrays, store in new_tvar
def div_data(tvar1,tvar2,new_tvar):
    #interpolate tvars
    tv1,tv2 = lin_interp(tvar1,tvar2)
    #separate and add data
    time = pytplot.data_quants[tv1].data.index
    data1 = pytplot.data_quants[tv1].data[0]
    data2 = pytplot.data_quants[tv2].data[0]
    data = data1/data2
    #store added data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar

#DERIVE
#take derivative w.r.t. time, store in new_tvar
def deriv_data(tvar1,new_tvar):
    #separate and derive data
    time = pytplot.data_quants[tvar1].data.index
    data1 = pytplot.data_quants[tvar1].data[0]
    data = np.diff(data1)
    time = np.delete(time,0)
    #store added data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar

def flatten_data(tvar1,tvar2):
    pass
    return

def interp_gap(tvar1,tvar2):
    pass
    return

#LINEAR INTERPOLATION
#interpolate tvar2 to tvar1 cadence
def lin_interp(tvar1,tvar2):
    #crop data
    tv1_t,tv1_d,tv2_t,tv2_d = crop_data(tvar1,tvar2)
        
    #interpolate to tvar1 cadence
    f = interp1d(tv2_t,tv2_d,fill_value="extrapolate")
    name1 = tvar1 + "_interp"
    name2 = tvar2 + "_interp"
    #store interpolated tvars as 'X_interp'
    pytplot.store_data(name1, data={'x':tv1_t,'y':tv1_d})
    pytplot.store_data(name2, data={'x':tv1_t,'y':f(tv1_t)})

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
        
    #pass only tvar1 time to interpolation
    #print(tv1_t,tv1_d,tv2_t,tv2_d)
    return tv1_t,tv1_d,tv2_t,tv2_d

deriv_data('sc_lon','a*b')
#print(pytplot.data_quants['sc_lon_interp'].data.head(2))
#print(pytplot.data_quants['sc_alt_interp'].data.head(2))
print(pytplot.data_quants['a*b'].data)
#print(np.diff(pytplot.data_quants['sc_lon_interp'].data.index))
#lin_interp('a','b')
#print(pytplot.data_quants['b_interp'].data)
