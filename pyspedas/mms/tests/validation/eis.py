'''

This script loads and prints EIS data at several data points.

This is meant to be called from the IDL test suite for comparison with the data loaded via IDL SPEDAS

'''


from pyspedas import mms_load_eis
from pytplot import get_data

mms_load_eis(datatype=['extof', 'phxtof'])

t, d, e = get_data('mms1_epd_eis_phxtof_proton_flux_omni')

# times
print(t[0:10].round(6).tolist())

# energy table
print(e.round(6).tolist())

# [29286.448073, 29934.537153, 10334.159171, 3525.301737, 654.593714]
print(d[5000, :].round(6).tolist())

# [1227.940468, 1413.869546, 1621.562557, 986.801898, 108.332355]
print(d[10000, :].round(6).tolist())

# [0.0, 126.516648, 148.667251, 44.479945, 5.635036]
print(d[15000, :].round(6).tolist())

# [23348.150933, 21319.249786, 13214.553887, 8140.552282, 761.221793]
print(d[20000, :].round(6).tolist())

t, d, e = get_data('mms1_epd_eis_extof_proton_flux_omni')

# times
print(t[0:10].round(6).tolist())

# energy table
print(e.round(6).tolist())

# [1276.03332, 606.363908, 16.55926, 0.0, 0.0, 0.0, 0.0]
print(d[5000, :].round(6).tolist())

# [434.89612, 102.014095, 12.167977, 0.0, 0.0, 0.0, 0.0]
print(d[10000, :].round(6).tolist())

# [6.514261, 14.790835, 0.0, 0.0, 0.0, 0.0, 0.0]
print(d[15000, :].round(6).tolist())

# [3298.158253, 403.540356, 42.910679, 0.0, 0.0, 0.0, 0.0]
print(d[20000, :].round(6).tolist())
