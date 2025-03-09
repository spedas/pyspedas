import numpy as np
from copy import deepcopy
from pytplot import get_data, store_data, options, tplot_wildcard_expand
from typing import Union, List
import logging

def _tvectot(tvar: str, new_name: str, join_component: bool):
    data = get_data(tvar)
    md = get_data(tvar,metadata=True)
    new_data = np.linalg.norm(data.y, axis=1)

    if join_component:
        # Caution: this can clobber existing variable names!  Maybe better to manipulate the
        # data directly instead of calling split_vec/join_vec
        #join_vec(split_vec(tvar)+[new_name], newname=new_name)
        joined_data = np.append(data.y, new_data[:,np.newaxis],1)
        store_data(new_name, data={'x':data.times,'y':joined_data}, attr_dict=deepcopy(md))
        options(new_name, 'legend_names', ['x', 'y', 'z', 'Magnitude'])
    else:
        store_data(new_name, data={'x': data.times, 'y': new_data}, attr_dict=md)
        options(new_name, 'legend_names', 'Magnitude')
    return new_name

def tvectot(tvars: Union[str, List[str]],
            newname=None,
            newnames: Union[str, List[str]] = None,
            suffix=None,
            join_component=True) -> Union[str , List[str]]:
    """
    Computes the magnitude of a vector time series.

    Parameters
    ----------
    tvars : str or list[str]
        Names of the tplot variables.
    newnames: str or list[str]
        (Deprecated) Names for the resultant magnitude tplot variables. If not provided, it appends the suffix to `tvars`.
    newname: str or list[str]
        Names for the resultant magnitude tplot variables. If not provided, it appends the suffix to `tvars`.
    suffix: str
        The suffix to append to tvars to form newnames if newnames is not provided.
    join_component: bool
        If True, the magnitude tplot variable is joined with the component tplot variables.

    Returns
    -------
    str or list[str]
        Names of the magnitude tplot variables.
    """

    # newnames is deprecated in favor of newname
    if newnames is not None:
        logging.info("tvectot: The newnames parameter is deprecated. Please use newname instead.")
        newname = newnames

    tvars = tplot_wildcard_expand(tvars)
    if len(tvars) == 0:
        return

    tvars_type = type(tvars)
    if tvars_type == str:
        tvars = [tvars]

    if suffix is None:
        if join_component:
            suffix = "_tot"
        else:
            suffix='_mag'

    if newname is None:
        newname = [tvar + suffix for tvar in tvars]

    # If newname is a scalar string, zip will iterate over characters
    if type(newname) is not list:
        newname = [newname]

    for tvar, newname_single in zip(tvars, newname):
        _tvectot(tvar, newname_single, join_component)
    
    if tvars_type == str:
        return newname[0]
    else:
        return newname
