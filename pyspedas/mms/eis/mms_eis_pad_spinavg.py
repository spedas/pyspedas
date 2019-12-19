import warnings
import numpy as np
from pyspedas import tnames
from pytplot import get_data, store_data, options

def mms_eis_pad_spinavg(scopes=['0','1','2','3','4','5'], probe='1', data_rate='srvy', datatype='extof', data_units='flux', species='proton', energy=[55, 800], size_pabin=15, suffix=''):
    """
    Calculate spin-averaged pitch angle distributions using data from the MMS Energetic Ion Spectrometer (EIS)
    
    Parameters:
        scopes: list of str
            telescope #s to include in the calculation

        probe: str
            probe #, e.g., '4' for MMS4

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst' (default: 'srvy')

        datatype: str
            'extof' or 'phxtof' (default: 'extof')

        data_units: str
            'flux' or 'cps' (default: 'flux')

        species: str
            species for calculation (default: 'proton')

        energy: list of float
            energy range to include in the calculation (default: [55, 800])

        size_pabin: int
            size of the pitch angle bins, in degrees (default: 15)

        suffix: str
            suffix of the loaded data

    Returns:
        Name of tplot variables created.
    """
    en_range_string = str(int(energy[0])) + '-' + str(int(energy[1])) + 'keV'

    if data_units == 'cps':
        units_label = '1/s'
    else:
        units_label = '1/(cm^2-sr-s-keV)'

    if len(scopes) == 1:
        scope_suffix = '_t' + scopes + suffix
    elif len(scopes) == 6:
        scope_suffix = '_omni' + suffix

    if data_rate == 'brst':
        prefix = 'mms' + probe + '_epd_eis_brst_'
    else:
        prefix = 'mms' + probe + '_epd_eis_'

    # get the spin #s associated with each measurement
    spin_times, spin_nums = get_data(prefix + datatype + '_spin' + suffix)

    # find where the spins start
    spin_starts = [spin_start for spin_start in np.where(spin_nums[1:] > spin_nums[:-1])[0]]

    pad_vars = tnames(prefix + datatype + '_*keV_' + species + '_' + data_units + scope_suffix + '_pad')

    out_vars = []

    for pad_var in pad_vars:
        pad_times, pad_data, pad_angles = get_data(pad_var)

        if pad_data is None:
            print('Error, variable containing valid PAD data missing: ' + pad_var)
            continue

        spin_avg_flux = np.zeros([len(spin_starts), len(pad_angles)])
        spin_times = np.zeros(len(spin_starts))

        current_start = 0

        # loop through the spins for this telescope
        for spin_idx, spin_start in enumerate(spin_starts):
            ind = np.where(spin_nums == spin_nums[spin_starts[spin_idx]])[0]
            if ind is not None:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    spin_avg_flux[spin_idx, :] = np.nanmean(pad_data[ind], axis=0)
            spin_times[spin_idx] = pad_times[current_start]
            current_start = spin_starts[spin_idx]+1

        newname = pad_var + '_spin'

        n_pabins = 180./size_pabin
        new_bins = [180.*n_pabin/n_pabins for n_pabin in range(0, int(n_pabins)+1)]
        new_pa_label = [180.*n_pabin/n_pabins+size_pabin/2. for n_pabin in range(0, int(n_pabins))]

        store_data(newname, data={'x': spin_times, 'y': spin_avg_flux, 'v': new_pa_label})
        options(newname, 'ylog', False)
        options(newname, 'zlog', True)
        options(newname, 'spec', True)
        options(newname, 'Colormap', 'jet')
        options(newname, 'ztitle', units_label)
        options(newname, 'ytitle', 'MMS' + str(probe) + ' ' + datatype + ' spin PAD (deg)')
        out_vars.append(newname)

    return out_vars