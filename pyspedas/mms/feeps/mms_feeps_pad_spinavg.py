
import warnings
import numpy as np
import scipy 
from pytplot import get_data, store_data, options

def mms_feeps_pad_spinavg(probe='1', data_units='intensity', datatype='electron', data_rate='srvy', level='l2', suffix='', energy=[70, 600], bin_size=16.3636):
    """
    This function will spin-average the FEEPS pitch angle distributions
    
    Parameters:
        probe: str
            probe #, e.g., '4' for MMS4

        data_units: str
            'intensity' or 'count_rate'

        datatype: str
            'electron' or 'ion'

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst'

        level: str
            data level, e.g., 'l2'

        suffix: str
            suffix of the loaded data

        energy: list of float
            energy range to include in the calculation
            
        bin_size: float
            size of the pitch angle bins

    Returns:
        Name of tplot variable created.
    """

    units_label = ''
    if data_units == 'intensity':
        units_label = '1/(cm^2-sr-s-keV)'
    elif data_units == 'counts':
        units_label = '[counts/s]'

    if datatype == 'electron':
        lower_en = 71
    else:
        lower_en = 78

    prefix = 'mms'+str(probe)+'_epd_feeps_'

    n_pabins = 180./bin_size
    new_bins = [180.*i/n_pabins for i in range(int(n_pabins)+1)]

    # get the spin sectors
    # v5.5+ = mms1_epd_feeps_srvy_l1b_electron_spinsectnum
    sector_times, spin_sectors = get_data(prefix + data_rate + '_' + level + '_' + datatype + '_spinsectnum' + suffix)

    spin_starts = [spin_end + 1 for spin_end in np.where(spin_sectors[:-1] >= spin_sectors[1:])[0]]

    en_range_string = str(int(energy[0])) + '-' + str(int(energy[1])) + 'keV'
    var_name =  prefix + data_rate + '_' + level + '_' + datatype + '_' + data_units + '_' + en_range_string + '_pad' + suffix

    times, data, angles = get_data(var_name)

    spin_avg_flux = np.zeros([len(spin_starts), len(angles)])
    rebinned_data = np.zeros([len(spin_starts), int(n_pabins)+1])
    spin_times = np.zeros(len(spin_starts))

    # the following is for rebinning and interpolating to new_bins
    srx = [float(len(angles))/(int(n_pabins)+1)*(x + 0.5) - 0.5 for x in range(int(n_pabins)+1)]

    current_start = 0
    for spin_idx in range(0, len(spin_starts)):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            spin_avg_flux[spin_idx, :] = np.nanmean(data[current_start:spin_starts[spin_idx]+1, :], axis=0)
            spin_times[spin_idx] = times[current_start]

            # rebin and interpolate to new_bins
            # this is meant to replicate the functionality of congrid in the IDL routine
            spin_avg_interp = scipy.interpolate.interp1d(np.arange(len(spin_avg_flux[spin_idx, :])), spin_avg_flux[spin_idx, :], fill_value='extrapolate')
            rebinned_data[spin_idx, :] = spin_avg_interp(srx)

            # we want to take the end values instead of extrapolating
            # again, to match the functionality of congrid in IDL
            rebinned_data[spin_idx, 0] = spin_avg_flux[spin_idx, 0]
            rebinned_data[spin_idx, -1] = spin_avg_flux[spin_idx, -1]

        current_start = spin_starts[spin_idx] + 1

    # store_data(var_name + '_spin' + suffix, data={'x': spin_times, 'y': spin_avg_flux, 'v': angles})
    store_data(var_name + '_spin' + suffix, data={'x': spin_times, 'y': rebinned_data, 'v': new_bins})
    options(var_name + '_spin' + suffix, 'spec', True)
    options(var_name + '_spin' + suffix, 'ylog', False)
    options(var_name + '_spin' + suffix, 'zlog', True)
    options(var_name + '_spin' + suffix, 'Colormap', 'jet')
    options(var_name + '_spin' + suffix, 'ztitle', units_label)
    options(var_name + '_spin' + suffix, 'ytitle', 'MMS' + str(probe) + ' ' + datatype + ' PA (deg)')

    return var_name + '_spin' + suffix
