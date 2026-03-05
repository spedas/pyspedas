import logging
import numpy as np
from pyspedas.tplot_tools import get_data, store_data, get_timespan
from .clean_model_parameters import clean_model_parameters, clean_parmod_data

def get_ts04_parameters(pos_var, pdyn, dst, byimf, bzimf, w1, w2, w3, w4, w5, w6, parmod, autoload):
    """
    Construct an array of  TS04 model parameters from individual scalar values, arrays, or tplot variables.

    Parameters
    ----------
    pos_var: str
        Input times and positions to be used
    pdyn: Any
        For the t96, t01, and ts04 models: solar wind dynamic pressure in nPa
    dst: Any
        For the t96, t01, and ts04 models: Dst storm time index in nT
    byimf: Any
        For the t96, t01, and ts04 models: Y component of interplanetary magnetic field
    bzimf: Any
        for the t96, t01, and ts04 models: Z component of interplanetary magnetic field
    w1: Any
        For the t01 and ts04 models: w1 index value
    w2: Any
        For the t01 and ts04 models: w2 index value
    w3: Any
        For the ts04 models: w3 index value
    w4: Any
        For the ts04 models: w4 index value
    w5: Any
        For the ts04 models: w5 index value
    w6: Any
        For the ts04 models: w6 index value
    parmod: ndarray
        A 10-element or n-by-10 array of parameter values to be replicated or used as-is for model parameters
    autoload: bool
        If True, ignore any passed parameters and download model parameters from an appropriate source.

    Returns
    -------
    ndarray of floats
        An n by 10, cleaned array of floating point parameters interpolated or replicated to the input timestamps

    """
    pos_trange = get_timespan(pos_var)
    pos_dat = get_data(pos_var)
    ntimes = len(pos_dat.times)
    output_parmod = np.zeros((ntimes,10))

    if autoload:
        logging.error('Autoload not yet supported for ts04')
        raise ValueError('Autoload not supported')
    if isinstance(parmod, np.ndarray):
        if len(parmod.shape) == 1 and parmod.shape[0] == 10:
            output_parmod[:] = parmod
            return output_parmod
        elif parmod.shape == (ntimes,10):
            output_parmod = parmod
            return output_parmod
        else:
            logging.error('get_ts04_parameters: Parmod array not a 10-element or nx10 element array')
            raise ValueError('Parmod array not a 10-element or nx10 element array')
    elif isinstance(parmod, str):
        output_parmod = clean_parmod_data(pos_dat.times, parmod)
        return output_parmod
    if pdyn is not None:
        cleaned_pdyn = clean_model_parameters(pos_dat.times, pdyn)
        output_parmod[:,0] = cleaned_pdyn
    else:
        logging.warning('get_ts04_parameters: No pdyn parameter specified, defaulting to 2.0')
        output_parmod[:,0] = 2.0
    if dst is not None:
        cleaned_dst = clean_model_parameters(pos_dat.times, dst)
        output_parmod[:,1] = cleaned_dst
    else:
        logging.warning('get_ts04_parameters: No dst parameter specified, defaulting to 2.0')
        output_parmod[:,1] = 2.0
    if byimf is not None:
        cleaned_byimf = clean_model_parameters(pos_dat.times, byimf)
        output_parmod[:,2] = cleaned_byimf
    else:
        logging.warning('get_ts04_parameters: No byimf parameter specified, defaulting to 2.0')
        output_parmod[:,2] = 2.0
    if bzimf is not None:
        cleaned_bzimf = clean_model_parameters(pos_dat.times, bzimf)
        output_parmod[:,3] = cleaned_bzimf
    else:
        logging.warning('get_ts04_parameters: No bzimf parameter specified, defaulting to 2.0')
        output_parmod[:,3] = 2.0
    if w1 is not None:
        cleaned_w1 = clean_model_parameters(pos_dat.times, w1)
        output_parmod[:,4] = cleaned_w1
    else:
        logging.warning('get_ts04_parameters: No w1 parameter specified, defaulting to 6.0')
        output_parmod[:,4] = 6.0
    if w2 is not None:
        cleaned_w2 = clean_model_parameters(pos_dat.times, w2)
        output_parmod[:,5] = cleaned_w2
    else:
        logging.warning('get_ts04_parameters: No w2 parameter specified, defaulting to 10.0')
        output_parmod[:,5] = 10.0
    if w3 is not None:
        cleaned_w3 = clean_model_parameters(pos_dat.times, w3)
        output_parmod[:,6] = cleaned_w3
    else:
        logging.warning('get_ts04_parameters: No w3 parameter specified, defaulting to 6.0')
        output_parmod[:,6] = 6.0
    if w4 is not None:
        cleaned_w4 = clean_model_parameters(pos_dat.times, w4)
        output_parmod[:,7] = cleaned_w4
    else:
        logging.warning('get_ts04_parameters: No w4 parameter specified, defaulting to 10.0')
        output_parmod[:,7] = 10.0
    if w5 is not None:
        cleaned_w5 = clean_model_parameters(pos_dat.times, w5)
        output_parmod[:,8] = cleaned_w5
    else:
        logging.warning('get_ts04_parameters: No w5 parameter specified, defaulting to 6.0')
        output_parmod[:,8] = 6.0
    if w6 is not None:
        cleaned_w6 = clean_model_parameters(pos_dat.times, w6)
        output_parmod[:,9] = cleaned_w6
    else:
        logging.warning('get_ts04_parameters: No w6 parameter specified, defaulting to 10.0')
        output_parmod[:,9] = 10.0

    return output_parmod

def tts04(pos_var_gsm, pdyn=None, dst=None, byimf=None, bzimf=None, w1=None, w2=None, w3=None, w4=None, w5=None, w6=None, autoload=False, parmod=None, suffix=''):
    """
    Evaluate the TS04 field model at the times and locations specified by an input tplot variable.

    This is a tplot wrapper for the functional interface to Sheng Tian's implementation of the
    Tsyganenko-Sitnov (2004) storm-time geomagnetic field model

    https://github.com/tsssss/geopack

    Input
    ------
        pos_gsm_tvar: str
            tplot variable containing the position data (km) in GSM coordinates

    Parameters
    -----------
        parmod: str
            A tplot variable containing the model parameters as a 10-element array (vs. time).  The timestamps should match the times in the input position
            variable. The motdl::

                (1) solar wind pressure pdyn (nanopascals),
                (2) dst (nanotesla),
                (3) byimf,
                (4) bzimf (nanotesla)
                (5-10) indices w1 - w6, calculated as time integrals from the beginning of a storm

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

    input_parmod = parmod
    parmod = get_ts04_parameters(pos_var=pos_var_gsm, pdyn=pdyn, dst=dst, byimf=byimf, bzimf=bzimf, w1=w1, w2=w2, w3=w3, w4=w4, w5=w5, w6=w6, parmod=input_parmod, autoload=autoload)

    for idx, time in enumerate(pos_data.times):
        if not np.isfinite(parmod[idx, :]).all():
            # skip if there are any NaNs in the input
            continue
        model = make_model("t04", time, parmod[idx, :])
        bgsm[idx,:] = model.B_gsm(pos_re[idx,:])

    saved = store_data(pos_var_gsm + '_bts04' + suffix, data={'x': pos_data.times, 'y': bgsm})

    if saved:
        return pos_var_gsm + '_bts04' + suffix
