'''

This crib sheet shows how to load and plot Electron Drift Instrument (EDI) data

'''

from pyspedas import mms_load_edi
from pytplot import tplot

# load data from the Electron Drift Instrument
mms_load_edi(trange=['2015-12-23', '2015-12-24'], data_rate='srvy', datatype='efield')

# plot the ExB drift velocity and electric field
tplot(['mms1_edi_vdrift_gse_srvy_l2', 'mms1_edi_e_gse_srvy_l2'])