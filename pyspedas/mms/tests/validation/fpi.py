from pyspedas import mms_load_fpi
from pytplot import get_data

mms_load_fpi()

t, d, e = get_data('mms1_des_energyspectr_omni_fast')

print(t[0:10].round(6).tolist())

print(d[0, :].round(6).tolist())

print(d[1000, :].tolist())

print(d[2000, :].tolist())

print(d[3000, :].tolist())

print(d[4000, :].tolist())

print(d[5000, :].tolist())

print(d[6000, :].tolist())

print(d[7000, :].tolist())

print(d[8000, :].tolist())

print(d[9000, :].tolist())
