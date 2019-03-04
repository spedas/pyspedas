'''

This crib sheet shows how to load MMS FPI data

'''

from pyspedas.mms import mms_load_fpi
from pytplot import tplot, del_data

# load the electron moments data
mms_load_fpi(datatype='des-moms', trange=['2015-10-16', '2015-10-17'])
tplot(['mms1_des_energyspectr_omni_fast', 'mms1_des_bulkv_gse_fast', 'mms1_des_numberdensity_fast'])

# load the ion moments data
mms_load_fpi(datatype='dis-moms', trange=['2015-10-16', '2015-10-17'])
tplot(['mms1_dis_energyspectr_omni_fast', 'mms1_dis_bulkv_gse_fast', 'mms1_dis_numberdensity_fast'])

del_data('*')

# load burst mode moments data for both electrons and ions
mms_load_fpi(data_rate='brst', datatype='dis-moms', trange=['2015-10-16/13:06', '2015-10-16/13:07'])
tplot(['mms1_dis_energyspectr_omni_brst', 'mms1_dis_bulkv_gse_brst', 'mms1_dis_numberdensity_brst'])
