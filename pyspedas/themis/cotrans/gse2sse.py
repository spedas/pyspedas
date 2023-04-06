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
from pyspedas.cotrans.cotrans import cotrans
from pyspedas.cotrans.cotrans_get_coord import cotrans_get_coord
from pyspedas.cotrans.cotrans_set_coord import cotrans_set_coord
from copy import deepcopy

def gse2sse(name_in: str, name_sun_pos: str, name_lun_pos: str, name_out: str, 
            isssetogse: bool = False, ignore_input_coord: bool = False, rotate_only: bool = False) -> int:

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
        isssetogse: bool
            If False (default), then GSE to SSE.
            If True, then SSE to GSE.
        ignore_input_coord: bool
            if False (default), do not check the input coordinate system
            if True, fail and return 0 if input coordinate does not match the requested transform.
        rotate_only: bool
            if False (default), assume input variable is a position with units of km, and apply the earth-moon
                offset before rotating to SSE, or after rotating to GSE
            if True, assume the input variable is a velocity or some other quantity that does not need the earth-moon
                translation step

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
        # check input coord
        in_coord = cotrans_get_coord(name_in)
        if in_coord is None:
            in_coord = "None"
        if not isssetogse and (in_coord.lower() != 'gse'):
            logging.error("GSE to SSE transform requested, but input coordinate system is " + in_coord)
            return 0
        if isssetogse and (in_coord.lower() != 'sse'):
            logging.error("SSE to GSE transform requested, but input coordinate system is " + in_coord)
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
    else:
        sun_pos_gse_name=name_sun_pos
        lun_pos_gse_name=name_lun_pos

    # Make rotation matrix
    sunpos = pytplot.get_data(sun_pos_gse_name)
    lunpos = pytplot.get_data(lun_pos_gse_name)
    sun_pos_dim = sunpos.y.shape

    # Moon to sun vector = sunpos - lunpos
    lun_sun_vec = sunpos.y - lunpos.y

    # SSE X-axis: unit vector from sun toward moon
    sse_x = tnormalize(lun_sun_vec, return_data=True)
    # SSE Y-axis: ecliptic north unit vector (0,0,1) cross SSE-X
    ecliptic_north = np.repeat(np.array([[0, 0, 1]]), sun_pos_dim[0], axis=0)
    sse_y = tcrossp(ecliptic_north,sse_x, return_data=True)
    # SSE Z-axis: SSE-X cross SSE-Y (not necessarily ecliptic north)
    sse_z = tcrossp(sse_x, sse_y, return_data=True)

    # Make rotation matrix from basis vectors, store in tplot variable

    out_data = np.zeros((sun_pos_dim[0], 3, 3))
    if not isssetogse:
        out_data[:,0,:] = sse_x
        out_data[:,1,:] = sse_y
        out_data[:,2,:] = sse_z
    else:
        # Invert sense of conversion by transposing rotation array
        out_data[:,:,0] = sse_x
        out_data[:,:,1] = sse_y
        out_data[:,:,2] = sse_z

    pytplot.store_data('sse_mat_cotrans', data={'x': sunpos.times, 'y': out_data})

    if not isssetogse:
        """ GSE -> SSE
        """

        if not rotate_only:
            logging.info("Applying earth-moon translation to input variable %s",name_in)
            input_pos = pytplot.get_data(name_in)
            translated_pos = input_pos.y - lunpos.y
            name_trans = name_in + '_trans'
            pytplot.store_data(name_trans,data={'x':input_pos.times, 'y':translated_pos})
            tvector_rotate('sse_mat_cotrans',name_trans,newname=name_out)
        else:
            tvector_rotate('sse_mat_cotrans',name_in,newname=name_out)

        return 1
    
    else:
        """ SSE -> GSE
        """
        if not rotate_only:
            name_trans=name_in + '_trans'
            tvector_rotate('sse_mat_cotrans',name_in,newname=name_trans)
            logging.info("Applying moon-earth translation to rotated variable %s",name_trans)
            trans_data = pytplot.get_data(name_trans)
            earth_data = trans_data.y + lunpos.y
            pytplot.store_data(name_out,data={'x':trans_data.times,'y':earth_data})
        else:
            tvector_rotate('sse_mat_cotrans',name_in,newname=name_out)

        return 1


