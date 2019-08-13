'''

This crib sheet shows how to load and plot ASPOC data

'''

from pyspedas import mms_load_aspoc
from pytplot import tplot

# load ASPOC data 
mms_load_aspoc(trange=['2015-10-16', '2015-10-17'], data_rate='srvy')

# plot the ion current from aspoc1, aspoc2, and total current
tplot(['mms1_asp1_ionc', 'mms1_asp2_ionc', 'mms1_aspoc_ionc'])
