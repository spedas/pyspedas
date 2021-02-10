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

        species: str
            species for calculation (default: 'proton')
            
        data_units: str
            'flux' or 'cps' (default: 'flux')

        datatype: str
            'extof' or 'phxtof' (default: 'extof')

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst' (default: 'srvy')

        suffix: str
            suffix of the loaded data

    Returns:
        List of tplot variables created.
    """
    if data_rate == 'brst':
        prefix = 'mms' + probe + '_epd_eis_brst_'
    else:
        prefix = 'mms' + probe + '_epd_eis_'

    if data_units == 'flux':
        units_label = '1/(cm^2-sr-s-keV)'
    elif data_units == 'cps':
        units_label = '1/s'
    elif data_units == 'counts':
        units_label = 'counts'

    spin_data = get_data(prefix + datatype + '_spin' + suffix)
    if spin_data == None:
        print('Error, problem finding EIS spin variable to calculate spin-averages')
        return

    spin_times, spin_nums = spin_data

    if spin_nums is not None:
        spin_starts = [spin_start for spin_start in np.where(spin_nums[1:] > spin_nums[:-1])[0]]

        telescopes = tnames(prefix + datatype + '_' + species + '_*' + data_units + '_t?' + suffix)

        if len(telescopes) != 6:
            print('Problem calculating the spin-average for species: ' + species + ' (' + datatype + ')')
            return None

        out_vars = []

        for scope in range(0, 6):
            this_scope = telescopes[scope]
            scope_data = get_data(this_scope)
            
            if len(scope_data) <= 2:
                print("Error, couldn't find energy table for the variable: " + this_scope)
                continue

            flux_times, flux_data, energies = scope_data

            spin_avg_flux = np.zeros([len(spin_starts), len(energies)])

            current_start = 0

            for spin_idx in range(0, len(spin_starts)):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    spin_avg_flux[spin_idx, :] = np.nanmean(flux_data[current_start:spin_starts[spin_idx]+1, :], axis=0)
                current_start = spin_starts[spin_idx] + 1

            store_data(this_scope + '_spin', data={'x': flux_times[spin_starts], 'y': spin_avg_flux, 'v': energies})
            options(this_scope + '_spin', 'ztitle', units_label)
            options(this_scope + '_spin', 'ytitle', 'MMS' + probe + ' ' + datatype + ' ' + species + ' (spin) Energy [keV]')
            options(this_scope + '_spin', 'spec', True)
            options(this_scope + '_spin', 'ylog', True)
            options(this_scope + '_spin', 'zlog', True)
            options(this_scope + '_spin', 'Colormap', 'jet')
            out_vars.append(this_scope + '_spin')
        return out_vars
    else:
        print('Error, problem finding EIS spin variable to calculate spin-averages')
        return None