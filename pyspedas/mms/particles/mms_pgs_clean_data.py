
import numpy as np

def mms_pgs_clean_data(data_in):
    """

    """

    output = {'data': np.reshape(data_in['data'], [data_in['data'].shape[1], data_in['data'].shape[2]*data_in['data'].shape[3]]),
              'bins': np.reshape(data_in['bins'], [data_in['data'].shape[1], data_in['data'].shape[2]*data_in['data'].shape[3]]),
              'theta': np.reshape(data_in['theta'], [data_in['data'].shape[1], data_in['data'].shape[2]*data_in['data'].shape[3]]),
              'energy': np.reshape(data_in['energy'], [data_in['data'].shape[1], data_in['data'].shape[2]*data_in['data'].shape[3]]),
              'phi': np.reshape(data_in['phi'], [data_in['data'].shape[1], data_in['data'].shape[2]*data_in['data'].shape[3]]),
              'dtheta': np.reshape(data_in['dtheta'], [data_in['data'].shape[1], data_in['data'].shape[2]*data_in['data'].shape[3]]),
              'dphi': np.reshape(data_in['dphi'], [data_in['data'].shape[1], data_in['data'].shape[2]*data_in['data'].shape[3]]),
              'denergy': np.reshape(data_in['denergy'], [data_in['data'].shape[1], data_in['data'].shape[2]*data_in['data'].shape[3]])}

    return output