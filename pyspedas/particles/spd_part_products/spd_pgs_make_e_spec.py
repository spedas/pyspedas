
import numpy as np

# use nanmean from bottleneck if it's installed, otherwise use the numpy one
try:
    import bottleneck as bn
    nanmean = bn.nanmean
except ImportError:
    nanmean = np.nanmean


def spd_pgs_make_e_spec(data_in):
    """
    Builds energy spectrogram from the particle data structure
    
    Parameters
    ----------
        data_in: dict
            Particle data structure

    Returns
    -------
    tuple
        Tuple containing: (energy values for the y-axis, spectrogram values)

    """

    data = data_in.copy()

    # zero inactive bins to ensure areas with no data are represented as NaN
    zero_bins = np.argwhere(data['bins'] == 0)
    if zero_bins.size != 0:
        for item in zero_bins:
            data['data'][item[0], item[1]] = 0.0

    ave = nanmean(data['data'], axis=1)

    y = data['energy'][:, 0]

    return (y, ave)
