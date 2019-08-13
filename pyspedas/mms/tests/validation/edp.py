from pyspedas import mms_load_edp
from pytplot import get_data

mms_load_edp()

t, d = get_data('mms1_edp_dce_gse_fast_l2')

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

print(d[1000000].tolist())

print(d[1100000].tolist())

print(d[1200000].tolist())

print(d[1300000].tolist())
