from pyspedas import mms_load_dsp
from pytplot import get_data

mms_load_dsp(data_rate='fast', datatype=['epsd', 'bpsd'])

t, d, f = get_data('mms1_dsp_bpsd_omni_fast_l2')

print(t[0:10].round(6).tolist())

print(d[1000].tolist())

print(d[2000].tolist())

print(d[3000].tolist())

print(d[4000].tolist())

print(d[5000].tolist())

print(d[6000].tolist())

print(d[7000].tolist())

print(d[8000].tolist())

print(d[9000].tolist())

print(d[10000].tolist())

print(f.tolist())

t, d, f = get_data('mms1_dsp_epsd_omni')

print(t[0:10].round(6).tolist())

print(d[1000].tolist())

print(d[2000].tolist())

print(d[3000].tolist())

print(d[4000].tolist())

print(d[5000].tolist())

print(d[6000].tolist())

print(d[7000].tolist())

print(d[8000].tolist())

print(d[9000].tolist())

print(d[10000].tolist())

print(f.tolist())
