
from pyspedas import mms_load_edi
from pytplot import get_data

mms_load_edi(trange=['2016-10-16','2016-10-17'])

t, d = get_data('mms1_edi_e_gse_srvy_l2')

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

print(d[1100].tolist())

print(d[1200].tolist())

print(d[1300].tolist())
