import numpy as np


def mms_pgs_split_hpca(data_in):
    """
    Split hpca elevation bins so that dphi == dtheta.
    This should allow the regrid step for FAC spectra to be skipped in mms_part_products.
    """
    clean_data = data_in.copy()
    clean_data['data'] = np.concatenate((clean_data['data'], clean_data['data']), axis=1)
    clean_data['bins'] = np.concatenate((clean_data['bins'], clean_data['bins']), axis=1)
    clean_data['energy'] = np.concatenate((clean_data['energy'], clean_data['energy']), axis=1)
    clean_data['denergy'] = np.concatenate((clean_data['denergy'], clean_data['denergy']), axis=1)
    clean_data['phi'] = np.concatenate((clean_data['phi'], clean_data['phi']), axis=1)
    clean_data['dphi'] = np.concatenate((clean_data['dphi'], clean_data['dphi']), axis=1)
    clean_data['theta'] = np.concatenate((clean_data['theta']+0.25*clean_data['dtheta'], clean_data['theta']-0.25*clean_data['dtheta']), axis=1)
    clean_data['dtheta'] = np.concatenate((clean_data['dtheta']/2.0, clean_data['dtheta']/2.0), axis=1)
    
    return clean_data
