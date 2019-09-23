'''

This crib sheet shows how to load and plot EIS data

'''

from pyspedas import mms_load_eis, tnames
from pytplot import tplot

# load ExTOF data
mms_load_eis(trange=['2015-10-16', '2015-10-17'], datatype='extof')

# plot the H+ flux
tplot(tnames('*_extof_proton_flux_omni'))

# load PHxTOF data
mms_load_eis(trange=['2015-10-16', '2015-10-17'], datatype='phxtof')

# plot the H+ flux
tplot(tnames('*_phxtof_proton_flux_omni'))
