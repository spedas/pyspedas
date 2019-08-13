
from pyspedas import mms_load_aspoc
from pytplot import get_data

mms_load_aspoc()

t, d = get_data('mms1_aspoc_ionc')

print(t[0:10].round(6).tolist())

print(d[50000])

print(d[51000])

print(d[52000])

print(d[53000])

print(d[54000])

print(d[55000])

print(d[56000])

print(d[57000])

print(d[58000])

print(d[59000])

print(d[60000])
