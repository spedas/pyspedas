
import math
import numpy as np
from scipy.ndimage import shift
from copy import deepcopy

# use nansum from bottleneck if it's installed, otherwise use the numpy one
try:
    import bottleneck as bn
    nansum = bn.nansum
except ImportError:
    nansum = np.nansum

def erg_pgs_make_theta_spec(data_in, resolution=None, colatitude=False, no_ang_weighting=False):
    """
    Builds theta (latitudinal) spectrogram from simplified particle data structure.

    Input:
        data_in: dict
            Particle data structure

    Parameters:
        resolution: int
            Number of theta points to include in the output

        colatitude: bool
            Flag to specify that data is in co-latitude (0, 180); if this is
            set to False (default), the data are assumed to be (-90, 90)

    Returns:
        Tuple containing: (theta values for y-axis, spectrogram values)

    """

    dr = math.pi/180.

    data = deepcopy(data_in)

    # zero inactive bins to ensure areas with no data are represented as NaN
    data['data'] = np.where(data['bins'] == 0,np.nan,data['data'])
    # get number of theta values
    if resolution is None:
        n_theta = len(np.unique(data['theta']))
    else:
        n_theta = resolution

    if colatitude:
        theta_range = [0, 180]
    else:
        theta_range = [-90, 90]

    theta_grid = np.linspace(theta_range[0], theta_range[1], n_theta+1)

    # init this sample's piece of the spectrogram
    ave = np.zeros(n_theta)

    theta_min = data['theta'] - 0.5*data['dtheta']
    theta_max = data['theta'] + 0.5*data['dtheta']
    theta_array = deepcopy(data['theta'])

    # loop over output grid to sum all active data and bin flags
    for i in range(0, n_theta):
       
        if not no_ang_weighting:
           
            weight = np.zeros(theta_min.shape)

            # data bins whose maximum overlaps the current spectrogram bin
            idx_max = np.argwhere((theta_max > theta_grid[i]) & (theta_max < theta_grid[i+1]))
            if idx_max.size != 0:
                weight[idx_max[:, 0].tolist(), idx_max[:, 1].tolist()] = (np.sin(dr * theta_max[idx_max[:, 0].tolist(), idx_max[:, 1].tolist()]) - np.sin(dr * theta_grid[i])) * data['dphi'][idx_max[:, 0].tolist(), idx_max[:, 1].tolist()]

            # data bins whose minimum overlaps the current spectrogram bin
            idx_min = np.argwhere((theta_min > theta_grid[i]) & (theta_min < theta_grid[i+1]))
            if idx_min.size != 0:
                weight[idx_min[:, 0].tolist(), idx_min[:, 1].tolist()] = (np.sin(dr * theta_grid[i+1]) - np.sin(dr * theta_min[idx_min[:, 0].tolist(), idx_min[:, 1].tolist()])) * data['dphi'][idx_min[:, 0].tolist(), idx_min[:, 1].tolist()]

            # data bins contained within the current spectrogram bin
            max_set = set([tuple(m) for m in idx_max])
            min_set = set([tuple(m) for m in idx_min])
            contained = np.array([m for m in max_set & min_set])
            if contained.size != 0:
                weight[contained[:, 0].tolist(), contained[:, 1].tolist()] = (np.sin(dr * theta_max[contained[:, 0].tolist(), contained[:, 1].tolist()]) - np.sin(dr * theta_min[contained[:, 0].tolist(), contained[:, 1].tolist()])) * data['dphi'][contained[:, 0].tolist(), contained[:, 1].tolist()]

            # data bins that completely cover the current spectrogram bin
            idx_all = np.argwhere((theta_min <= theta_grid[i]) & (theta_max >= theta_grid[i+1]))
            if idx_all.size != 0:
                weight[idx_all[:, 0].tolist(), idx_all[:, 1].tolist()] = (np.sin(dr * theta_grid[i+1]) - np.sin(dr * theta_grid[i])) * data['dphi'][idx_all[:, 0].tolist(), idx_all[:, 1].tolist()]

            # combine indices
            idx = np.concatenate((idx_min, idx_max, idx_all))

            if idx_max.size + idx_min.size + idx_all.size > 0:
                # normalize weighting to selected, active bins
                weight[idx[:, 0].tolist(), idx[:, 1].tolist()] = weight[idx[:, 0].tolist(), idx[:, 1].tolist()] * data['bins'][idx[:, 0].tolist(), idx[:, 1].tolist()]\
                                                                * np.isfinite(data['data'][idx[:, 0].tolist(), idx[:, 1].tolist()])
                weight = weight/nansum(weight)

                # average
                ave[i] = nansum(data['data'][idx[:, 0].tolist(), idx[:, 1].tolist()]*weight[idx[:, 0].tolist(), idx[:, 1].tolist()])
       
        else: # ;;without weighting by dtheta and dphi
            id_array = np.argwhere(np.isfinite(data['data'])\
                     & (data['bins'] == 1)\
                     & (theta_array > theta_grid[i])\
                     & (theta_array < theta_grid[i+1]))

            if len(id_array) > 0:
                ave[i] = np.nanmean(data['data'][id_array[:, 0].tolist(), id_array[:, 1].tolist()])

    # get y axis
    y = (theta_grid+shift(theta_grid, 1))/2.0
    y = y[1:]

    return (y, ave)

