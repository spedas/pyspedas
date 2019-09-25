'''

This crib sheet shows how to load and plot FEEPS data

'''

from pyspedas import mms_load_feeps, mms_feeps_pad
from pytplot import tplot

# load electron data
mms_load_feeps(trange=['2015-10-16', '2015-10-17'], datatype='electron')

# plot the omni-directional electron intensity
tplot(['mms1_epd_feeps_srvy_l2_electron_intensity_omni', 'mms1_epd_feeps_srvy_l2_electron_intensity_omni_spin'])

# calculate the pitch angle distribution
mms_feeps_pad()

# plot the PAD
tplot('mms1_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad')