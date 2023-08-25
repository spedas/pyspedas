import numpy as np

# use nansum from bottleneck if it's installed, otherwise use the numpy one
try:
    import bottleneck as bn
    nansum = bn.nansum
except ImportError:
    nansum = np.nansum


def mms_pgs_make_theta_spec(data_in, resolution=16, colatitude=False):
    """
    Builds a theta (latitudinal) spectrogram from a simplified particle data structure.

    Parameters
    ----------
    data_in : dict
        A dictionary containing the particle data, including 'data', 'theta', and 'bins' keys.
    resolution : int, optional
        The number of bins to use for the spectrogram. Defaults to 16.
    colatitude : bool, optional
        Set to True if the input data is in colatitude rather than latitude.

    Returns
    -------
    y : numpy.ndarray
        The y axis of the spectrogram.
    ave : numpy.ndarray
        The spectrogram.
    """
    data = data_in.copy()
    n_theta = resolution

    # zero inactive bins to ensure areas with no data are represented as NaN
    zero_bins = np.argwhere(data['bins'] == 0)
    if zero_bins.size != 0:
        for item in zero_bins:
            data['data'][item[0], item[1]] = 0.0

    ave = np.zeros(n_theta)
    bin_size = 180.0/n_theta
    outbins = np.arange(0, 181.0, bin_size)

    # shift to colatitude
    if not colatitude:
        data['theta'] = 90.0-data['theta']

    theta_flat = data['theta'].flatten()
    data_flat = data['data'].flatten()
    bins_flat = data['bins'].flatten()

    for bin_idx in range(0, len(outbins)-1):
        this_bin = np.argwhere((theta_flat >= outbins[bin_idx]) & (theta_flat < outbins[bin_idx+1]))
        if len(this_bin) > 0:
            bins = nansum(bins_flat[this_bin])
            if bins != 0.0:
                ave[bin_idx] += nansum(data_flat[this_bin])/bins

    if not colatitude:
        data['theta'] = 90.0-data['theta']
        outbins = 90.0-outbins

    y = outbins[0:n_theta]+0.5*(outbins[1::]-outbins[0:n_theta])

    return y, ave
