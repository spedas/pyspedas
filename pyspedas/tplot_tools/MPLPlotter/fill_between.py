"""Configure filled regions for tplot panels."""

import logging
import numpy as np
from pyspedas.tplot_tools import tplot_wildcard_expand, get_data, join_vec, del_data
from matplotlib import pyplot as plt


def _get_bounds(tvars: list[str], use_envelope: bool = False) -> tuple[np.ndarray,np.ndarray]:
    """
    Takes list of tplot variables, gets the y data, and returns the maximum and minimum bounds as an
    array of size (n,2), where the first column is the minimum and the second column is the maximum. 
    """
    temp_name="fill_between_min_max" 
    join_vec(tvars, newname=temp_name)
    data_concat = get_data(temp_name)
    del_data(temp_name)

    if len(tvars) > 2:
        use_envelope = True
    if use_envelope:
        return (np.min(data_concat.y,axis=1),np.max(data_concat.y,axis=1),data_concat.times)
    else:
        return (data_concat.y[:,0],data_concat.y[:,1],data_concat.times)

# TODO: is fig needed?
def fill_between(
    tvars: str | list[str],
    y_fill_line = None,
    use_envelope: bool = False,
    fill_between_kw: dict = {},
    display:bool=False,
    fig=None,
    axis=None
):
    """
    Fills area of curves using tplot variable y data.
    For two or more tplot variables, fills between the maximum and minimum bounds of y data.
    If y reference value specified, instead fills between all curves and the specified y value.
    For one tplot variable, fills between the tplot y data and a reference y value (defaults to 0 
    if not specified).
    
    Parameters
    ----------
        tvars: str or list of str, required
            Tplot variables which to fill. Expands wildcards.
        fig: Matplotlib figure object
                Use an existing figure to plot in (mainly for recursive calls to render composite variables)
        axis: Matplotlib axes object
            Use an existing set of axes to plot on (mainly for recursive calls to render composite variables)
        
    Returns
    -------
        matplotlib fig object
    """
    # This call resolves wildcard patterns and converts integers to variable names
    tvars = tplot_wildcard_expand(tvars)
    # tvars should now be list[str]
    if len(tvars) == 0:
        logging.warning("fill_between: No matching tplot names were found")
        return

    # If fig and axis have not been specified, define them here:
    #if fig is None and axis is None:
    fig, axis = plt.subplots(nrows=1, sharex=True, gridspec_kw={'height_ratios': [1]}, layout='constrained')
    
    if len(tvars) == 1:
        data_tvar = get_data(tvars[0])
        if y_fill_line is None:
            y_fill_line = 0
        axis.fill_between(data_tvar.times,data_tvar.y,y_fill_line,**fill_between_kw)
    else:
        curve_a, curve_b, data_x = _get_bounds(tvars,use_envelope=use_envelope)
        if y_fill_line is None:
            axis.fill_between(data_x,curve_a,curve_b,**fill_between_kw)
        else:
            axis.fill_between(data_x,curve_a,y_fill_line,**fill_between_kw)
            axis.fill_between(data_x,curve_b,y_fill_line,**fill_between_kw)
    
    if display:
        plt.show()

if __name__ == "__main__": # for testing, remove when done
    import pyspedas
    pyspedas.store_data("Variable1", data={'x':[1,2,3,4,5,6], 'y':[1,2,2,-1,-3,1]})
    #pyspedas.store_data("Variable2", data={'x':[1,2,3,4,5,6], 'y':[5,-4,3,2,1,0]})
    #fill_between("Variable*", display=True) 
    #fill_between("Variable1", display=True) 
    #fill_between("Variable1", y_fill_line = -1, display=True) 
    
    # different x values
    pyspedas.store_data("Variable2", data={'x':[2,3,4,5,6,7], 'y':[5,-4,3,2,1,0]})
    #fill_between("Variable*", display=True) 
    fill_between("Variable*", y_fill_line = -1, display=True) 