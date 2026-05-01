
import numpy as np
from copy import deepcopy

def erg_pgs_make_e_spec(data_in):
    """
    Builds energy spectrogram from the particle data structure
    
    Input:
        data_in: dict
            Particle data structure

    Returns:
        Tuple containing: (energy values for the y-axis, spectrogram values)

    """

    data = deepcopy(data_in)

    data_array = deepcopy(data['data'])
    # zero inactive bins to ensure areas with no data are represented as NaN
    data_array = np.where(data['bins'] == 0,0,data['data'])
    ave = data_array.sum(axis=1) / data['bins'].sum(axis=1)

    y = data['energy'][:, 0]

    return (y, ave)
