import pydivide
import pytplot
import pandas as pd
from pytplot import data_quants
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy import interpolate


time = [8,12,16,20,24,28,32]
altitude = [25,100,500,600,605,630,700]
pytplot.store_data('spacecraft_altitude', data={'x':time,'y':altitude})

time = [2,11,14,20,25,30,40]
density = [100, 50, 10, 1,0,0,0]
pytplot.store_data('h_density', data={'x':time,'y':density})

def shift(l,n):
    return l[n:] + l[:n]

def link_to_tvar_manual(link,tvar):

    #if link == 'alt':
    #    link = 'spacecraft_altitude'
    #elif link == 'lat':
    #    link = 
    link_timeorig = np.asarray(data_quants[link].data.index.tolist())
    link_dataorig = np.asarray(data_quants[link].data[0].tolist())
    link_timeshift = np.asarray(shift(data_quants[link].data.index.tolist(), 1))
    link_datashift = np.asarray(shift(data_quants[link].data[0].tolist(),1))
    
    rise = link_datashift - link_dataorig
    rise = np.delete(rise,-1)
    run = link_timeshift - link_timeorig
    run = np.delete(run,-1)
    m = rise/run
    
    tvar_timeorig = np.asarray(data_quants[tvar].data.index.tolist())
    
    while tvar_timeorig[-1] > link_timeorig[-1]:
        tvar_timeorig = np.delete(tvar_timeorig,-1)
    while tvar_timeorig[0] > link_timeorig[0]:
        link_timeorig = np.delete(link_timeorig,0)
    link_interp = np.array([])
    link_time_interp = np.array([])
    for tvar_index,tvar_time in enumerate(tvar_timeorig):
        for link_index, link_time in enumerate(link_timeorig):
            if link_time == link_timeorig[-1]:
                pass
            elif link_timeorig[link_index] <= tvar_time and link_timeorig[link_index + 1] > tvar_time:
                slope = m[link_index]
                
                #y = m(x-x1) + y1
                y = slope*(tvar_timeorig[tvar_index]-link_timeorig[link_index])+ link_dataorig[link_index]
                prstr = str(slope) + "*" + str(tvar_timeorig[tvar_index]-link_timeorig[link_index]) + " + " + str(link_dataorig[link_index] - link_dataorig[0])
                print(prstr)
                link_interp = np.append(link_interp,y)
                link_time_interp = np.append(link_time_interp,tvar_timeorig[tvar_index])
    
        
    print(link_interp)
    print(link_time_interp)
    
    newvarname = link + "_" + tvar + "_link"
    pytplot.store_data(newvarname, data={'x':link_time_interp,'y':link_interp})
    
    #plt.plot(tvar_timeorig,link_interp,'r',link_timeorig,link_dataorig,'b')
    #plt.show()
    
def link_to_tvar(link,tvar,method):
    
    #pull saved variables from data_quants
    link_timeorig = np.asarray(data_quants[link].data.index.tolist())
    link_dataorig = np.asarray(data_quants[link].data[0].tolist())
    tvar_timeorig = np.asarray(data_quants[tvar].data.index.tolist())
    
    #shorten tvar array to be within link array
    while tvar_timeorig[-1] > link_timeorig[-1]:
        tvar_timeorig = np.delete(tvar_timeorig,-1)
    while tvar_timeorig[0] < link_timeorig[0]:
        tvar_timeorig = np.delete(tvar_timeorig,0)

    x = link_timeorig
    y = link_dataorig
    xnew = tvar_timeorig

    #choose method, interpolate, plot, and store
    if method == 'linear':
        f = interp1d(x,y)
        newvarname = link + "_" + tvar + "_link"
        pytplot.store_data(newvarname, data={'x':xnew,'y':f(xnew)})
    elif method == 'cubic':
        f2 = interp1d(x, y, kind='cubic')
        newvarname = link + "_" + tvar + "_link"
        pytplot.store_data(newvarname, data={'x':xnew,'y':f2(xnew)})
    elif method == 'spline':
        tck = interpolate.splrep(x, y, s=0)
        ynew = interpolate.splev(xnew, tck, der=0)
        newvarname = link + "_" + tvar + "_link"
        pytplot.store_data(newvarname, data={'x':xnew,'y':ynew})
        
    else:
        print('Error: choose interpolation method.')
        print('linear, cubic, spline')
        return
    
#link_to_tvar('spacecraft_altitude','h_density','cubic')
