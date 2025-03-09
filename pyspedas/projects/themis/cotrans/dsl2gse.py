"""Transform DSL data to GSE data.

Notes:
    Works in a similar way to IDL spedas dsl2gse.pro
"""

import logging
import numpy as np
from copy import deepcopy
#import pytplot

import pyspedas
from pyspedas.cotrans_tools.cotrans_lib import subgei2gse
from pytplot import data_exists, del_data, store_data, get_data, set_coords, get_coords
from pyspedas.projects.themis import autoload_support


def dsl2gse(name_in: str, name_out: str, isgsetodsl: bool = False, ignore_input_coord: bool = False,
            probe: str=None, use_spinaxis_corrections: bool=True) -> int:
    """Transform dsl to gse.

    Parameters
    ----------
        name_in: str
            Name of input tplot variable (e.g. 'tha_fgl_dsl')
        name_out: str
            Name of output tplot variable (e.g. 'tha_fgl_gse')
        isgsetodsl: bool
            If False (default) then DSL to GSE.
            If True, then GSE to DSL.
        ignore_input_coord: bool
            if False (default), do not check the input coordinate system
            if True, fail and return 0 if input coordinate does not match the requested transform.
        probe: str
            Usually optional, if the probe can be inferred from the input variable name (e.g. tha_xxx_yyy).
            Otherwise, one of ['a','b','c','d','e','f']
        use_spinaxis_corrections: bool
            If True (default), use spin axis corrections from V03 state CDFs when available.
            If False, use the uncorrected spin axis variables.

    Returns
    -------
        1 for successful completion.

    """
    needed_vars = [name_in]
    c = [value for value in needed_vars if data_exists(value)]
    if len(c) < 1:
        logging.error("Variables needed: " + str(needed_vars))
        m = [value for value in needed_vars if value not in c]
        logging.error("Variables missing: " + str(m))
        logging.error("Please load missing variables.")
        return 0

    if probe is None:
        probe = name_in[2]

    if not ignore_input_coord:
        in_coord = get_coords(name_in)
        if in_coord is None:
            in_coord = "None"
        if isgsetodsl and (in_coord.lower() != 'gse'):
            logging.error("GSE to DSL transform requested, but input coordinate system is " + in_coord)
            return 0
        if not isgsetodsl and (in_coord.lower() != 'dsl'):
            logging.error("DSL to GSE transform requested, but input coordinate system is " + in_coord)
            return 0

    autoload_support(varname=name_in, probe=probe, spinaxis=True)

    if use_spinaxis_corrections:
        spinras = 'th' + probe + '_spinras_corrected'
        spindec = 'th' + probe + '_spindec_corrected'
    else:
        spinras = 'th' + probe + '_spinras'
        spindec = 'th' + probe + '_spindec'

    # Interpolate spinras and spindec
    spinnames_in = [spinras, spindec]
    hiras_name = spinras + '_hires'
    hidec_name = spindec + '_hires'
    hi_names = [hiras_name, hidec_name]

    # If new names exist, delete the variables
    if data_exists(hiras_name):
        del_data(hiras_name)
    if data_exists(hidec_name):
        del_data(hidec_name)

    pyspedas.tinterpol(spinnames_in, name_in, method="linear",
                       newname=hi_names, suffix='')

    # Get data
    data_in = get_data(name_in)
    meta_in = get_data(name_in, metadata=True)
    meta_copy = deepcopy(meta_in)
    data_ras = get_data(hiras_name)
    data_dec = get_data(hidec_name)

    # Make a unit vector that points along the spin axis
    spla = (90.0 - (data_dec[1])) * np.pi / 180.0
    splo = data_ras[1] * np.pi / 180.0
    # spherical to cartesian
    zscs0 = np.sin(spla) * np.cos(splo)
    zscs1 = np.sin(spla) * np.sin(splo)
    zscs2 = np.cos(spla)
    znorm = np.sqrt(zscs0 * zscs0 + zscs1 * zscs1 + zscs2 * zscs2)
    zscs0 = np.divide(zscs0, znorm)
    zscs1 = np.divide(zscs1, znorm)
    zscs2 = np.divide(zscs2, znorm)
    zscs = np.column_stack((zscs0, zscs1, zscs2))

    # unit vector that points along the spin axis in GSE
    trgse = subgei2gse(data_in[0], zscs)
    zgse = trgse
    sun = [1.0, 0.0, 0.0]
    my_y = np.cross(zgse, sun)
    ynorm = np.sqrt(my_y[:, 0] * my_y[:, 0] + my_y[:, 1] * my_y[:, 1] + my_y[:, 2] * my_y[:, 2])
    my_y[:, 0] = np.divide(my_y[:, 0], ynorm)
    my_y[:, 1] = np.divide(my_y[:, 1], ynorm)
    my_y[:, 2] = np.divide(my_y[:, 2], ynorm)
    my_x = np.cross(my_y, zgse)
    xnorm = np.sqrt(my_x[:, 0] * my_x[:, 0] + my_x[:, 1] * my_x[:, 1] + my_x[:, 2] * my_x[:, 2])
    my_x[:, 0] = np.divide(my_x[:, 0], xnorm)
    my_x[:, 1] = np.divide(my_x[:, 1], xnorm)
    my_x[:, 2] = np.divide(my_x[:, 2], xnorm)

    yscs = np.column_stack((zgse[:, 1] * sun[2] - zgse[:, 2] * sun[1],
                            zgse[:, 2] * sun[0] - zgse[:, 0] * sun[2],
                            zgse[:, 0] * sun[1] - zgse[:, 1] * sun[0]))
    # yscs_norm = np.sqrt(yscs[:,0] ** 2.0 + yscs[:,1] ** 2.0 + yscs[:,2] ** 2.0)
    # yscs = np.divide(yscs, yscs_norm)
    xscs = np.column_stack((yscs[:, 1] * zgse[:, 2] - yscs[:, 2] * zgse[:, 1],
                            yscs[:, 2] * zgse[:, 0] - yscs[:, 0] * zgse[:, 2],
                            yscs[:, 0] * zgse[:, 1] - yscs[:, 1] * zgse[:, 0]))

    if not isgsetodsl:
        # DSL -> GSE
        dd = data_in[1]
        d0 = dd[:, 0] * my_x[:, 0] + dd[:, 1] * my_y[:, 0] + dd[:, 2] * zgse[:, 0]
        d1 = dd[:, 0] * my_x[:, 1] + dd[:, 1] * my_y[:, 1] + dd[:, 2] * zgse[:, 1]
        d2 = dd[:, 0] * my_x[:, 2] + dd[:, 1] * my_y[:, 2] + dd[:, 2] * zgse[:, 2]
        out_coord = 'GSE'

    else:
        # GSE -> DSL
        dd = data_in[1]
        d0 = dd[:, 0] * my_x[:, 0] + dd[:, 1] * my_x[:, 1] + dd[:, 2] * my_x[:, 2]
        d1 = dd[:, 0] * my_y[:, 0] + dd[:, 1] * my_y[:, 1] + dd[:, 2] * my_y[:, 2]
        d2 = dd[:, 0] * zgse[:, 0] + dd[:, 1] * zgse[:, 1] + dd[:, 2] * zgse[:, 2]
        out_coord = 'DSL'

    dd_out = [d0, d1, d2]
    data_out = np.column_stack(dd_out)

    store_data(name_out, data={'x': data_in[0], 'y': data_out}, attr_dict=meta_copy)
    set_coords(name_out, out_coord)

    return 1
