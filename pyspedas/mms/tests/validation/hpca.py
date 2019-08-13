
from pyspedas import mms_load_hpca
from pyspedas.mms.hpca.mms_hpca_calc_anodes import mms_hpca_calc_anodes
from pyspedas.mms.hpca.mms_hpca_spin_sum import mms_hpca_spin_sum
from pytplot import get_data

probe = '1'

mms_load_hpca(datatype='ion', probe=probe, trange=['2016-10-16', '2016-10-17'])
mms_hpca_calc_anodes(fov=[0, 360], probe=probe)
mms_hpca_spin_sum(probe=probe)

t, d, e = get_data('mms1_hpca_hplus_flux_elev_0-360_spin')

print(t[0:10].round(6).tolist())

print(d[0, :].round(6).tolist())

print(d[1000, :].round(6).tolist())

print(d[2000, :].round(6).tolist())

print(d[3000, :].round(6).tolist())

print(d[4000, :].round(6).tolist())

print(d[5000, :].round(6).tolist())

print(d[6000, :].round(6).tolist())

print(d[7000, :].round(6).tolist())
