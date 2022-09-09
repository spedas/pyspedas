
import logging
import numpy as np

from pyspedas.utilities.data_exists import data_exists
from pyspedas.cotrans.cotrans import cotrans
from pyspedas.analysis.tnormalize import tnormalize
from pyspedas.analysis.tcrossp import tcrossp
from pyspedas.analysis.tinterpol import tinterpol

from pytplot import get_data, store_data

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def mms_pgs_xgse(mag_temp, pos_temp):
    """
    Generates the 'xgse' transformation matrix
    """
    mag_data = get_data(mag_temp)

    # xaxis of this system is X of the gse system. Z is mag field
    x_axis = np.zeros((len(mag_data.times), 3))
    x_axis[:, 0] = 1

    # create orthonormal basis set
    z_basis = tnormalize(mag_temp, return_data=True)
    y_basis = tcrossp(z_basis, x_axis, return_data=True)
    y_basis = tnormalize(y_basis, return_data=True)
    x_basis = tcrossp(y_basis, z_basis, return_data=True)

    return (x_basis, y_basis, z_basis)


def mms_pgs_phigeo(mag_temp, pos_temp):
    """
    Generates the 'phigeo' transformation matrix
    """
    pos_data = get_data(pos_temp)

    if pos_data is None:
        logging.error('Error with position data')
        return
        
    # transformation to generate other_dim dim for phigeo from thm_fac_matrix_make
    # All the conversions to polar and trig simplifies to this.
    # But the reason the conversion is why this is the conversion that is done, is lost on me.
    # The conversion swaps the x & y components of position, reflects over x=0,z=0 then projects into the xy plane
    pos_conv = np.stack((-pos_data.y[:, 1], pos_data.y[:, 0], np.zeros(len(pos_data.times))))
    pos_conv = np.transpose(pos_conv, [1, 0])
    store_data(pos_temp, data={'x': pos_data.times, 'y': pos_conv})

    # transform into GSE because the particles are in GSE
    cotrans(name_in=pos_temp, name_out=pos_temp, coord_in='gei', coord_out='gse')

    # create orthonormal basis set
    z_basis = tnormalize(mag_temp, return_data=True)
    x_basis = tcrossp(pos_temp, z_basis, return_data=True)
    x_basis = tnormalize(x_basis, return_data=True)
    y_basis = tcrossp(z_basis, x_basis, return_data=True)

    return (x_basis, y_basis, z_basis)


def mms_pgs_mphigeo(mag_temp, pos_temp):
    """
    Generates the 'mphigeo' transformation matrix
    """
    pos_data = get_data(pos_temp)

    if pos_data is None:
        logging.error('Error with position data')
        return

    # the following is heisted from the IDL version
    # transformation to generate other_dim dim for mphigeo from thm_fac_matrix_make
    # All the conversions to polar and trig simplifies to this.  
    # But the reason the conversion is why this is the conversion that is done, is lost on me.
    # The conversion swaps the x & y components of position, reflects over x=0,z=0 then projects into the xy plane
    pos_conv = np.stack((-pos_data.y[:, 1], pos_data.y[:, 0], np.zeros(len(pos_data.times))))
    pos_conv = np.transpose(pos_conv, [1, 0])
    store_data(pos_temp, data={'x': pos_data.times, 'y': pos_conv})

    # transform into GSE because the particles are in GSE
    cotrans(name_in=pos_temp, name_out=pos_temp, coord_in='gei', coord_out='gse')

    # create orthonormal basis set
    z_basis = tnormalize(mag_temp, return_data=True)
    x_basis = tcrossp(z_basis, pos_temp, return_data=True)
    x_basis = tnormalize(x_basis, return_data=True)
    y_basis = tcrossp(z_basis, x_basis, return_data=True)

    return (x_basis, y_basis, z_basis)


def mms_pgs_make_fac(times, mag_tvar_in, pos_tvar_in, fac_type='mphigeo'):
    """
    Generate the field aligned coordinate transformation matrix
    """

    if not data_exists(mag_tvar_in):
        logging.error('Magnetic field variable not found: "' + mag_tvar_in + '"; skipping field-aligned outputs')
        return

    if not data_exists(pos_tvar_in):
        logging.error('Position variable not found: "' + pos_tvar_in + '"; skipping field-aligned outputs')
        return

    valid_types = ['mphigeo', 'phigeo', 'xgse']

    if fac_type not in valid_types:
        logging.error('Invalid FAC type; valid types: "mphigeo", "phigeo", "xgse"')
        return

    cotrans(name_in=pos_tvar_in, name_out=pos_tvar_in, coord_in='gse', coord_out='gei')

    mag_temp = mag_tvar_in + '_pgs_temp'
    pos_temp = pos_tvar_in + '_pgs_temp'

    # first, we need to interpolate the magnetic field and position
    # variables to the time stamps of the particle data (times)
    tinterpol(mag_tvar_in, times, newname=mag_temp)
    tinterpol(pos_tvar_in, times, newname=pos_temp)

    if fac_type == 'mphigeo':
        basis = mms_pgs_mphigeo(mag_temp, pos_temp)
    elif fac_type == 'phigeo':
        basis = mms_pgs_phigeo(mag_temp, pos_temp)
    elif fac_type == 'xgse':
        basis = mms_pgs_xgse(mag_temp, pos_temp)

    fac_output = np.zeros((len(times), 3, 3))
    fac_output[:, 0, :] = basis[0]
    fac_output[:, 1, :] = basis[1]
    fac_output[:, 2, :] = basis[2]

    return fac_output
