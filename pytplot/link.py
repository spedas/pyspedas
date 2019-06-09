# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from pytplot import data_quants
import numpy as np

def link(names, link_name, link_type='alt'):
    
    link_type = link_type.lower()
    if not isinstance(names, list):
        names = [names]
        
    for i in names:
        if i not in data_quants.keys():
            print(str(i) + " is not currently in pytplot.")
            return
        
        if isinstance(i,int):
            i = list(data_quants.keys())[i-1]
    
        link_to_tvar(data_quants[i].name, link_type, link_name)
                
    return


def link_to_tvar(name, type, link, method='linear'):
    from scipy import interpolate
    from scipy.interpolate import interp1d
    from .store_data import store_data

    # pull saved variables from data_quants
    link_timeorig = np.asarray(data_quants[link].coords['time'].values)
    link_dataorig = np.asarray(data_quants[link].values)
    tvar_timeorig = np.asarray(data_quants[name].coords['time'].values)

    # If the two tplot variables have the same time cadence, we
    # don't need to do anything
    if np.array_equal(link_timeorig, tvar_timeorig):
        data_quants[name].attrs['plot_options']['links'][type] = link
        return

    # shorten tvar array to be within link array
    while tvar_timeorig[-1] > link_timeorig[-1]:
        tvar_timeorig = np.delete(tvar_timeorig, -1)
    while tvar_timeorig[0] < link_timeorig[0]:
        tvar_timeorig = np.delete(tvar_timeorig, 0)

    x = link_timeorig
    y = link_dataorig
    xnew = tvar_timeorig

    # choose method, interpolate, plot, and store
    if method == 'linear':
        f = interp1d(x, y)
        newvarname = link + "_" + name + "_link"
        store_data(newvarname, data={'x': xnew, 'y': f(xnew)})
    elif method == 'cubic':
        f2 = interp1d(x, y, kind='cubic')
        newvarname = link + "_" + name + "_link"
        store_data(newvarname, data={'x': xnew, 'y': f2(xnew)})
    elif method == 'quad_spline':
        tck = interpolate.splrep(x, y, s=0, k=2)
        ynew = interpolate.splev(xnew, tck, der=0)
        newvarname = link + "_" + name + "_link"
        store_data(newvarname, data={'x': xnew, 'y': ynew})

    else:
        print('Error: choose interpolation method.')
        print('linear, cubic, quad_spline')
        return

    data_quants[name].attrs['plot_options']['links'][type] = newvarname