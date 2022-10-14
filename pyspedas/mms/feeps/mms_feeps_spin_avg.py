import warnings
import numpy as np
from pytplot import get_data, store_data, options

# use nanmean from bottleneck if it's installed, otherwise use the numpy one
# bottleneck nanmean is ~2.5x faster
try:
    import bottleneck as bn
    nanmean = bn.nanmean
except ImportError:
    nanmean = np.nanmean

def mms_feeps_spin_avg(probe='1', data_units='intensity', datatype='electron', data_rate='srvy', level='l2', suffix=''):
    """
    This function will spin-average the omni-directional FEEPS energy spectra
    
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

    Returns:
        Name of tplot variable created.
    """

    units_label = ''
    if data_units == 'intensity':
        units_label = '1/(cm^2-sr-s-keV)'
    elif data_units == 'counts':
        units_label = '[counts/s]'

    if datatype == 'electron':
        lower_en = 71.0
    else:
        lower_en = 78.0

    prefix = 'mms'+str(probe)+'_epd_feeps_'

    # get the spin sectors
    # v5.5+ = mms1_epd_feeps_srvy_l1b_electron_spinsectnum
    sector_times, spin_sectors = get_data(prefix + data_rate + '_' + level + '_' + datatype + '_spinsectnum' + suffix)

    spin_starts = [spin_end + 1 for spin_end in np.where(spin_sectors[:-1] >= spin_sectors[1:])[0]]

    var_name = prefix + data_rate + '_' + level + '_' + datatype + '_' + data_units + '_omni'

    times, data, energies = get_data(var_name + suffix)

    spin_avg_flux = np.zeros([len(spin_starts), len(energies)])

    current_start = spin_starts[0]
    for spin_idx in range(1, len(spin_starts)-1):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            spin_avg_flux[spin_idx-1, :] = nanmean(data[current_start:spin_starts[spin_idx]+1, :], axis=0)
        current_start = spin_starts[spin_idx] + 1

    store_data(var_name + '_spin' + suffix, data={'x': times[spin_starts], 'y': spin_avg_flux, 'v': energies})
    options(var_name + '_spin' + suffix, 'spec', True)
    options(var_name + '_spin' + suffix, 'ylog', True)
    options(var_name + '_spin' + suffix, 'zlog', True)
    options(var_name + '_spin' + suffix, 'yrange', [lower_en, 600.0])
    options(var_name + '_spin' + suffix, 'ztitle', units_label)
    options(var_name + '_spin' + suffix, 'ytitle', 'MMS' + str(probe) + ' ' + datatype)
    options(var_name + '_spin' + suffix, 'ysubtitle', '[keV]')

    return var_name + '_spin' + suffix
