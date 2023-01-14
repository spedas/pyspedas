"""Transform DSL data to GSE data.

Notes:
    Works in a similar way to IDL spedas dsl2gse.pro
"""

import numpy as np
import pytplot

import pyspedas
from pyspedas.cotrans.cotrans_lib import subgei2gse
from pyspedas.utilities.data_exists import data_exists
from pyspedas.cotrans.cotrans_get_coord import cotrans_get_coord
from pyspedas.cotrans.cotrans_set_coord import cotrans_set_coord
from copy import deepcopy


def dsl2gse(name_in: str, spinras: str, spindec: str, name_out: str, isgsetodsl: bool = False,
            ignore_input_coord: bool = True) -> int:
    """Transform dsl to gse.

    Parameters
    ----------
        name_in: str
            Name of input pytplot variable (eg. 'tha_fgl_dsl')
        spinras: str
            Name of pytplot variable for spin (eg.'tha_spinras').
        spindec: str
            Name of pytplot variable for spin (eg.'tha_spinras').
        name_out: str
            Name of output pytplot variable (eg. 'tha_fgl_gse')
        isgsetodsl: bool
            If 0 (default) then DSL to GSE.
            If 1, then GSE to DSL.
        ignore_input_coord: bool
            if 0 (default), do not check the input coordinate system
            if 1, fail and return 0 if input coordinate does not match the requested transform.

    Returns
    -------
        1 for sucessful completion.

    """
    needed_vars = [name_in, spinras, spindec]
    c = [value for value in needed_vars if data_exists(value)]
    if len(c) < 3:
        print("Variables needed: " + str(needed_vars))
        m = [value for value in needed_vars if value not in c]
        print("Variables missing: " + str(m))
        print("Please load missing variables.")
        return 0

    if ignore_input_coord is False:
        in_coord = cotrans_get_coord(name_in)
        if in_coord is None:
            in_coord = "None"
        if (isgsetodsl is True) and (in_coord.lower() != 'gse'):
            print("GSE to DSL transform requested, but input coordinate system is " + in_coord)
            return 0
        if (isgsetodsl is False) and (in_coord.lower() != 'dsl'):
            print("DSL to GSE transform requested, but input coordinate system is " + in_coord)
            return 0

    # Interpolate spinras and spindec
    spinnames_in = [spinras, spindec]
    hiras_name = spinras + '_hires'
    hidec_name = spindec + '_hires'
    hi_names = [hiras_name, hidec_name]

    # If new names exist, delete the variables
    if hiras_name in pytplot.tplot_names():
        pytplot.del_data(hiras_name)
    if hidec_name in pytplot.tplot_names():
        pytplot.del_data(hidec_name)

    pyspedas.tinterpol(spinnames_in, name_in, method="linear",
                       newname=hi_names, suffix='')

    # Get data
    data_in = pytplot.get_data(name_in)
    meta_in = pytplot.get_data(name_in, metadata=True)
    meta_copy = deepcopy(meta_in)
    data_ras = pytplot.get_data(hiras_name)
    data_dec = pytplot.get_data(hidec_name)

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

    if isgsetodsl == 0:
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

    pytplot.store_data(name_out, data={'x': data_in[0], 'y': data_out}, attr_dict=meta_copy)
    cotrans_set_coord(name_out, out_coord)

    return 1
