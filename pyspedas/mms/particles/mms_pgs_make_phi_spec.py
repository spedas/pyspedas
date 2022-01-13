
import numpy as np

# use nansum from bottleneck if it's installed, otherwise use the numpy one
try:
    import bottleneck as bn
    nansum = bn.nansum
except ImportError:
    nansum = np.nansum

def mms_pgs_make_phi_spec(data_in, resolution=32):

    data = data_in.copy()
    n_phi = resolution

    # zero inactive bins to ensure areas with no data are represented as NaN
    zero_bins = np.argwhere(data['bins'] == 0)
    if zero_bins.size != 0:
        for item in zero_bins:
            data['data'][item[0], item[1]] = 0.0

    ave = np.zeros(n_phi)
    bin_size = 360.0/n_phi
    outbins = np.arange(0, 361, bin_size)

    phi_flat = data['phi'].flatten()
    data_flat = data['data'].flatten()
    bins_flat = data['bins'].flatten()

    for bin_idx in range(0, len(outbins)-1):
        this_bin = np.argwhere((phi_flat >= outbins[bin_idx]) & (phi_flat < outbins[bin_idx+1]))
        if len(this_bin) > 0:
            ave[bin_idx] += nansum(data_flat[this_bin])/nansum(bins_flat[this_bin])
    
    y = outbins[0:n_phi]+0.5*(outbins[1::]-outbins[0:n_phi])

    return (y, ave)
