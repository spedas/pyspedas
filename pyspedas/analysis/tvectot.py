from numpy import linalg
from pytplot import split_vec, join_vec, get_data, store_data, options
from typing import Union, List
import logging

def _tvectot(tvar: str, new_name: str, join_component: bool):
    data = get_data(tvar)
    md = get_data(tvar,metadata=True)
    new_data = linalg.norm(data.y, axis=1)
    store_data(new_name, data={'x':data.times,'y':new_data},attr_dict=md)
    
    if join_component:
        join_vec(split_vec(tvar)+[new_name], newname=new_name)
        options(new_name, 'legend_names', ['x', 'y', 'z', 'Magnitude'])
    else:
        options(new_name, 'legend_names', 'Magnitude')
    return new_name

def tvectot(tvars: Union[str, List[str]], newname=None, newnames: Union[str, List[str]] = None, suffix="_mag", join_component=False) -> Union[str , List[str]]:
    """
    Computes the magnitude of a vector time series.

    Parameters
    ----------
    - tvars : Names of the tplot variables.
    - newnames: (Deprecated) Names for the resultant magnitude tplot variables. If not provided, it appends the suffix to `tvars`.
    - newname: Names for the resultant magnitude tplot variables. If not provided, it appends the suffix to `tvars`.
    - suffix: The suffix to append to tensor_names to form new_names if new_names is not provided.
    - join_component: If True, the magnitude tplot variable is joined with the component tplot variables.

    Returns
    -------
    Names of the magnitude tplot variables.
    """

    # newnames is deprecated in favor of newname
    if newnames is not None:
        logging.info("tvectot: The newnames parameter is deprecated. Please use newname instead.")
        newname = newnames

    tvars_type = type(tvars)
    if tvars_type == str:
        tvars = [tvars]
    if join_vec:
        suffix = "_tot"

    if newname is None:
        newname = [tvar + suffix for tvar in tvars]

    for tvar, newname_single in zip(tvars, newname):
        _tvectot(tvar, newname_single, join_component)
    
    if tvars_type == str:
        return newname[0]
    else:
        return newname
