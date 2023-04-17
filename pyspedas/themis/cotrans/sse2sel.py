"""Transformation SSE data to SEL data.
Notes:
    Works in a similar wasy to IDL spedas sse2sel.pro
"""
import logging
import numpy as np
import pytplot
from pyspedas import tnormalize, tcrossp
from pyspedas.cotrans.tvector_rotate import tvector_rotate
from pyspedas.utilities.data_exists import data_exists
from pyspedas.cotrans.cotrans import cotrans
from pyspedas.cotrans.cotrans_get_coord import cotrans_get_coord
from pyspedas.cotrans.cotrans_set_coord import cotrans_set_coord
from pyspedas.analysis.tinterpol import tinterpol
from pyspedas.analysis.deriv_data import deriv_data
from pyspedas.themis.cotrans.gse2sse import gse2sse

def sse2sel(name_in: str, name_sun_pos: str, name_lun_pos: str, 
            name_lun_att_x: str, name_lun_att_z: str, name_out: str, 
            isseltosse: bool = False, variable_type: str = 'Other', ignore_input_coord: bool = False, rotate_only: bool = False) -> int:
    """Transform sse to sel.
    Parameters
    ----------
        name_in: str
            Name of input pytplot variable (e.g. 'tha_state_pos_sse' or 'tha_state_pos_sel')
        name_sun_pos: str
            Name of pytplot variable for sun position in GEI coordinates (e.g.'slp_sun_pos').
        name_lun_pos: str
            Name of pytplot variable for moon position in GEI coordinates (e.g.'slp_lun_pos').
        name_lun_att_x: str
            Name of pytplot variable for SEL X-axis in GEI coordinates (e.g. 'slp_lun_att_x'). 
        name_lun_att_z: str
            Name of pytplot variable for SEL Z-axis in GEI coordinates (e.g. 'slp_lun_att_z').
        name_out: str
            Name of output pytplot variable (e.g. 'tha_fgl_sse')
        isseltosse: bool
            If False (default), then SSE to SEL.
            If True, then SEL to SSE.
        ignore_input_coord: bool
            if False (default), do not check the input coordinate system
            if True, fail and return 0 if input coordinate does not match the requested transform.
        variable_type: str
            A string describing the type of data being transformed.  If value is "pos" or "vel", the appropriate
                offsets (lunar position or velocity) are applied during the transform.  Any other value will be treated
                as equivalent to rotate_only=True.
        rotate_only: bool
            if False (default), assume input variable is a position with units of km, and apply the earth-moon
                offset before rotating to SEL, or after rotating to SSE     #TODO: please check 
            if True, assume the input variable is a velocity or some other quantity that does not need the earth-moon
                translation step
    Returns
    -------
        1 for sucessful completion.
    """
    needed_vars = [name_in, name_sun_pos, name_lun_pos, name_lun_att_x, name_lun_att_z]
    c = [value for value in needed_vars if data_exists(value)]
    if len(c) < 5:
        logging.error("Variables needed: " + str(needed_vars))
        m = [value for value in needed_vars if value not in c]
        logging.error("Variables missing: " + str(m))
        logging.error("Please load missing variables.")
        return 0
   
    if not ignore_input_coord:
        # check input coord
        in_coord = cotrans_get_coord(name_in)
        if in_coord is None:
            in_coord = "None"
        if not isseltosse and (in_coord.lower() != 'sse'):
            logging.error("SSE to SEL transform requested, but input coordinate system is " + in_coord)
            return 0
        if isseltosse and (in_coord.lower() != 'sel'):
            logging.error("SEL to SSE transform requested, but input coordinate system is " + in_coord)
            return 0
        
        # check sun pos coord
        sun_pos_coord = cotrans_get_coord(name_sun_pos)
        if sun_pos_coord is None:
            sun_pos_coord = "None"
        if sun_pos_coord.lower() != 'gse':
            logging.info('Transforming %s to GSE',name_sun_pos)
            sun_pos_gse_name = name_sun_pos+'_gse'
            cotrans(name_in=name_sun_pos,name_out=sun_pos_gse_name,coord_out='GSE')
        else:
            sun_pos_gse_name=name_sun_pos
        # check lun pos coord
        lun_pos_coord = cotrans_get_coord(name_lun_pos)
        if lun_pos_coord is None:
            lun_pos_coord = "None"
        if lun_pos_coord.lower() != 'gse':
            logging.info('Transforming %s to GSE', name_lun_pos)
            lun_pos_gse_name = name_lun_pos + '_gse'
            cotrans(name_in=name_lun_pos, name_out=lun_pos_gse_name, coord_out='GSE')
        else:
            lun_pos_gse_name = name_lun_pos
        # check lun att x coord
        lun_att_x_coord = cotrans_get_coord(name_lun_att_x)
        if lun_att_x_coord is None:
            lun_att_x_coord = "None"
        if lun_att_x_coord.lower() != 'gse':
            logging.info('Transforming %s to GSE', name_lun_att_x)
            lun_att_x_gse_name = name_lun_att_x + '_gse'
            cotrans(name_in=name_lun_att_x, name_out=lun_att_x_gse_name, coord_out='GSE')
        else:
            lun_att_x_gse_name = name_lun_att_x
        # check lun att z coord
        lun_att_z_coord = cotrans_get_coord(name_lun_att_z)
        if lun_att_z_coord is None:
            lun_att_z_coord = "None"
        if lun_att_z_coord.lower() != 'gse':
            logging.info('Transforming %s to GSE', name_lun_att_z)
            lun_att_z_gse_name = name_lun_att_z + '_gse'
            cotrans(name_in=name_lun_att_z, name_out=lun_att_z_gse_name, coord_out='GSE')
        else:
            lun_att_z_gse_name = name_lun_att_z
    else:
        sun_pos_gse_name = name_sun_pos
        lun_pos_gse_name = name_lun_pos
        lun_att_x_gse_name = name_lun_att_x
        lun_att_z_gse_name = name_lun_att_z
    # Make rotation matrix
    sunpos = pytplot.get_data(sun_pos_gse_name)
    sun_pos_dim = sunpos.y.shape

    # X basis vector
    result = gse2sse(lun_att_x_gse_name, sun_pos_gse_name, lun_pos_gse_name, 'sel_x_sse', rotation_only=True)
    sel_x_sse = pytplot.get_data('sel_x_sse')
    x_axis = sel_x_sse.y
    
    # Z basis vector
    result = gse2sse(lun_att_z_gse_name, sun_pos_gse_name, lun_pos_gse_name, 'sel_z_sse', rotation_only=True)
    sel_z_sse = pytplot.get_data('sel_z_sse')
    z_axis = sel_z_sse.y

    # Y basis vector
    tcrossp('sel_z_sse', 'sel_x_sse', newname='sel_y_sse')
    sel_y_sse = pytplot.get_data('sel_y_sse')
    y_axis = sel_y_sse.y

    out_data = np.zeros((sun_pos_dim[0], 3, 3))
    if not isseltosse:
        out_data[:,0,:] = x_axis
        out_data[:,1,:] = y_axis
        out_data[:,2,:] = z_axis
    else:
        # Invert sense of conversion by transposing rotation array
        out_data[:,:,0] = x_axis
        out_data[:,:,1] = y_axis
        out_data[:,:,2] = z_axis
    pytplot.store_data('sel_mat_cotrans', data={'x': sunpos.times, 'y': out_data})
    if not isseltosse:
        """ SSE -> SEL
        """
        tvector_rotate('sel_mat_cotrans',name_in,newname=name_out)
        cotrans_set_coord(name_out,'SEL')
        return 1
    
    else:
        """ SEL -> SSE
        """
        tvector_rotate('sel_mat_cotrans',name_in,newname=name_out)
        cotrans_set_coord(name_out,'SSE')
        return 1