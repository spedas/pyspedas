import logging
import numpy as np
from pyspedas.projects.omni.load import load
from pyspedas.utilities.xdegap import xdegap
from pytplot import get_data

def solarwind_load(trange, level='hro2', min5=False):
    """
    Loads solar wind data from OMNI. 

    Parameters
    ----------
    trange : list of float
        Time range of data to be loaded.
    level : str, optional
        Data level for OMNI data; valid options: 'hro', 'hro2'. 
        Default is 'hro2'.
    min5 : bool, optional
        Flag indicating whether to load 1-minute or 5-minute data. Default is False (1-minute data).

    Returns
    -------
    Numpy array of solar wind data with shape (N, 3), where N is the number of time points
    and the columns are time, pressure, and Bz GSM.

    """

    if min5:
        datatype = '5min'
    else:
        datatype = '1min'
    
    omni_vars = load(trange=trange, level=level, datatype=datatype)
    
    if omni_vars is None or 'BZ_GSM' not in omni_vars or 'Pressure' not in omni_vars:
        logging.error("Solar Wind load error: OMNI data not found.")
        return None
    
    bzgsm = get_data('BZ_GSM')
    dp = get_data('Pressure')
    times = bzgsm.times

    # Remove NaN values from the data, replacing them with the average of surrounding values
    bnon = xdegap(bzgsm.y)
    dpnon= xdegap(dp.y)
    
    # Order matches IDL code. It is different from mms_cotrans_lmn.py
    return np.array([times, dpnon, bnon]).T
