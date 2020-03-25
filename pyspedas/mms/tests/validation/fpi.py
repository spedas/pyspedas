from pyspedas import mms_load_fpi
from pytplot import get_data

mms_load_fpi()

t, d, e = get_data('mms1_des_energyspectr_omni_fast')

print(t[0:10].round(6).tolist())

print(d[0, :].round(6).tolist())

print(d[1000, :].round(14).tolist())

print(d[2000, :].round(14).tolist())

print(d[3000, :].round(14).tolist())

print(d[4000, :].round(14).tolist())

print(d[5000, :].round(14).tolist())

print(d[6000, :].round(14).tolist())

print(d[7000, :].round(14).tolist())

print(d[8000, :].round(14).tolist())

print(d[9000, :].round(14).tolist())
