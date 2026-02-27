import logging
import numpy as np
from pyspedas.tplot_tools import get_data, store_data

def tt89(pos_var_gsm, iopt=3, suffix='', igrf_only=False):
    """
    tplot wrapper for the functional interface to Sheng Tian's implementation 
    of the Tsyganenko T89 and IGRF model:

    https://github.com/tsssss/geopack

    Input
    ------
        pos_gsm_tvar: str
            tplot variable containing the position data (km) in GSM coordinates

    Parameters
    -----------
        iopt: int
            Specifies the ground disturbance level:

                =========  ======== =======  =======  =======  =======  =======
                iopt= 1       2        3        4        5        6      7
                kp=  0,0+  1-,1,1+  2-,2,2+  3-,3,3+  4-,4,4+  5-,5,5+  &gt =6-
                =========  ======== =======  =======  =======  =======  =======

        suffix: str
            Suffix to append to the tplot output variable

    Returns
    --------
        str
            Name of the tplot variable containing the model data
    """
    from .generic_geopack_adapters import make_model
    pos_data = get_data(pos_var_gsm)

    if pos_data is None:
        logging.error('Variable not found: ' + pos_var_gsm)
        return

    bgsm = np.zeros((len(pos_data.times),3))
    # convert to Re
    pos_re = pos_data.y/6371.2

    parmod = np.zeros(10)
    parmod[0] = iopt
    for idx, time in enumerate(pos_data.times):
        if igrf_only:
            model=make_model("igrf",time,parmod)  # doesn't actually use parmod at all
        else:
            model=make_model("t89",time,parmod)

        bgsm[idx,:] = model.B_gsm(pos_re[idx,:])

    saved = store_data(pos_var_gsm + '_bt89' + suffix, data={'x': pos_data.times, 'y': bgsm})

    if saved:
        return pos_var_gsm + '_bt89' + suffix
