"""Transform DSL data to GSE data.

Notes:
    Works in a similar way to IDL spedas dsl2gse.pro
"""

import pytplot
import pyspedas
from pyspedas.cotrans.cotrans_lib import subgei2gse
import numpy as np


def dsl2gse(name_in, spinras, spindec, name_out, isgsetodsl=0):
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

    Returns
    -------
        1 for sucessful completion.

    """
    all_names = pytplot.tplot_names()
    needed_vars = [name_in, spinras, spindec]
    c = [value for value in needed_vars if value in all_names]
    if len(c) < 3:
        print("Variables needed: " + str(needed_vars))
        m = [value for value in needed_vars if value not in c]
        print("Variables missing: " + str(m))
        print("Please load missing variables.")
        return

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
    data_ras = pytplot.get_data(hiras_name)
    data_dec = pytplot.get_data(hidec_name)

    # Make a unit vector that points along the spin axis
    spla = (90.0 - (data_dec[1])) * np.pi/180.0
    splo = data_ras[1] * np.pi/180.0
    # spherical to cartesian
    zscs0 = np.sin(spla) * np.cos(splo)
    zscs1 = np.sin(spla)*np.sin(splo)
    zscs2 = np.cos(spla)
    zscs = np.column_stack((zscs0, zscs1, zscs2))

    # unit vector that points along the spin axis in GSE
    trgse = subgei2gse(data_in[0], zscs)
    zgse = [trgse[:, 0], trgse[:, 1], trgse[:, 2]]
    sun = [1.0, 0.0, 0.0]
    yscs = [zgse[1] * sun[2] - zgse[2] * sun[1],
            zgse[2] * sun[0] - zgse[0] * sun[2],
            zgse[0] * sun[1] - zgse[1] * sun[0]]
    yscsNorm = np.sqrt(yscs[0]**2.0 + yscs[1]**2.0 + yscs[2]**2.0)
    yscs = yscs/yscsNorm
    xscs = [yscs[1] * zgse[2] - yscs[2] * zgse[1],
            yscs[2] * zgse[0] - yscs[0] * zgse[2],
            yscs[0] * zgse[1] - yscs[1] * zgse[0]]

    if isgsetodsl == 0:
        # DSL -> GSE
        dd = data_in[1]
        d0 = dd[:, 0] * xscs[0] + dd[:, 1] * yscs[0] + dd[:, 2] * zgse[0]
        d1 = dd[:, 0] * xscs[1] + dd[:, 1] * yscs[1] + dd[:, 2] * zgse[1]
        d2 = dd[:, 0] * xscs[2] + dd[:, 1] * yscs[2] + dd[:, 2] * zgse[2]

    else:
        # GSE -> DSL
        dd = data_in[1]
        d0 = dd[:, 0] * xscs[0] + dd[:, 1] * xscs[1] + dd[:, 2] * xscs[2]
        d1 = dd[:, 0] * yscs[0] + dd[:, 1] * yscs[1] + dd[:, 2] * yscs[2]
        d2 = dd[:, 0] * zgse[0] + dd[:, 1] * zgse[1] + dd[:, 2] * zgse[2]

    dd_out = [d0, d1, d2]
    data_out = np.column_stack(dd_out)

    pytplot.store_data(name_out, data={'x': data_in[0], 'y': data_out})

    return 1
