'''

This script loads and prints FEEPS srvy-mode ion data at several data points.

This is meant to be called from the IDL test suite for comparison with the data loaded via IDL SPEDAS

'''

from pyspedas import mms_load_feeps
from pytplot import get_data

mms_load_feeps(datatype='ion')

t, d, e = get_data('mms1_epd_feeps_srvy_l2_ion_intensity_omni')

# times
print(t[0:10].round(6).tolist())

# energy table
print(e.round(6).tolist())

# spot-check some data values
print(d[2, :].tolist())

print(d[2000, :].tolist())

print(d[5000, :].tolist())

print(d[10000, :].tolist())

print(d[15000, :].tolist())


