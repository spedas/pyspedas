'''

This crib sheet shows how to load and plot EIS data

'''

from pyspedas import mms_load_eis, mms_eis_pad, tnames
from pytplot import tplot

# load ExTOF data
mms_load_eis(trange=['2015-10-16', '2015-10-17'], datatype='extof')

# plot the H+ flux
tplot(tnames('*_extof_proton_flux_omni'))

# load PHxTOF data
mms_load_eis(trange=['2015-10-16', '2015-10-17'], datatype='phxtof')

# plot the H+ flux
tplot(tnames('*_phxtof_proton_flux_omni'))

# calculate the ExTOF pitch angle distribution
mms_eis_pad(datatype='extof')

tplot(['mms1_epd_eis_extof_56-535keV_proton_flux_omni_pad_spin', 'mms1_epd_eis_extof_56-535keV_proton_flux_omni_pad'])

# calculate the PHxTOF pitch angle distribution
mms_eis_pad(datatype='phxtof', energy=[10, 60])

tplot(['mms1_epd_eis_phxtof_11-57keV_proton_flux_omni_pad_spin', 'mms1_epd_eis_phxtof_11-57keV_proton_flux_omni_pad'])