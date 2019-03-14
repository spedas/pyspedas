'''

This crib sheet shows how to load MMS FGM data

'''

from pyspedas import mms_load_fgm
from pytplot import tplot, get_data, del_data

# by default, 'srvy' mode data for MMS1 are loaded
mms_load_fgm(trange=['2015-10-16', '2015-10-17'])
tplot(['mms1_fgm_b_gse_srvy_l2', 'mms1_fgm_b_gsm_srvy_l2'])

del_data('*')

# to load burst mode data, change the data rate to 'brst'
mms_load_fgm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:07'])
tplot(['mms1_fgm_b_gse_brst_l2', 'mms1_fgm_b_gsm_brst_l2'])

del_data('*')

# to keep the data flagged by the 'flag' variable, use the keep_flagged keyword
mms_load_fgm(keep_flagged=True, trange=['2015-10-16', '2015-10-17'])
tplot(['mms1_fgm_b_gse_srvy_l2', 'mms1_fgm_b_gsm_srvy_l2'])

# access the data values with get_data
times, data = get_data('mms1_fgm_b_gse_srvy_l2')

# print the first time
print(times[0])

# and the first vector+magnitude in the dataset
print(data[0])
