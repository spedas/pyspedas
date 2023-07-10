# Load and show tplot variable created using load_fdsn

from pyspedas.mth5.load_fdsn import load_fdsn
import pytplot
import numpy as np

load_fdsn(network="4P", station="ALW48", trange=['2015-06-22', '2015-06-24'])
pytplot.tplot('fdsn_4P_ALW48')

# Get data
time, mag = pytplot.get_data('fdsn_4P_ALW48')

# Re-normalize magnetometer data removing the baseline
mag[:,0] -= np.mean(mag[:,0])
mag[:,1] -= np.mean(mag[:,1])
mag[:,2] -= np.mean(mag[:,2])

pytplot.store_data('fdsn_4P_ALW48_norm', data={'x': time, 'y':mag})

# Plot
pytplot.tplot('fdsn_4P_ALW48_norm')
