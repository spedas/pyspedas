import logging
import numpy as np
from pyspedas.tplot_tools import get_data, store_data, get_timespan
from .clean_model_parameters import clean_model_parameters, clean_parmod_data
from .kp2iopt import kp2iopt

def get_t89_parameters(pos_var, kp, iopt, parmod, autoload, igrf_only):
    """
    Construct an array of T89 model parameters from individual scalar values, arrays, or tplot variables.

    Parameters
    ----------
    pos_var: str
        Input times and positions to be used
    kp: Any
        The Kp parameter to use for the t89 model (scalar, array, or tplot variable name)
    iopt: Any
        The model parameter to use for the t89 model (scalar, array, or tplot variable name)
    igrf_only: bool
        For the t89 model, if true, only include the IGRF standard field.
    parmod: Any
        A 10-element or n-by-10 array of parameter values (or an equivalent tplot variable) to be replicated or used as-is for model parameters
    autoload: bool
        If True, ignore any passed parameters and download model parameters from an appropriate source.

    Returns
    -------
    ndarray of floats
        An n by 10, cleaned array of floating point parameters interpolated or replicated to the input timestamps

    """
    from pyspedas.projects.noaa.noaa_load_kp import noaa_load_kp
    pos_trange = get_timespan(pos_var)
    pos_dat = get_data(pos_var)
    ntimes = len(pos_dat.times)
    output_parmod = np.zeros((ntimes,10))

    if autoload:
        # Pad the input time range by 30 minutes on each side for loading support data
        support_trange = [pos_trange[0] - 1800.0, pos_trange[1] + 1800]
        noaa_load_kp(trange=support_trange)
        kp='Kp'
    if isinstance(parmod, np.ndarray):
        if len(parmod.shape) == 1 and parmod.shape[0] == 10:
            output_parmod[:] = parmod
            return output_parmod
        elif parmod.shape == (ntimes,10):
            output_parmod = parmod
            return output_parmod
        else:
            logging.error('Parmod array not a 10-element or nx10 element array')
            raise ValueError('Parmod array not a 10-element or nx10 element array')
    elif isinstance(parmod, str):
        output_parmod = clean_parmod_data(pos_dat.times, parmod, method="nearest")
        return output_parmod
    if igrf_only:
        output_parmod[:,:] = 0.0
        return output_parmod
    if iopt is not None:
        cleaned_iopt = clean_model_parameters(pos_dat.times, iopt, method="nearest")
        output_parmod[:,0] = cleaned_iopt
        return output_parmod
    if kp is not None:
        cleaned_kp = clean_model_parameters(pos_dat.times, kp, method="nearest")
        cleaned_iopt = kp2iopt(cleaned_kp)
        output_parmod[:,0] = cleaned_iopt
    else:
        logging.warning('get_t89_parameters: No kp, iopt, or parmod data provided, defaulting to iopt=3')
        output_parmod[:,0] = 3

    return output_parmod

def tt89(pos_var_gsm, kp=None, iopt=None, parmod=None, autoload=False, suffix='', igrf_only=False):
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

    input_parmod = parmod
    parmod = get_t89_parameters(pos_var=pos_var_gsm, kp=kp, iopt=iopt, parmod=input_parmod, igrf_only=igrf_only, autoload=autoload)
    for idx, time in enumerate(pos_data.times):
        if igrf_only:
            model=make_model("igrf",time,parmod[idx,:])  # doesn't actually use parmod at all
        else:
            model=make_model("t89",time,parmod[idx,:])

        bgsm[idx,:] = model.B_gsm(pos_re[idx,:])

    saved = store_data(pos_var_gsm + '_bt89' + suffix, data={'x': pos_data.times, 'y': bgsm})

    if saved:
        return pos_var_gsm + '_bt89' + suffix
