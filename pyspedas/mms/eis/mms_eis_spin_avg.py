import warnings
import numpy as np
from pytplot import get_data, store_data, options
from pyspedas import tnames

def mms_eis_spin_avg(probe='1', species='proton', data_units='flux', datatype='extof', data_rate='srvy', suffix=''):
    """
    This function will spin-average the EIS spectrograms, and is automatically called from mms_load_eis
    
    Parameters:
        probe: str
            probe #, e.g., '4' for MMS4
        data_units: str
            'flux' 
        datatype: str
            'extof' or 'phxtof'
        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst'
        suffix: str
            suffix of the loaded data

    Returns:
        List of tplot variables created.
    """
    if data_rate == 'brst':
        prefix = 'mms' + probe + '_epd_eis_brst_'
    else:
        prefix = 'mms' + probe + '_epd_eis_'

    spin_times, spin_nums = get_data(prefix + datatype + '_spin' + suffix)

    if spin_nums is not None:
        spin_starts = [spin_start for spin_start in np.where(spin_nums[1:] > spin_nums[:-1])[0]]

        telescopes = tnames(prefix + datatype + '_' + species + '_*' + data_units + '_t?' + suffix)

        out_vars = []

        for scope in range(0, 6):
            this_scope = telescopes[scope]
            flux_times, flux_data, energies = get_data(this_scope)

            spin_avg_flux = np.zeros([len(spin_starts), len(energies)])

            current_start = 0

            for spin_idx in range(0, len(spin_starts)):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    spin_avg_flux[spin_idx-1, :] = np.nanmean(flux_data[current_start:spin_starts[spin_idx]+1, :], axis=0)
                current_start = spin_starts[spin_idx] + 1

            store_data(this_scope + '_spin' + suffix, data={'x': flux_times[spin_starts], 'y': spin_avg_flux, 'v': energies})
            options(this_scope + '_spin' + suffix, 'spec', True)
            options(this_scope + '_spin' + suffix, 'ylog', True)
            options(this_scope + '_spin' + suffix, 'zlog', True)
            options(this_scope + '_spin' + suffix, 'Colormap', 'jet')
            out_vars.append(this_scope + '_spin' + suffix)
        return out_vars
    else:
        print('Error, problem finding EIS spin variable to calculate spin-averages')
        return None