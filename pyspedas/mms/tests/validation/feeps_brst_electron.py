'''

This script loads and prints FEEPS brst-mode ion data at several data points.

This is meant to be called from the IDL test suite for comparison with the data loaded via IDL SPEDAS

'''

from pyspedas import mms_load_feeps
from pytplot import get_data

mms_load_feeps(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst')

t, d, e = get_data('mms1_epd_feeps_brst_l2_electron_intensity_omni')

# times
print(t[0:10].round(6).tolist())

# energy table
print(e.round(6).tolist())

# spot-check some data values
print(d[2, :].tolist())

print(d[200, :].tolist())

print(d[300, :].tolist())

print(d[350, :].tolist())

print(d[400, :].tolist())

print(d[450, :].tolist())
