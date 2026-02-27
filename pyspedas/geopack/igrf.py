import logging
import numpy as np
from pyspedas.tplot_tools import get_data, store_data
from .generic_geopack_adapters import make_model


def tigrf(pos_var_gsm, suffix=''):
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
    suffix: str
        Suffix to append to the tplot output variable

    Returns
    --------
    str
        Name of the tplot variable containing the model data
    """
    pos_data = get_data(pos_var_gsm)

    if pos_data is None:
        logging.error('Variable not found: ' + pos_var_gsm)
        return

    bgsm = np.zeros((len(pos_data.times), 3))

    # convert to Re
    pos_re = pos_data.y/6371.2
    dummy_parmod=np.zeros(10)

    for idx, time in enumerate(pos_data.times):
        model = make_model("igrf",time,dummy_parmod)
        bgsm[idx,:] = model.B_gsm(pos_re[idx,:])

    saved = store_data(pos_var_gsm + '_btigrf' + suffix, data={'x': pos_data.times, 'y': bgsm})

    if saved:
        return pos_var_gsm + '_igrf' + suffix
