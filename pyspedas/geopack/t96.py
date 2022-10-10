import logging
import numpy as np
from pytplot import get_data, store_data
from geopack import geopack, t96


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
        parmod: ndarray
            10-element array (vs. time), but only the first 4 elements are used
                (1) solar wind pressure pdyn (nanopascals)
                (2) dst (nanotesla)
                (3) byimf (nanotesla)
                (4) bzimf (nanotesla)

        suffix: str
            Suffix to append to the tplot output variable

    Returns
    --------
        Name of the tplot variable containing the model data
    """
    pos_data = get_data(pos_var_gsm)

    if pos_data is None:
        logging.error('Variable not found: ' + pos_var_gsm)
        return

    b0gsm = np.zeros((len(pos_data.times), 3))
    dbgsm = np.zeros((len(pos_data.times), 3))

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
        tilt = geopack.recalc(time)

        # dipole B in GSM
        b0gsm[idx, 0], b0gsm[idx, 1], b0gsm[idx, 2] = geopack.dip(pos_re[idx, 0], pos_re[idx, 1], pos_re[idx, 2])

        # T96 dB in GSM
        dbgsm[idx, 0], dbgsm[idx, 1], dbgsm[idx, 2] = t96.t96(par[idx, :], tilt, pos_re[idx, 0], pos_re[idx, 1], pos_re[idx, 2])

    bgsm = b0gsm + dbgsm

    saved = store_data(pos_var_gsm + '_bt96' + suffix, data={'x': pos_data.times, 'y': bgsm})

    if saved:
        return pos_var_gsm + '_bt96' + suffix
