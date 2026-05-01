import pyspedas
from pyspedas.tplot_tools import store_data, tplot_wildcard_expand
import pandas as pd
import copy
import xarray as xr
import logging
import numpy as np

from pyspedas.tplot_tools import convert_tplotxarray_to_pandas_dataframe


# JOIN TVARS
# join TVars into single TVar with multiple columns
def join_vec(tvars, newname=None, merge=False):
    """
    Joins 1D tplot variables into one tplot variable.

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions. If there are more, they may become flattened!

    Parameters
    ----------
    tvars : list of str
        Name of tplot variables to join together.
    newname : str, optional
        The name of the new tplot variable. If not specified (the default), a name will be assigned.
    merge : bool, optional
        Whether or not to merge the created variable into an older variable.
        Default is False.

    Returns
    -------
    None

    Examples
    --------
    >>> import pyspedas
    >>> import numpy as np
    >>> pyspedas.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})
    >>> pyspedas.store_data('e', data={'x':[2,5,8,11,14,17,21], 'y':[[np.nan,1,1],[np.nan,2,3],[4,np.nan,47],[4,np.nan,5],[5,5,99],[6,6,25],[7,np.nan,-5]]})
    >>> pyspedas.store_data('g', data={'x':[0,4,8,12,16,19,21], 'y':[[8,1,1],[100,2,3],[4,2,47],[4,39,5],[5,5,99],[6,6,25],[7,-2,-5]]})
    >>> pyspedas.join_vec(['d','e','g'],newname='deg')

    """

    to_merge = False
    if newname in pyspedas.tplot_tools.data_quants.keys() and merge:
        prev_data_quant = pyspedas.tplot_tools.data_quants[newname]
        to_merge = True

    # Allow wildcard specification
    tvars=tplot_wildcard_expand(tvars)

    if newname is None:
        newname = "-".join(tvars) + "_joined"

    has_extra_v_values = False
    v_shape = None
    data_shape = None
    combined_v = None

    # Make sure all the components exist and are compatible to be joined
    for i, val in enumerate(tvars):
        dq = pyspedas.tplot_tools.data_quants[val]
        data_shape = dq.values.shape
        if len(data_shape) != 1:
            logging.error(f"join_vec: variable {val} must be 1-dimensional, but has shape {data_shape}.")
            return None
        if i == 0:
            if 'extra_v_values' in dq.attrs.keys():
                has_extra_v_values = True
                extra_v_values = dq.attrs['extra_v_values']
                v_shape = extra_v_values.shape
                # If extra_v_values has multiple elements, maybe it's time varying....it should match the number of timestamps.
                # We'll create the array here, and populate each row as we go.
                if has_extra_v_values:
                    if len(extra_v_values) == 1:
                        combined_v = np.empty((len(tvars),),dtype=extra_v_values.dtype)
                        combined_v[0] = extra_v_values[0]
                    elif len(extra_v_values) == data_shape[0]:
                        combined_v = np.empty((data_shape[0],len(tvars)), dtype=extra_v_values.dtype)
                        combined_v[:,0] = extra_v_values
                    else:
                        logging.error(f"join_vec: variable {val} has shape {data_shape}, but has incompatible extra_v_values shape {v_shape}.")
                        return None
            df = convert_tplotxarray_to_pandas_dataframe(tvars[i], no_spec_bins=True)

        else:
            if 'extra_v_values' in dq.attrs.keys():
                current_has_extra_v_values = True
                current_extra_v_values = dq.attrs['extra_v_values']
                current_v_shape = current_extra_v_values.shape
            else:
                current_has_extra_v_values = False
                current_extra_v_values = None
                current_v_shape = None
            current_data_shape = dq.values.shape

            if current_has_extra_v_values != has_extra_v_values:
                logging.error(f"join_vec: Unable to combine {tvars[0]} and {tvars[i]}, mismatched extra_v_values attributes.")
                return None
            elif has_extra_v_values and v_shape != current_v_shape:
                logging.error(f"join_vec: Unable to combine {tvars[0]} and {tvars[i]}, mismatched extra_v_values shapes {v_shape} and {current_v_shape}.")
                return None
            elif data_shape != current_data_shape:
                logging.error(f"join_vec: Unable to combine {tvars[0]} and {tvars[i]}, mismatched data shapes {data_shape} and {current_data_shape}")
                return None

            if has_extra_v_values and v_shape[0] == 1:
                combined_v[i] = current_extra_v_values[0]
            elif has_extra_v_values and v_shape[0] > 1:
                combined_v[:,i] = current_extra_v_values
            d = convert_tplotxarray_to_pandas_dataframe(tvars[i], no_spec_bins=True)
            df = pd.concat([df, d], axis=1)

    if combined_v is None:
        store_data(newname, data={"x": df.index, "y": df.values})
    else:
        store_data(newname, data={"x": df.index, "y": df.values, "v": combined_v})

    if to_merge is True:
        cur_data_quant = pyspedas.tplot_tools.data_quants[newname]
        plot_options = copy.deepcopy(pyspedas.tplot_tools.data_quants[newname].attrs)
        pyspedas.tplot_tools.data_quants[newname] = xr.concat(
            [prev_data_quant, cur_data_quant], dim="time"
        ).sortby("time")
        pyspedas.tplot_tools.data_quants[newname].attrs = plot_options

    return newname
