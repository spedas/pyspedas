'''

This crib sheet shows how to load MMS MEC data

'''

from pyspedas.mms import mms_load_mec
from pytplot import tplot, del_data

# 'srvy' mode data for MMS1 are loaded by default
mms_load_mec(trange=['2015-10-16', '2015-10-17'])

tplot(['mms1_mec_r_gsm', 'mms1_mec_v_gsm'])
