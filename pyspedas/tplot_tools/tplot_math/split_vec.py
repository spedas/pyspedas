"""
Splits up 2D data into many 1D tplot variables.

Notes
-----
Similar to split_vec.pro in IDL SPEDAS.

"""

import copy
import logging
import pyspedas
from pyspedas.tplot_tools import store_data, get_data
import numpy as np
import logging

def split_vec(
        tvar,
        polar=False,
        newname=None,
        new_name=None,
        columns='all',
        suffix=None
):
    """
    Splits up 2D data into many 1D tplot variables. Takes a stored tplot vector like Vp
    and stores tplot variables Vp_x, Vp_y, Vp_z

    Parameters
    ----------
        tvar : str
            Name of tplot variable to split up
        polar : bool, optional
            If True, the input data is in polar coordinates.
            Suffix will be set to ['_mag', '_th', '_phi'].
            Default: False
        new_name : int/list, optional (Deprecated)
            The names of the new tplot variables.
            This must be the same length as the number of variables created.
        newname : int/list, optional
            The names of the new tplot variables.
            This must be the same length as the number of variables created.
            Default: None
        columns : list of ints, optional
            The specific column numbers to grab from the data.
            Default: 'all' (splits all columns)
        suffix: str
            Suffix str to be added to end of tplot variable name
            Default: None

    Returns
    -------
    list[str]
        List of variables created

    Examples
    --------
        >>> pyspedas.store_data('b', data={'x':[2,5,8,11,14,17,20], 'y':[[1,1,1,1,1,1],[2,2,5,4,1,1],[100,100,3,50,1,1],[4,4,8,58,1,1],[5,5,9,21,1,1],[6,6,2,2,1,1],[7,7,1,6,1,1]]})
        >>> pyspedas.split_vec('b')



    """
    # new_name is deprecated in favor of newname
    if new_name is not None:
        logging.info("split_vec: The new_name parameter is deprecated. Please use newname instead.")
        newname = new_name

    # Make sure the tvar is found
    if tvar not in pyspedas.tplot_tools.data_quants:
        logging.error(f"Error: {tvar} not found in memory.")
        return None

    # Give a default to the new name
    if newname is None:
        newname = tvar

    # Gather data from the tvar
    alldata = get_data(tvar)
    time = alldata[0]
    data = alldata[1]
    dim = data.shape
    metadata = get_data(tvar, metadata=True)

    has_v = False
    combined_v = None
    time_varying_v = False

    # If already size one, simply return
    if len(dim) == 1:
        return [tvar]
    # Is there depend_1 data to split?
    elif len(dim) == 2:
        if len(alldata) == 3:
            has_v = True
            combined_v = alldata[2]
            if len(combined_v.shape) == 1:
                time_varying_v = False
            else:
                time_varying_v = True

    elif len(dim) > 2:
        logging.error(f"split_vec:data array for {tvar} has {len(dim)} dimensions, too many to split")
        return None


    vec_length = dim[1]

    # Determine what the suffix list will be
    if suffix is not None:
        if vec_length > len(suffix):
            logging.error(f"split_vec error: number of columns ({vec_length}) is greater than the number of suffix entered")
    else:
        if vec_length == 3:
            if polar:
                suffix = ['_mag', '_th', '_phi']
            else:
                suffix = ["_x", "_y", "_z"]
        else:
            suffix = []
            for i in range(vec_length):
                suffix.append("_"+str(i))

    created_variables = []

    # grab column data
    if columns == 'all':
        columns = range(vec_length)

    v_idx = 0
    for i in columns:
        # if not a list
        if isinstance(i, list):
            range_start = i[0]
            range_end = i[1]
        else:
            range_start = i
            range_end = i
        split_col = list(range(range_start, range_end+1))
        split_name = newname + suffix[i]
        created_variables = created_variables + [split_name]

        if has_v and time_varying_v:
            data_for_tplot = {'x': time, 'y': data[:, split_col].squeeze(), 'v': combined_v[:,v_idx]}
        elif has_v and not time_varying_v:
            data_for_tplot = {'x': time, 'y': data[:, split_col].squeeze(), 'v': np.array([combined_v[v_idx]])}
        else:
            data_for_tplot = {'x': time, 'y': data[:, split_col].squeeze()}

        plot_options = metadata.get('plot_options', {})
        yaxis_opt = plot_options.get('yaxis_opt', {})
        labels = yaxis_opt.get('legend_names', None)
        if labels is None:
            cdf = metadata.get('CDF', {})
            labels = cdf.get('LABELS', None)

        if labels is None:
            attrs = metadata
        else:
            # Make a deep copy to avoid modifying original metadata
            attrs = copy.deepcopy(metadata)
            if 'plot_options' not in attrs:
                attrs['plot_options'] = {}
            if 'yaxis_opt' not in attrs['plot_options']:
                attrs['plot_options']['yaxis_opt'] = {}
            attrs['plot_options']['yaxis_opt']['legend_names'] = []

            if v_idx < len(labels):
                attrs['plot_options']['yaxis_opt']['legend_names'].append(labels[v_idx])

        if not store_data(split_name, data=data_for_tplot, attr_dict=attrs):
            raise Exception(f"Failed to store {split_name} in pyspedas.")
        v_idx += 1

    return created_variables
