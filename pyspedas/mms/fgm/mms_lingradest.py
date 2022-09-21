import logging
import numpy as np
from pyspedas import tinterpol
from pyspedas.analysis.lingradest import  lingradest
from pytplot import get_data, store_data, options, join_vec


def mms_lingradest(fields=None, positions=None, suffix=''):
    """

    """

    if fields is None or positions is None:
        logging.error('B-field and spacecraft position keywords required.')
        return

    # interpolate the magnetic field data all onto the same timeline (MMS1):
    # should be in GSE coordinates
    tinterpol(fields[1], fields[0], newname=fields[1] + '_i')
    tinterpol(fields[2], fields[0], newname=fields[2] + '_i')
    tinterpol(fields[3], fields[0], newname=fields[3] + '_i')

    # interpolate the definitive ephemeris onto the magnetic field timeseries
    # should be in GSE coordinates
    tinterpol(positions[0], fields[0], newname=positions[0] + '_i')
    tinterpol(positions[1], fields[0], newname=positions[1] + '_i')
    tinterpol(positions[2], fields[0], newname=positions[2] + '_i')
    tinterpol(positions[3], fields[0], newname=positions[3] + '_i')

    B1 = get_data(fields[0])
    B2 = get_data(fields[1] + '_i')
    B3 = get_data(fields[2] + '_i')
    B4 = get_data(fields[3] + '_i')

    Bx1 = B1.y[:, 0]
    By1 = B1.y[:, 1]
    Bz1 = B1.y[:, 2]

    Bx2 = B2.y[:, 0]
    By2 = B2.y[:, 1]
    Bz2 = B2.y[:, 2]

    Bx3 = B3.y[:, 0]
    By3 = B3.y[:, 1]
    Bz3 = B3.y[:, 2]

    Bx4 = B4.y[:, 0]
    By4 = B4.y[:, 1]
    Bz4 = B4.y[:, 2]

    R1 = get_data(positions[0] + '_i')
    R2 = get_data(positions[1] + '_i')
    R3 = get_data(positions[2] + '_i')
    R4 = get_data(positions[3] + '_i')

    # start the calculation
    output = lingradest(Bx1, Bx2, Bx3, Bx4,
                        By1, By2, By3, By4,
                        Bz1, Bz2, Bz3, Bz4,
                        R1.y, R2.y, R3.y, R4.y)
    # end of the calculations

    # store the results
    store_data('Bt' + suffix, data={'x': B1.times, 'y': output['Bbc']})
    store_data('Bx' + suffix, data={'x': B1.times, 'y': output['Bxbc']})
    store_data('By' + suffix, data={'x': B1.times, 'y': output['Bybc']})
    store_data('Bz' + suffix, data={'x': B1.times, 'y': output['Bzbc']})

    join_vec(['Bt'+suffix, 'Bx'+suffix, 'By'+suffix, 'Bz'+suffix], new_tvar='Bbc' + suffix)

    # B-field gradients
    store_data('gradBx' + suffix, data={'x': B1.times, 'y': output['LGBx']})
    store_data('gradBy' + suffix, data={'x': B1.times, 'y': output['LGBy']})
    store_data('gradBz' + suffix, data={'x': B1.times, 'y': output['LGBz']})

    CB = np.sqrt(output['LCxB']**2 + output['LCyB']**2 + output['LCzB']**2)

    # in nT/1000km
    store_data('absCB' + suffix, data={'x': B1.times, 'y': CB})
    store_data('CxB' + suffix, data={'x': B1.times, 'y': output['LCxB']})
    store_data('CyB' + suffix, data={'x': B1.times, 'y': output['LCyB']})
    store_data('CzB' + suffix, data={'x': B1.times, 'y': output['LCzB']})

    store_data('divB_nT/1000km' + suffix, data={'x': B1.times, 'y': output['LD']})

    join_vec(['absCB'+suffix, 'CxB'+suffix, 'CyB'+suffix, 'CzB'+suffix], new_tvar='curlB_nT/1000km' + suffix)

    # jx in nA/m^2
    store_data('jx' + suffix, data={'x': B1.times, 'y': 0.8 * output['LCxB']})
    # jy in nA/m^2
    store_data('jy' + suffix, data={'x': B1.times, 'y': 0.8 * output['LCyB']})
    # jz in nA/m^2
    store_data('jz' + suffix, data={'x': B1.times, 'y': 0.8 * output['LCzB']})

    join_vec(['jx'+suffix, 'jy'+suffix, 'jz'+suffix], new_tvar='jtotal' + suffix)

    store_data('curvx' + suffix, data={'x': B1.times, 'y': output['curv_x_B']})
    store_data('curvy' + suffix, data={'x': B1.times, 'y': output['curv_y_B']})
    store_data('curvz' + suffix, data={'x': B1.times, 'y': output['curv_z_B']})

    join_vec(['curvx'+suffix,  'curvy'+suffix,  'curvz'+suffix], new_tvar='curvB' + suffix)

    store_data('Rc_1000km' + suffix, data={'x': B1.times, 'y': output['RcurvB']})