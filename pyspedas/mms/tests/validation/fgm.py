'''

This script loads and prints FGM data at several data points.

This is meant to be called from the IDL test suite for comparison with the data loaded via IDL SPEDAS

'''

from pyspedas import mms_load_fgm
from pytplot import get_data

mms_load_fgm()

t, d = get_data('mms1_fgm_b_gse_srvy_l2')

print(t[0:10].round(6).tolist())

print(d[10000].tolist())

print(d[50000].tolist())

print(d[100000].tolist())

print(d[200000].tolist())

print(d[300000].tolist())

print(d[400000].tolist())

print(d[500000].tolist())

print(d[600000].tolist())

print(d[700000].tolist())

print(d[800000].tolist())

print(d[900000].tolist())
