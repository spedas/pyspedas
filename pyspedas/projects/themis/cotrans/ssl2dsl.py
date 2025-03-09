"""Transform SSL data to DSL data.

Notes:
    Works in a similar way to IDL spedas ssl2gse.pro
"""

import logging
from math import pi
import numpy as np
from copy import deepcopy

from pytplot import get_data, store_data, data_exists, get_coords, set_coords
from pyspedas.projects.themis.state_tools import Spinmodel,get_spinmodel
from pyspedas.projects.themis import autoload_support


def ssl2dsl(name_in: str, name_out: str, isdsltossl: bool = False, ignore_input_coord: bool  = False,
            probe: str=None, use_spinphase_correction: bool=True, eclipse_correction_level: int=0) -> int:
    """Transform ssl to dsl.

    Parameters
    ----------
        name_in: str
            Name of input tplot variable (e.g. 'tha_fgl_ssl')
        name_out: str
            Name of output tplot variable (e.g. 'tha_fgl_dsl')
        isdsltossl: bool
            If 0 (default) then SSL to DSL.
            If 1, then DSL to SSL.
        ignore_input_coord: bool
            if False (default), then fail and return 0 if input coordinate system does not match requested transform
            if True, do not check input coordinate system.
        probe: str
            Usually optional, if the variable name is prefixed with 'tha', 'thb', etc.
            Otherwise, one of ['a','b','c','d','e','f']
        use_spinphase_correction: bool
            If True (default), use spin phase corrections from V03 STATE CDF
            if False, omit this
        eclipse_correction_level: int
            Specify which of the three available spin models to use for this transform
            0: (default) No eclipse correction
            1: Eclipse corrections for waveform data
            2: Eclipse corrections for particles and spin fits (includes additional angular offset)

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
        probe=name_in[2]

    autoload_support(varname=name_in, probe=probe, spinmodel=True)
    spinmodel_obj=get_spinmodel(probe=probe, correction_level=eclipse_correction_level)

    if not ignore_input_coord:
        in_coord=get_coords(name_in)
        if in_coord is None:
            in_coord = "None"
        if isdsltossl and (in_coord.upper() != 'DSL'):
            logging.error("DSL to SSL transform requested, but input coordinate system is " + in_coord)
            return 0
        if not isdsltossl and (in_coord.upper() != 'SSL'):
            logging.error("SSL to DSL transform requested, but input coordinate system is " + in_coord)
            return 0

    # Get data
    result = get_data(name_in)
    in_times = result.times
    data_in = result.y
    metadata = get_data(name_in, metadata=1)
    meta_copy = deepcopy(metadata)

    logging.info('Using spin model to calculate phase versus time...')
    result = spinmodel_obj.interp_t(in_times, use_spinphase_correction=use_spinphase_correction)
    spinmodel_phase = result.spinphase * pi / 180.0
    phase = spinmodel_phase
    d0 = data_in[:, 0]
    d1 = data_in[:, 1]
    d2 = data_in[:, 2]
    out_d2 = d2

    # if isdsltossl == 0:
    #     # despin
    #     out_d0 = d0 * np.cos(phase) - d1 * np.sin(phase)
    #     out_d1 = d0 * np.sin(phase) + d1 * np.cos(phase)
    # else:
    #     # spin
    #     out_d0 = d0 * np.cos(phase) + d1 * np.sin(phase)
    #     out_d1 = -d0 * np.sin(phase) + d1 * np.cos(phase)

    out_coord = 'DSL'
    if isdsltossl:
        # despin
        phase = -1.0*phase
        out_coord = 'SSL'

    out_d0 = d0 * np.cos(phase) - d1 * np.sin(phase)
    out_d1 = d0 * np.sin(phase) + d1 * np.cos(phase)

    dd_out = [out_d0, out_d1, out_d2]
    data_out = np.column_stack(dd_out)
    store_data(name_out, data={'x': in_times, 'y': data_out}, attr_dict=meta_copy)
    set_coords(name_out,out_coord)

    return 1
