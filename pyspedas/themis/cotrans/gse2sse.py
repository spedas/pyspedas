"""Transform GSE data to SSE data.

Notes:
    Works in a similar way to IDL spedas dsl2gse.pro
"""

import logging
import numpy as np
import pytplot

import pyspedas
from pyspedas import tnormalize, tcrossp
from pyspedas.cotrans.tvector_rotate import tvector_rotate
from pyspedas.cotrans.cotrans_lib import subgei2gse
from pyspedas.utilities.data_exists import data_exists
from pyspedas.cotrans.cotrans_get_coord import cotrans_get_coord
from pyspedas.cotrans.cotrans_set_coord import cotrans_set_coord
from copy import deepcopy

def gse2sse(name_in: str, name_sun_pos: str, name_lun_pos: str, name_out: str, 
            isgsetosse: bool = False, ignore_input_coord: bool = False) -> int:

    """Transform gse to sse.

    Parameters
    ----------
        name_in: str
            Name of input pytplot variable (e.g. 'tha_fgl_dsl')
        name_sun_pos: str
            Name of pytplot variable for sun position (e.g.'slp_sun_pos').
        name_lun_pos: str
            Name of pytplot variable for spin (e.g.'slp_lun_pos').
        name_out: str
            Name of output pytplot variable (e.g. 'tha_fgl_sse')
        isgsetosse: bool
            If False, then SSE to GSE.
            If True (default), then GSE to SSE.
        ignore_input_coord: bool
            if False (default), do not check the input coordinate system
            if True, fail and return 0 if input coordinate does not match the requested transform.

    Returns
    -------
        1 for sucessful completion.
    """

    needed_vars = [name_in, name_sun_pos, name_lun_pos]
    c = [value for value in needed_vars if data_exists(value)]
    if len(c) < 3:
        logging.error("Variables needed: " + str(needed_vars))
        m = [value for value in needed_vars if value not in c]
        logging.error("Variables missing: " + str(m))
        logging.error("Please load missing variables.")
        return 0
   
    if not ignore_input_coord:
        # checkt input coord 
        in_coord = cotrans_get_coord(name_in)
        if in_coord is None:
            in_coord = "None"
        if isgsetosse and (in_coord.lower() != 'gse'):
            logging.error("GSE to SSE transform requested, but input coordinate system is " + in_coord)
            return 0
        if not isgsetosse and (in_coord.lower() != 'sse'):
            logging.error("SSE to GSE transform requested, but input coordinate system is " + in_coord)
            return 0
        
        # checkt sun pos coord 
        sun_pos_coord = cotrans_get_coord(name_sun_pos)
        if sun_pos_coord is None:
            sun_pos_coord = "None"
        if isgsetosse and (sun_pos_coord.lower() != 'gse'):
            logging.error("GSE to SSE transform requested, but sun pos coordinate system is " + sun_pos_coord)
            return 0
        if not isgsetosse and (sun_pos_coord.lower() != 'sse'):
            logging.error("SSE to GSE transform requested, but sun pos coordinate system is " + sun_pos_coord)
            return 0
        
        # checkt lun pos coord 
        lun_pos_coord = cotrans_get_coord(name_lun_pos)
        if lun_pos_coord is None:
            lun_pos_coord = "None"
        if isgsetosse and (lun_pos_coord.lower() != 'gse'):
            logging.error("GSE to SSE transform requested, but lun pos coordinate system is " + lun_pos_coord)
            return 0
        if not isgsetosse and (lun_pos_coord.lower() != 'sse'):
            logging.error("SSE to GSE transform requested, but lun pos coordinate system is " + lun_pos_coord)
            return 0

    if isgsetosse:   
        """ GSE -> SSE
        """ 
        sun_pos = pytplot.get_data(name_sun_pos)
        lun_pos = pytplot.get_data(name_lun_pos)

        # translation of sse_matrix_make.pro
        sun_pos_dim = sun_pos.y.shape
        out_data = np.zeros((sun_pos_dim[0], 3, 3))

        # X basis vector
        x_axis = tnormalize(sun_pos.y -  lun_pos.y, return_data = True)
        out_data[:,0,:] = x_axis

        # Y basis vector
        ecliptic_north = np.repeat(np.array([[0, 0, 1]]), sun_pos_dim[0], axis=0)
        y_axis = tcrossp(ecliptic_north, x_axis, return_data = True)
        out_data[:,1,:] = y_axis

        # Z basis vector
        z_axis = tcrossp(x_axis, y_axis, return_data = True)

        pytplot.store_data('sse_mat_cotrans', data={'x': sun_pos.times, 'y': out_data})

        # rotate
        tvector_rotate('sse_mat_cotrans',name_in, newname = name_out)
        
        return 1
    
    else:
        """ GSE -> SSE
        """ 
        pass


