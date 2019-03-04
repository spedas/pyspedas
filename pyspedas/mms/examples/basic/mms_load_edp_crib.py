'''

This crib sheet shows how to load MMS electric field data

'''

from pyspedas.mms import mms_load_edp
from pytplot import tplot

# 'fast' mode electric field data for MMS1 are loaded by default
mms_load_edp(trange=['2015-10-16', '2015-10-17'])
tplot('mms1_edp_dce_gse_fast_l2')

# to load the burst mode data, set the data rate to 'brst'
mms_load_edp(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:07'])
tplot('mms1_edp_dce_gse_brst_l2')

# to load the spacecraft potential data, set the datatype to 'scpot'
mms_load_edp(datatype='scpot', trange=['2015-10-16', '2015-10-17'])
tplot('mms1_edp_scpot_fast_l2')
