import logging
import numpy as np
from pyspedas.tplot_tools import get_data, store_data

def tt89(pos_var_gsm, kp=None, iopt=None, parmod=None, autoload=True, suffix='', igrf_only=False):
    """
    Evaluate the T89 field model at the times/positions specified by an input tplot variable.

    Parameters
    -----------
    pos_gsm_tvar: str
        tplot variable containing the position data (km) in GSM coordinates.
    iopt: str | int (Optional)
        If present, specifies the ground disturbance level. If iopt is a string, it is interpreted as a
        tplot variable name and interpolated to the times in pos_gsm_tvar.  iopt is related to the Kp index::

            =========  ======== =======  =======  =======  =======  =======
            iopt= 1       2        3        4        5        6      7
            kp=  0,0+  1-,1,1+  2-,2,2+  3-,3,3+  4-,4,4+  5-,5,5+  >= 6-
            =========  ======== =======  =======  =======  =======  =======

    kp: str | float (Optional)
        If present, specifies the Kp index, which will be converted to the equivalent iopt value.
        If kp is a string, it is interpreted as a tplot variable name and interpolated to the times in pos_gsm_tvar.
    parmod: str | array[float] (Optional)
        If present, specifies an  n by 10 elements floating point array of parameters. The first
        element is interpreted as the iopt value, and the rest are ignored.  If parmod is a string,
        it is interpreted as a tplot variable name and interpolated to the times in pos_gsm_tvar.
    autoload: boolean (Optional)
        If True, ignore any other parameters provided, load Kp index data from the Kyoto WDC,
        and convert to iopt values.
    suffix: str (Optional)
        Suffix to append to the tplot output variable
    igrf_only: bool
        If True, only return the IGRF field, without adding the T89 correction.
        This usage is deprecated...please use the tigrf() routine if that's what you need.
        Default: False

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
