
import warnings
import numpy as np
from pytplot import get_data, store_data, options

def mms_feeps_spin_avg(probe='1', data_units='intensity', datatype='electron', data_rate='srvy', level='l2', suffix=''):

    if datatype == 'electron':
        lower_en = 71
    else:
        lower_en = 78

    prefix = 'mms'+str(probe)+'_epd_feeps_'

    # get the spin sectors
    # v5.5+ = mms1_epd_feeps_srvy_l1b_electron_spinsectnum
    sector_times, spin_sectors = get_data(prefix + data_rate + '_' + level + '_' + datatype + '_spinsectnum' + suffix)

    spin_starts = [spin_end+1 for spin_end in np.where(spin_sectors[:-1] >= spin_sectors[1:])[0]]

    var_name = prefix+data_rate+'_'+level+'_'+datatype+'_'+data_units+'_omni'

    times, data, energies = get_data(var_name)

    spin_avg_flux = np.zeros([len(spin_starts), len(energies)])

    current_start = spin_starts[0]
    for spin_idx in range(1, len(spin_starts)-1):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            spin_avg_flux[spin_idx-1, :] = np.nanmean(data[current_start:spin_starts[spin_idx]+1, :], axis=0)
        current_start = spin_starts[spin_idx] + 1

    store_data(var_name+'_spin'+suffix, data={'x': times[spin_starts], 'y': spin_avg_flux, 'v': energies})
    options(var_name+'_spin'+suffix, 'spec', True)
    options(var_name+'_spin'+suffix, 'ylog', True)
    options(var_name+'_spin'+suffix, 'zlog', True)
    options(var_name+'_spin'+suffix, 'Colormap', 'jet')
