# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pyspedas
import copy

def reduce_spec_dataset(tplot_dataset=None, name=None):
    # This function will reduce the data in a 3+ dimensional DataSet object into something that can be plotted with a
    # spectrogram, either by taking slices of the data or by summing the dimensions into this one.
    if tplot_dataset is not None:
        da = copy.deepcopy(tplot_dataset)
    elif name is not None:
        da = copy.deepcopy(pyspedas.tplot_tools.data_quants[name])
    else:
        return

    if da.attrs['plot_options']['extras'].get('spec_dim_to_plot', None) is not None:
        coordinate_to_plot = da.attrs['plot_options']['extras']['spec_dim_to_plot']
    else:
        # If not found, default to v2 (to match behavior in options.py when setting "spec" option)
        coordinate_to_plot = "v2"

    dim_to_plot = coordinate_to_plot + '_dim'

    for d in da.dims:
        if d == dim_to_plot:
            pass
        elif d == 'time':
            pass
        else:
            if 'spec_slices_to_use' in da.attrs['plot_options']['extras']:
                for key, value in da.attrs['plot_options']['extras']['spec_slices_to_use'].items():
                    dim = key+"_dim"
                    if dim == d:
                        da=da.isel({dim:value})
                        break
                else:
                    da = da.sum(dim=d, skipna=True, keep_attrs=True)
            else:
                da = da.sum(dim=d, skipna=True, keep_attrs=True)
    return da

