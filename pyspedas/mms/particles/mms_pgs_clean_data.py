
import numpy as np
from scipy.ndimage.interpolation import shift


def mms_pgs_clean_data(data_in):
    """
    Sanitize MMS FPI/HPCA data structures for use with
    mms_part_products; reforms energy by theta by phi to energy by angle
    and calculates delta-energy for each bin
    """

    output = {'charge': data_in['charge'], 'mass': data_in['mass'],
              'data': np.reshape(data_in['data'], [data_in['data'].shape[0], data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'bins': np.reshape(data_in['bins'], [data_in['data'].shape[0], data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'theta': np.reshape(data_in['theta'], [data_in['data'].shape[0], data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'energy': np.reshape(data_in['energy'], [data_in['data'].shape[0], data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'phi': np.reshape(data_in['phi'], [data_in['data'].shape[0], data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'dtheta': np.reshape(data_in['dtheta'], [data_in['data'].shape[0], data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'dphi': np.reshape(data_in['dphi'], [data_in['data'].shape[0], data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'denergy': np.reshape(data_in['denergy'], [data_in['data'].shape[0], data_in['data'].shape[1]*data_in['data'].shape[2]], order='F')}

    de = output['energy'] - shift(output['energy'], [1, 0])
    output['denergy'] = shift((de+shift(de, [1, 0]))/2.0, -1)
    # just have to make a guess at the edges(bottom edge)
    output['denergy'][0, :] = de[1, :]
    # just have to make a guess at the edges(top edge)
    output['denergy'][-1, :] = de[-1, :]

    return output
