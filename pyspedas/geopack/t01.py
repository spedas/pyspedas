import logging
import numpy as np
from pyspedas.tplot_tools import get_data, store_data, get_timespan
from .clean_model_parameters import clean_model_parameters, clean_parmod_data

def get_t01_parameters(pos_var, pdyn=None, dst=None, byimf=None, bzimf=None, g1=None, g2=None, parmod=None, autoload=False):
    """
    Construct an array of  T01 model parameters from individual scalar values, arrays, or tplot variables.

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
    g1: Any
        For the t01 and ts04 models: g1 index value
    g2: Any
        For the t01 and ts04 models: g2 index value
    parmod: Any
        A 10-element or n-by-10 array of parameter values (or equivalent tplot variable) to be replicated or used as-is for model parameters
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
        logging.error('Autoload not yet supported for t01')
        raise ValueError('Autoload not supported')
    if isinstance(parmod, np.ndarray):
        if len(parmod.shape) == 1 and parmod.shape[0] == 10:
            output_parmod[:] = parmod
            return output_parmod
        elif parmod.shape == (ntimes,10):
            output_parmod = parmod
            return output_parmod
        else:
            logging.error('get_t01_parameters: Parmod array not a 10-element or nx10 element array')
            raise ValueError('Parmod array not a 10-element or nx10 element array')
    elif isinstance(parmod, str):
        output_parmod = clean_parmod_data(pos_dat.times, parmod)
        return output_parmod
    if pdyn is not None:
        cleaned_pdyn = clean_model_parameters(pos_dat.times, pdyn)
        output_parmod[:,0] = cleaned_pdyn
    else:
        logging.warning('get_t01_parameters: No pdyn parameter specified, defaulting to 2.0')
        output_parmod[:,0] = 2.0
    if dst is not None:
        cleaned_dst = clean_model_parameters(pos_dat.times, dst)
        output_parmod[:,1] = cleaned_dst
    else:
        logging.warning('get_t01_parameters: No dst parameter specified, defaulting to 2.0')
        output_parmod[:,1] = 2.0
    if byimf is not None:
        cleaned_byimf = clean_model_parameters(pos_dat.times, byimf)
        output_parmod[:,2] = cleaned_byimf
    else:
        logging.warning('get_t01_parameters: No byimf parameter specified, defaulting to 2.0')
        output_parmod[:,2] = 2.0
    if bzimf is not None:
        cleaned_bzimf = clean_model_parameters(pos_dat.times, bzimf)
        output_parmod[:,3] = cleaned_bzimf
    else:
        logging.warning('No bximf parameter specified, defaulting to 2.0')
        output_parmod[:,3] = 2.0
    if g1 is not None:
        cleaned_g1 = clean_model_parameters(pos_dat.times, g1)
        output_parmod[:,4] = cleaned_g1
    else:
        logging.warning('No g1 parameter specified, defaulting to 6.0')
        output_parmod[:,4] = 6.0
    if g2 is not None:
        cleaned_g2 = clean_model_parameters(pos_dat.times, g2)
        output_parmod[:,5] = cleaned_g2
    else:
        logging.warning('No g2 parameter specified, defaulting to 10.0')
        output_parmod[:,5] = 10.0

    return output_parmod


def tt01(pos_var_gsm, pdyn=None, dst=None, byimf=None, bzimf=None, g1=None, g2=None, parmod=None, suffix='', autoload=False):
    """
    Evaluate the T01 field model at the times and positions specified by an input tplot variable.

    This is a tplot wrapper for the functional interface to Sheng Tian's implementation of the Tsyganenko 2001 and IGRF model:

    https://github.com/tsssss/geopack

    Input
    ------
        pos_gsm_tvar: str
            tplot variable containing the position data (km) in GSM coordinates

    Parameters
    -----------
        parmod: string
            A tplot variable containing a 10-element model parameter array (vs. time).  The timestamps should match the input position variable.
            Only the first 6 elements are used::

                (1) solar wind pressure pdyn (nanopascals),
                (2) dst (nanotesla)
                (3) byimf (nanotesla)
                (4) bzimf (nanotesla)
                (5) g1-index
                (6) g2-index  (see Tsyganenko [2001] for an exact definition of these two indices)

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
    parmod = get_t01_parameters(pos_var=pos_var_gsm, pdyn=pdyn, dst=dst, byimf=byimf, bzimf=bzimf, g1=g1, g2=g2, parmod=input_parmod, autoload=autoload)

    for idx, time in enumerate(pos_data.times):
        model = make_model("t01", time, parmod[idx, :])  # does geopack.recalc(time) internally
        bgsm[idx, :] = model.B_gsm(pos_re[idx, :])  # returns IGRF + T01 in GSM

    saved = store_data(pos_var_gsm + '_bt01' + suffix, data={'x': pos_data.times, 'y': bgsm})

    if saved:
        return pos_var_gsm + '_bt01' + suffix
