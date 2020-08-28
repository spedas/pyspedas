from pyspedas import mms_load_edp
from pytplot import get_data

mms_load_edp(probe=1, trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst')

t, d = get_data('mms1_edp_dce_gse_brst_l2')

print(t[0:10].round(6).tolist())

print(d[10000].tolist())

print(d[50000].tolist())

print(d[100000].tolist())

print(d[200000].tolist())

print(d[300000].tolist())

print(d[400000].tolist())
