'''

This crib sheet shows how to load and plot HPCA data

'''

from pyspedas import mms_load_hpca
from pytplot import tplot

# load moments data
mms_load_hpca(trange=['2015-10-16/13:05', '2015-10-16/13:10'], data_rate='brst', time_clip=True)

# show H+, O+ and He+ density
tplot(['mms1_hpca_hplus_number_density', 
        'mms1_hpca_oplus_number_density', 
        'mms1_hpca_heplus_number_density'])

# show H+, O+ and He+ temperature
tplot(['mms1_hpca_hplus_scalar_temperature', 
        'mms1_hpca_oplus_scalar_temperature', 
        'mms1_hpca_heplus_scalar_temperature'])

# show H+, O+ and He+ flow velocity
tplot(['mms1_hpca_hplus_ion_bulk_velocity', 
        'mms1_hpca_oplus_ion_bulk_velocity', 
        'mms1_hpca_heplus_ion_bulk_velocity'])

# load the ion data
mms_load_hpca(trange=['2015-10-16/13:05', '2015-10-16/13:07'], datatype='ion', data_rate='brst')

from pyspedas import mms_hpca_calc_anodes
from pyspedas import mms_hpca_spin_sum

# average the flux over the full field of view (0-360)
mms_hpca_calc_anodes(fov=[0, 360], probe='1')

# spin-average to calculate the omni-directional flux
mms_hpca_spin_sum()

# show omni-directional flux for H+, O+ and He+, He++
tplot(['mms1_hpca_hplus_flux_elev_0-360_spin', 
             'mms1_hpca_oplus_flux_elev_0-360_spin', 
             'mms1_hpca_heplus_flux_elev_0-360_spin', 
             'mms1_hpca_heplusplus_flux_elev_0-360_spin'])
