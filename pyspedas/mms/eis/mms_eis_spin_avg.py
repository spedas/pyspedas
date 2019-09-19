
import warnings
import numpy as np
from pytplot import get_data, store_data, options
from pyspedas import tnames

def mms_eis_spin_avg(probe='1', species='proton', data_units='flux', datatype='extof', data_rate='srvy', suffix=''):

    if data_rate == 'brst':
        prefix = 'mms' + probe + '_epd_eis_brst_'
    else:
        prefix = 'mms' + probe + '_epd_eis_'

    spin_times, spin_nums = get_data(prefix + datatype + '_' + 'spin' + suffix)

    if spin_nums is not None:
        spin_starts = [spin_start for spin_start in np.where(spin_nums[1:] > spin_nums[:-1])[0]]

        telescopes = tnames(prefix + datatype + '_' + species + '_*' + data_units + '_t?' + suffix)

        for scope in range(0, 5):
            this_scope = telescopes[scope]
            flux_times, flux_data, energies = get_data(this_scope)

            spin_avg_flux = np.zeros([len(spin_starts), len(energies)])

            current_start = 0

            for spin_idx in range(0, len(spin_starts)-1):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    spin_avg_flux[spin_idx-1, :] = np.nanmean(flux_data[current_start:spin_starts[spin_idx]+1, :], axis=0)
                current_start = spin_starts[spin_idx] + 1

            store_data(this_scope+'_spin'+suffix, data={'x': flux_times[spin_starts], 'y': spin_avg_flux, 'v': energies})
            options(this_scope+'_spin'+suffix, 'spec', True)
            options(this_scope+'_spin'+suffix, 'ylog', True)
            options(this_scope+'_spin'+suffix, 'zlog', True)
            options(this_scope+'_spin'+suffix, 'Colormap', 'jet')
