import logging
import numpy as np
from pyspedas.tplot_tools import get_data, store_data, get_timespan, set_coords, set_units
from .clean_model_parameters import clean_model_parameters, clean_parmod_data
from .prepare_pos_variable import prepare_pos_variable
from pyspedas.cotrans_tools.cotrans import cotrans
from .prepare_pos_variable import prepare_pos_variable

def get_t96_parameters(pos_var, pdyn, dst, byimf, bzimf, parmod, autoload):
    """
    Construct an array of  T96 model parameters from individual scalar values, arrays, or tplot variables.

    Parameters
    ----------
    pos_var: str
        Input times and positions to be used
    pdyn: Any
        Solar wind dynamic pressure in nPa
    dst: Any
        Dst index in nT
    byimf: Any
        Y component of interplanetary magnetic field
    bzimf: Any
        Z component of interplanetary magnetic field
    parmod: ndarray
        A 10-element or n-by-10 array of parameter values to be replicated or used as-is for model parameters
    autoload: bool
        If True, ignore any passed parameters and download model parameters from an appropriate source.

    Returns
    -------
    ndarray of floats
        An n by 10, cleaned array of floating point parameters interpolated or replicated to the input timestamps

    """
    from pyspedas.projects.kyoto.load_dst import dst as kyoto_dst
    from pyspedas.projects.omni.load import load as load_omni
    pos_trange = get_timespan(pos_var)
    pos_dat = get_data(pos_var)
    ntimes = len(pos_dat.times)
    output_parmod = np.zeros((ntimes,10))

    if autoload:
        # Pad input time interval by +/- 30 minutes when loading support data
        support_trange = [pos_trange[0] - 3600.0, pos_trange[1] + 3600.0]
        kyoto_dst(trange=support_trange)
        load_omni(trange=support_trange)
        pdyn = 'OMNI_HRO_1min_Pressure'
        byimf = 'OMNI_HRO_1min_BY_GSM'
        bzimf = 'OMNI_HRO_1min_BZ_GSM'
        dst='kyoto_dst'


    if isinstance(parmod, np.ndarray):
        if len(parmod.shape) == 1 and parmod.shape[0] == 10:
            output_parmod[:] = parmod
            return output_parmod
        elif parmod.shape == (ntimes,10):
            output_parmod = parmod
            return output_parmod
        else:
            logging.error('get_t96_parameters: Parmod array not a 10-element or nx10 element array')
            raise ValueError('Parmod array not a 10-element or nx10 element array')
    elif isinstance(parmod, str):
        output_parmod = clean_parmod_data(pos_dat.times, parmod)
        return output_parmod
    if pdyn is not None:
        cleaned_pdyn = clean_model_parameters(pos_dat.times, pdyn)
        output_parmod[:,0] = cleaned_pdyn
    else:
        logging.warning('get_t96_parameters: No pdyn parameter specified, defaulting to 2.0')
        output_parmod[:,0] = 2.0
    if dst is not None:
        cleaned_dst = clean_model_parameters(pos_dat.times, dst)
        output_parmod[:,1] = cleaned_dst
    else:
        logging.warning('get_t96_parameters: No dst parameter specified, defaulting to -30.0')
        output_parmod[:,1] = -30.0
    if byimf is not None:
        cleaned_byimf = clean_model_parameters(pos_dat.times, byimf)
        output_parmod[:,2] = cleaned_byimf
    else:
        logging.warning('get_t96_parameters: No byimf parameter specified, defaulting to 0.0')
        output_parmod[:,2] = 0.0
    if bzimf is not None:
        cleaned_bzimf = clean_model_parameters(pos_dat.times, bzimf)
        output_parmod[:,3] = cleaned_bzimf
    else:
        logging.warning('No bzimf parameter specified, defaulting to -5.0')
        output_parmod[:,3] = -5.0

    return output_parmod


def tt96(pos_var, units_in:str = None, coord_in:str =None, pdyn=None, dst=None, byimf=None, bzimf=None, parmod=None, autoload=False, coord_out:str = 'GSM', suffix=''):
    """
    Evaluate the T96 field model at the times and positions specified by an input tplot variable.

    This is a tplot wrapper for the functional interface to Sheng Tian's implementation of the Tsyganenko 96 and IGRF model:

    https://github.com/tsssss/geopack


    Parameters
    -----------
        pos_var: str
            tplot variable containing the position data (km) in GSM coordinates
        coord_in: str
            (Optional) Coordinate system of input variable, overrides any metadata in pos_var. Must be convertible to GSM.
        units_in: str
            (Optional) Units of input variable, overrides any metadata in pos_var. Valid options: ['km', 'Re']
        parmod: str
            A tplot variable containing a 10-element model parameter array (vs. time).  The timestamps
            should match the timestamps in the input position variable. Only the first 4 elements are used::

                (1) solar wind pressure pdyn (nanopascals)
                (2) dst (nanotesla)
                (3) byimf (nanotesla)
                (4) bzimf (nanotesla)

        coord_out: str
            (Optional) Coordinate system of output variable. Must be convertible from GSM. Default: 'GSM'

        suffix: str
            Suffix to append to the tplot output variable

    Returns
    --------
        str
            Name of the tplot variable containing the model data
    """
    from .generic_geopack_adapters import make_model
    input_gsm_re = prepare_pos_variable(pos_var,coord_in=coord_in, units_in=units_in)
    pos_data = get_data(input_gsm_re)

    if pos_data is None:
        logging.error('Variable not found: ' + pos_var)
        return

    pos_re = pos_data.y

    bgsm = np.zeros((len(pos_data.times),3))

    input_parmod = parmod
    parmod = get_t96_parameters(pos_var=pos_var, pdyn=pdyn, dst=dst, byimf=byimf, bzimf=bzimf, parmod=input_parmod, autoload=autoload)

    for idx, time in enumerate(pos_data.times):
        model = make_model("t96", time, parmod[idx,:])
        bgsm[idx,:] = model.B_gsm(pos_re[idx,:])

    if coord_out.lower() != 'gsm':
        bgsm_out_coord = cotrans(time_in=pos_data.times, data_in=bgsm, coord_in='GSM', coord_out=coord_out)
        bgsm = bgsm_out_coord

    out_name = pos_var + '_bt96' + suffix
    saved = store_data(out_name, data={'x': pos_data.times, 'y': bgsm})

    if saved:
        set_coords(out_name,coord_out)
        set_units(out_name,'nT')
        return out_name
