import logging
import numpy as np
from pyspedas.tplot_tools import get_data, store_data, get_coords, set_coords, get_units, set_units
from pyspedas.cotrans_tools.cotrans import cotrans
from .generic_geopack_adapters import make_model
from .prepare_pos_variable import prepare_pos_variable


def tigrf(pos_var, units_in:str = None, coord_in:str =None, coord_out:str = 'GSM', suffix=''):
    """
    tplot wrapper for the functional interface to Sheng Tian's implementation 
    of the Tsyganenko T89 and IGRF model:

    https://github.com/tsssss/geopack

    Parameters
    -----------
        pos_var: str
            tplot variable containing the position data.
        coord_in: str
            (Optional) Coordinate system of input variable, overrides any metadata in pos_var. Must be convertible to GSM.
        units_in: str
            (Optional) Units of input variable, overrides any metadata in pos_var. Valid options: ['km', 'Re']
        coord_out: str
            (Optional) Coordinate system of output variable. Must be convertible from GSM. Default: 'GSM'
        suffix: str
            Suffix to append to the tplot output variable

    Returns
    --------
    str
        Name of the tplot variable containing the model data
    """
    input_gsm_re = prepare_pos_variable(pos_var,coord_in=coord_in, units_in=units_in)
    pos_data = get_data(input_gsm_re)
    pos_re = pos_data.y
    bgsm = np.zeros((len(pos_data.times), 3))

    dummy_parmod=np.zeros(10)

    for idx, time in enumerate(pos_data.times):
        model = make_model("igrf",time,dummy_parmod)
        bgsm[idx,:] = model.B_gsm(pos_re[idx,:])

    if coord_out.lower() != 'gsm':
        bgsm_out_coord = cotrans(time_in=pos_data.times, data_in=bgsm, coord_in='GSM', coord_out=coord_out)
        bgsm = bgsm_out_coord

    out_name = pos_var + '_btigrf' + suffix
    saved = store_data(out_name, data={'x': pos_data.times, 'y': bgsm})

    if saved:
        set_coords(out_name,coord_out)
        set_units(out_name,'nT')
        return out_name
