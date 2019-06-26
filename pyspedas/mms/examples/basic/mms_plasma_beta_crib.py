'''

This crib sheet shows how to calculate plasma beta using FPI and FGM data

'''

from pyspedas import tinterpol, mms_load_fpi, mms_load_fgm
from pytplot import get_data, store_data, tplot
import numpy as np

mu0 = 1256.0 # nT-m/A
Kb=1.3807*10**(-16.) # cm^2-g-1/s^2-1/K

probe = '1'
trange = ['2015-10-16/11:00', '2015-10-16/14:00']

mms_load_fpi(datatype=['dis-moms', 'des-moms'], trange=trange, probe=probe)
mms_load_fgm(trange=trange, probe=probe)

temp_para_i = 'mms'+probe+'_dis_temppara_fast'
temp_perp_i = 'mms'+probe+'_dis_tempperp_fast'
temp_para_e = 'mms'+probe+'_des_temppara_fast'
temp_perp_e = 'mms'+probe+'_des_tempperp_fast'
number_density_i = 'mms'+probe+'_dis_numberdensity_fast'
number_density_e = 'mms'+probe+'_des_numberdensity_fast'
b_field = 'mms'+probe+'_fgm_b_gsm_srvy_l2'
b_magnitude = 'mms'+probe+'_fgm_b_gsm_srvy_l2_mag'

times, data = get_data(b_field)

store_data(b_magnitude, data={'x': times, 'y': data[:, 3]})

ntimes, ndata = get_data(number_density_i)

n_out_indices = [i[0] for i in np.argwhere(ntimes>=times[0])]

store_data(number_density_i, data={'x': ntimes[n_out_indices], 'y': ndata[n_out_indices]})

tinterpol(b_magnitude, interp_names=[number_density_i], new_names='b_mag_interpolated')

btimes, bdata = get_data('mms1_fgm_b_gsm_srvy_l2_mag-itrp')

ipatimes, i_para_temp = get_data(temp_para_i)
ipetimes, i_perp_temp = get_data(temp_perp_i)
epatimes, e_para_temp = get_data(temp_para_e)
epetimes, e_perp_temp = get_data(temp_perp_e)

nitimes, i_n = get_data(number_density_i)
netimes, e_n = get_data(number_density_e)

# note: 1.0e-8 comes from A-nT/m -> g/(s^2-cm)
Pmag = 1.0e-8*bdata**2/(2.0*mu0)

Te_total=(e_para_temp+2*e_perp_temp)/3.0
Ti_total=(i_para_temp+2*i_perp_temp)/3.0

# note: eV -> K conversion: 11604.505 K/eV
Pplasma = (i_n*11604.505*Ti_total+e_n*11604.505*Te_total)*Kb

Beta = Pplasma/Pmag

store_data('plasma_beta', data={'x': btimes, 'y': Beta})
store_data('magnetic_pressure', data={'x': btimes, 'y': Pmag})
store_data('plasma_pressure', data={'x': btimes, 'y': Pplasma})

tplot(['plasma_beta', 'plasma_pressure', 'magnetic_pressure'])
