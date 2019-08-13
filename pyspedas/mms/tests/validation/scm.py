from pyspedas import mms_load_scm
from pytplot import get_data

mms_load_scm()

t, d = get_data('mms1_scm_acb_gse_scsrvy_srvy_l2')

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

print(d[1500000].tolist())

print(d[2000000].tolist())
