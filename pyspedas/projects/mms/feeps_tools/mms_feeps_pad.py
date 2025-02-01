import logging
import warnings
import numpy as np
from pytplot import get, store, options
from pyspedas.projects.mms.feeps_tools.mms_feeps_pitch_angles import mms_feeps_pitch_angles
from pyspedas.projects.mms.feeps_tools.mms_feeps_active_eyes import mms_feeps_active_eyes
from pyspedas.projects.mms.feeps_tools.mms_feeps_pad_spinavg import mms_feeps_pad_spinavg

# use nanmean from bottleneck if it's installed, otherwise use the numpy one
# bottleneck nanmean is ~2.5x faster
try:
    import bottleneck as bn
    nanmean = bn.nanmean
except ImportError:
    nanmean = np.nanmean

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def mms_feeps_pad(bin_size=16.3636, probe='1', energy=[70, 600], level='l2', suffix='', datatype='electron', data_units='intensity', data_rate='srvy', angles_from_bfield=False):
    """
    This function will calculate pitch angle distributions using data from the MMS Fly's Eye Energetic Particle Sensor (FEEPS)
    
    Parameters
    ----------
        probe: str
            probe #, e.g., '4' for MMS4

        data_units: str
            'intensity' 

        datatype: str
            'electron' or 'ion'

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst'

        level: str
            data level

        suffix: str
            suffix of the loaded data

        energy: list of float
            energy range to include in the calculation

        bin_size: float
            size of the pitch angle bins
            
        angles_from_bfield: bool
            calculate the pitch angles from the B-field data instead of reading from the CDFs

    Returns
    --------
        List of tplot variables created.
    """

    # account for angular response (finite field of view) of instruments
    # electrons can use +/- 21.4 deg on each pitch angle as average response angle; ions can start with +/-10 deg, but both need to be further refined
    if datatype == 'electron':
        dangresp = 21.4 # deg
    elif datatype == 'ion': 
        dangresp = 10.0 # deg

    if energy[0] < 32.0:
        logging.error('Please select a starting energy of 32 keV or above')
        return

    units_label = ''
    if data_units == 'intensity':
        units_label = '1/(cm^2-sr-s-keV)'
    elif data_units == 'counts':
        units_label = '[counts/s]'
    
    if not isinstance(probe, str):
        probe = str(probe)

    prefix = 'mms' + probe
    n_pabins = 180/bin_size
    pa_bins = [180.*pa_bin/n_pabins for pa_bin in range(0, int(n_pabins)+1)]
    pa_label = [180.*pa_bin/n_pabins+bin_size/2. for pa_bin in range(0, int(n_pabins))]

    if data_rate == 'brst' and angles_from_bfield == False:
        # v5.5+ = mms1_epd_feeps_srvy_l2_electron_pitch_angle
        pad_pas = get(prefix+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_pitch_angle'+suffix)
        if pad_pas is None:
            logging.error("Error reading variable containing FEEPS pitch angles")
            return
        pa_times = pad_pas[0]
        pa_data = pad_pas[1]
    else:
        feeps_pa_data = mms_feeps_pitch_angles(probe=probe, level=level, data_rate=data_rate, datatype=datatype, suffix=suffix)
        if feeps_pa_data is None:
            return
        pa_var, idx_maps = feeps_pa_data
        pa_times, pa_data = get(pa_var)

    if pa_data is None:
        logging.error("Error, couldn't find the PA variable")
        return

    eyes = mms_feeps_active_eyes([pa_times.min(), pa_times.max()], probe, data_rate, datatype, level)

    pa_data_map = {}

    if data_rate == 'srvy':
        if datatype == 'electron': 
            pa_data_map['top-electron'] = idx_maps['electron-top']
            pa_data_map['bottom-electron'] = idx_maps['electron-bottom']
        if datatype == 'ion':
            pa_data_map['top-ion'] = idx_maps['ion-top']
            pa_data_map['bottom-ion'] = idx_maps['ion-bottom']
    elif data_rate == 'brst':
        # note: the following are indices of the top/bottom sensors in pa_data
        # they should be consistent with pa_dlimits.labels
        pa_data_map['top-electron'] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        pa_data_map['bottom-electron'] = [9, 10, 11, 12, 13, 14, 15, 16, 17]
        # and ions:
        pa_data_map['top-ion'] = [0, 1, 2]
        pa_data_map['bottom-ion'] = [3, 4, 5]

    sensor_types = ['top', 'bottom']

    if datatype == 'electron':
        dflux = np.zeros([len(pa_times), len(pa_data_map['top-electron'])+len(pa_data_map['bottom-electron'])])
        dpa = np.zeros([len(pa_times), len(pa_data_map['top-electron'])+len(pa_data_map['bottom-electron'])])
    elif datatype == 'ion':
        dflux = np.zeros([len(pa_times), len(pa_data_map['top-ion'])+len(pa_data_map['bottom-ion'])])
        dpa = np.zeros([len(pa_times), len(pa_data_map['top-ion'])+len(pa_data_map['bottom-ion'])])

    for s_type in sensor_types:
        pa_map = pa_data_map[s_type+'-'+datatype]
        particle_idxs = [eye-1 for eye in eyes[s_type]]
        for isen, sensor_num in enumerate(particle_idxs):
            var_name = 'mms'+str(probe)+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_'+s_type+'_'+data_units+'_sensorid_'+str(sensor_num+1)+'_clean_sun_removed'+suffix
            times, data, energies = get(var_name)
            data[data == 0] = 'nan' # remove any 0s before averaging
            if np.isnan(energies[0]): # assumes all energies are NaNs if the first is
                continue
            # energy indices to use:
            indx = np.where((energies >= energy[0]) & (energies <= energy[1]))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                dflux[:, pa_map[isen]] = nanmean(data[:, indx[0]], axis=1)
            dpa[:, pa_map[isen]] = pa_data[:, pa_map[isen]]

    # we need to replace the 0.0s left in after populating dpa with NaNs; these 
    # 0.0s are left in there because these points aren't covered by sensors loaded
    # for this datatype/data_rate
    dpa[dpa == 0] = 'nan'

    pa_flux = np.zeros([len(pa_times), int(n_pabins)])
    delta_pa = (pa_bins[1]-pa_bins[0])/2.0

    # Now loop through PA bins and time, find the telescopes where there is data in those bins and average it up!
    for pa_idx, pa_time in enumerate(pa_times):
        for ipa in range(0, int(n_pabins)):
            if not np.isnan(dpa[pa_idx, :][0]):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    ind = np.argwhere((dpa[pa_idx, :] + dangresp >= pa_label[ipa]-delta_pa) & (dpa[pa_idx, :]-dangresp < pa_label[ipa]+delta_pa)).flatten()
                    if ind.size != 0:
                        if len(ind) > 1:
                            pa_flux[pa_idx, ipa] = nanmean(dflux[pa_idx, ind], axis=0)
                        else:
                            pa_flux[pa_idx, ipa] = dflux[pa_idx, ind[0]]

    pa_flux[pa_flux == 0] = 'nan' # fill any missed bins with NAN

    en_range_string = str(int(energy[0])) + '-' + str(int(energy[1])) + 'keV'
    new_name = 'mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_'+data_units+'_'+ en_range_string +'_pad'+suffix

    store(new_name, data={'x': times, 'y': pa_flux, 'v': pa_label})
    options(new_name, 'ylog', False)
    options(new_name, 'zlog', True)
    options(new_name, 'spec', True)
    options(new_name, 'ztitle', units_label)
    options(new_name, 'ytitle', 'MMS' + str(probe) + ' ' + datatype + ' PA')
    options(new_name, 'ysubtitle', '[deg]')

    # create the spin-averaged PAD
    spin_avg_var = mms_feeps_pad_spinavg(probe=probe, data_units=data_units, datatype=datatype, data_rate=data_rate, level=level, suffix=suffix, energy=energy, bin_size=bin_size)
    
    return [new_name, spin_avg_var]
