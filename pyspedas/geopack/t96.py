import logging
import numpy as np
from pyspedas.tplot_tools import get_data, store_data

def tt96(pos_var_gsm, parmod=None, suffix=''):
    """
    tplot wrapper for the functional interface to Sheng Tian's implementation of the Tsyganenko 96 and IGRF model:

    https://github.com/tsssss/geopack

    Input
    ------
        pos_gsm_tvar: str
            tplot variable containing the position data (km) in GSM coordinates

    Parameters
    -----------
        parmod: str
            A tplot variable containing a 10-element model parameter array (vs. time).  The timestamps
            should match the timestamps in the input position variable. Only the first 4 elements are used::

                (1) solar wind pressure pdyn (nanopascals)
                (2) dst (nanotesla)
                (3) byimf (nanotesla)
                (4) bzimf (nanotesla)

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

    bgsm = np.zeros((len(pos_data.times), 3))

    # convert to Re
    pos_re = pos_data.y/6371.2

    if parmod is not None:
        par = get_data(parmod)

        if par is not None:
            par = par.y
    else:
        logging.error('parmod keyword required.')
        return

    for idx, time in enumerate(pos_data.times):
        model = make_model("t96",time,par[idx,:])
        bgsm[idx,:] = model.B_gsm(pos_re[idx,:])

    saved = store_data(pos_var_gsm + '_bt96' + suffix, data={'x': pos_data.times, 'y': bgsm})

    if saved:
        return pos_var_gsm + '_bt96' + suffix
