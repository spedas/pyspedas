from pyspedas import mms_load_fpi
from pytplot import get_data

mms_load_fpi(probe=1, datatype='des-moms', data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:07'])

t, d, e = get_data('mms1_des_energyspectr_omni_brst')

print(t[0:10].round(6).tolist())

print(d[0, :].tolist())

print(d[1000, :].tolist())

print(d[2000, :].tolist())

print(d[3000, :].tolist())

print(d[4000, :].tolist())
