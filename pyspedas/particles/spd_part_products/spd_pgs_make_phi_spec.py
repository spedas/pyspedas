
import math
import numpy as np
from scipy.ndimage.interpolation import shift

# use nansum from bottleneck if it's installed, otherwise use the numpy one
try:
    import bottleneck as bn
    nansum = bn.nansum
except ImportError:
    nansum = np.nansum

def spd_pgs_make_phi_spec(data_in, resolution=None):
    """
    Builds phi (longitudinal) spectrogram from the particle data structure

    Input:
        data_in: dict
            Particle data structure

    Parameters:
        resolution: int
            Number of phi bins in the output

    Returns:
        Tuple containing: (phi values for y-axis, spectrogram values)
    """

    dr = math.pi/180.

    data = data_in.copy()

    # zero inactive bins to ensure areas with no data are represented as NaN
    zero_bins = np.argwhere(data['bins'] == 0)
    if zero_bins.size != 0:
        for item in zero_bins:
            data['data'][item[0], item[1]] = 0.0

    # get number of phi values
    if resolution is None:
        # method taken from the IDL code
        idx = np.nanargmin(np.abs((data['theta'][0, :])))
        n_phi = len(np.argwhere(data['theta'][0, :] == np.abs((data['theta'][0, :]))[idx]))
    else:
        n_phi = resolution

    # init this sample's piece of the spectrogram
    ave = np.zeros(n_phi)

    # form grid specifying the spectrogram's phi bins
    phi_grid = np.linspace(0, 360.0, n_phi+1)
    phi_grid_width = np.nanmedian(phi_grid - shift(phi_grid, 1))

    # get min/max of all data bins
    # keep phi in [0, 360]
    phi_min = (data['phi'] - 0.5*data['dphi']) 
    phi_max = (data['phi'] + 0.5*data['dphi']) % 360.0

    # algorithm below assumes maximums at 360 not wrapped to 0
    phi_max[phi_max == 0] = 360.0

    # keep phi in [0, 360]
    phi_min[phi_min < 0] = phi_min[phi_min < 0] + 360

    # keep track of bins that span phi=0
    wrapped = phi_min > phi_max

    # When averaging data bins will be weighted by the solid angle of their overlap,
    # with the given spectrogram bin.  Since each spectrogram bin spans all theta 
    # values the theta portion of that calculation can be done in advance.  These
    # values will later be multiplied by the overlap along phi to get the total 
    # solid angle. 
    omega_part = np.abs(np.sin(dr * (data['theta'] + .5*data['dtheta'])) - np.sin(dr * (data['theta'] - .5*data['dtheta'])))

    omega_part_flat = omega_part.flatten(order='F')
    phi_max_flat = phi_max.flatten(order='F')
    phi_min_flat = phi_min.flatten(order='F')
    wrapped_flat = wrapped.flatten(order='F')
    data_flat = data['data'].flatten(order='F')
    bins_flat = data['bins'].flatten(order='F')
    dphi_flat = data['dphi'].flatten(order='F')

    # Loop over each phi bin in the spectrogram and determine which data bins
    # overlap.  All overlapping bins will be weighted according to the solid 
    # angle of their intersection and averaged.
    for i in range(0, n_phi):
        weight = np.zeros(phi_min_flat.shape)

        # data bins whose maximum overlaps the current spectrogram bin
        idx_max = np.argwhere((phi_max_flat > phi_grid[i]) & (phi_max_flat < phi_grid[i+1]))
        if idx_max.size != 0:
            weight[idx_max] = (phi_max_flat[idx_max] - phi_grid[i]) * omega_part_flat[idx_max]

        # data bins whose minimum overlaps the current spectrogram bin
        idx_min = np.argwhere((phi_min_flat > phi_grid[i]) & (phi_min_flat < phi_grid[i+1]))
        if idx_min.size != 0:
            weight[idx_min] = (phi_grid[i+1] - phi_min_flat[idx_min]) * omega_part_flat[idx_min]

        # data bins contained within the current spectrogram bin
        contained = np.intersect1d(idx_max, idx_min)
        if contained.size != 0:
            weight[contained] = dphi_flat[contained] * omega_part_flat[contained]
        
        # data bins that completely cover the current spectrogram bin 
        idx_all = np.argwhere(((phi_min_flat <= phi_grid[i]) & (phi_max_flat >= phi_grid[i+1])) |
                              (wrapped_flat & ((phi_min_flat > phi_grid[i+1]) & (phi_max_flat > phi_grid[i+1]))) |
                              (wrapped_flat & ((phi_min_flat < phi_grid[i]) & (phi_max_flat < phi_grid[i]))))
        if idx_all.size != 0:
            weight[idx_all] = phi_grid_width * omega_part_flat[idx_all]

        # combine indices
        idx = np.unique(np.concatenate((idx_min, idx_max, idx_all)))

        # assign a weighted average to this bin
        if idx_max.size + idx_min.size + idx_all.size > 0:
            # normalize weighting to selected, active bins
            weight[idx] = weight[idx] * bins_flat[idx]
            weight = weight/nansum(weight)

            # average
            ave[i] = nansum(data_flat[idx]*weight[idx])

    # get y axis
    y = (phi_grid+shift(phi_grid, 1))/2.0
    y = y[1:]

    return (y, ave)
