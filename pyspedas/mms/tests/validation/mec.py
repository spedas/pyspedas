from pyspedas import mms_load_mec
from pytplot import get_data

mms_load_mec()

t, d = get_data('mms1_mec_r_gse')

print(t[0:10].round(6).tolist())

print(d[0].tolist())

print(d[100].tolist())

print(d[200].tolist())

print(d[300].tolist())

print(d[400].tolist())

print(d[500].tolist())

print(d[600].tolist())

print(d[700].tolist())

print(d[800].tolist())

print(d[900].tolist())

print(d[1000].tolist())

print(d[1500].tolist())

print(d[2000].tolist())

print(d[2500].tolist())
