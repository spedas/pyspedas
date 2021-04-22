
import math
import numpy as np
from scipy.ndimage.interpolation import shift

# use nansum from bottleneck if it's installed, otherwise use the numpy one
try:
    import bottleneck as bn
    nansum = bn.nansum
except:
    nansum = np.nansum

def spd_pgs_make_phi_spec(data_in, resolution=None):
    """

    """

    dr = math.pi/180.
    rd = 1.0/dr

    data = data_in.copy()

    # zero inactive bins to ensure areas with no data are represented as NaN
    zero_bins = np.argwhere(data['bins'] == 0)
    if zero_bins.size != 0:
        for item in zero_bins:
            data['data'][item[0], item[1]] = 0.0

    # get number of phi values
    if resolution == None:
        # method taken from the IDL code
        idx = np.nanargmin(np.abs((data['theta'][0, :])))
        n_phi = len(np.argwhere(data['theta'][0, :] == np.abs((data['theta'][0, :]))[idx]))
    else:
        n_phi = resolution

    # init this sample's piece of the spectrogram
    ave = np.zeros(n_phi)
    ave_s = np.zeros(n_phi)

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

    # Loop over each phi bin in the spectrogram and determine which data bins
    # overlap.  All overlapping bins will be weighted according to the solid 
    # angle of their intersection and averaged.
    for i in range(0, n_phi):
        weight = np.zeros(phi_min.shape)

        # data bins whose maximum overlaps the current spectrogram bin
        idx_max = np.argwhere((phi_max > phi_grid[i]) & (phi_max < phi_grid[i+1]))
        if idx_max.size != 0:
            weight[idx_max[:, 0].tolist(), idx_max[:, 1].tolist()] = (phi_max[idx_max[:, 0].tolist(), idx_max[:, 1].tolist()] - phi_grid[i]) * omega_part[idx_max[:, 0].tolist(), idx_max[:, 1].tolist()]

        # data bins whose minimum overlaps the current spectrogram bin
        idx_min = np.argwhere((phi_min > phi_grid[i]) & (phi_min < phi_grid[i+1]))
        if idx_min.size != 0:
            weight[idx_min[:, 0].tolist(), idx_min[:, 1].tolist()] = (phi_grid[i+1] - phi_min[idx_min[:, 0].tolist(), idx_min[:, 1].tolist()]) * omega_part[idx_min[:, 0].tolist(), idx_min[:, 1].tolist()]
        
        # data bins contained within the current spectrogram bin
        max_set = set([tuple(m) for m in idx_max])
        min_set = set([tuple(m) for m in idx_min])
        contained = np.array([m for m in max_set & min_set])
        if contained.size != 0:
            weight[contained[:, 0].tolist(), contained[:, 1].tolist()] = data['dphi'][contained[:, 0].tolist(), contained[:, 1].tolist()] * omega_part[contained[:, 0].tolist(), contained[:, 1].tolist()]
        
        # data bins that completely cover the current spectrogram bin 
        idx_all = np.argwhere(((phi_min <= phi_grid[i]) & (phi_max >= phi_grid[i+1])) |
                              (wrapped & ((phi_min > phi_grid[i+1]) & (phi_max > phi_grid[i+1]))) |
                              (wrapped & ((phi_min < phi_grid[i]) & (phi_max < phi_grid[i]))))
        if idx_all.size != 0:
            weight[idx_all[:, 0].tolist(), idx_all[:, 1].tolist()] = phi_grid_width * omega_part[idx_all[:, 0].tolist(), idx_all[:, 1].tolist()]

        # combine indices
        idx = np.concatenate((idx_min, idx_max, idx_all))

        # assign a weighted average to this bin
        if idx_max.size + idx_min.size + idx_all.size > 0:
            # normalize weighting to selected, active bins
            weight[idx[:, 0].tolist(), idx[:, 1].tolist()] = weight[idx[:, 0].tolist(), idx[:, 1].tolist()] * data['bins'][idx[:, 0].tolist(), idx[:, 1].tolist()]
            weight = weight/nansum(weight)

            # average
            ave[i] = nansum(data['data'][idx[:, 0].tolist(), idx[:, 1].tolist()]*weight[idx[:, 0].tolist(), idx[:, 1].tolist()])

    # get y axis
    y = (phi_grid+shift(phi_grid, 1))/2.0
    y = y[1:]

    return (y, ave)
