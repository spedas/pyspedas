import logging
import numpy as np
import pyspedas 
from pytplot import get, store, options
from pyspedas.projects.mms.feeps_tools.mms_feeps_active_eyes import mms_feeps_active_eyes
from pyspedas.projects.mms.feeps_tools.mms_feeps_getgyrophase import mms_feeps_getgyrophase

# use nanmean from bottleneck if it's installed, otherwise use the numpy one
# bottleneck nanmean is ~2.5x faster
try:
    import bottleneck as bn
    nanmean = bn.nanmean
except ImportError:
    nanmean = np.nanmean


def mms_feeps_gpd(trange=['2017-07-11/22:30', '2017-07-11/22:35'], 
                  probe='2', 
                  data_rate='brst', 
                  level='l2', 
                  datatype='electron',
                  data_units='intensity',
                  bin_size=15, # deg
                  energy=[50, 500]):
    """
    Calculate gyrophase distributions using data from the MMS Fly's Eye Energetic Particle Sensor (FEEPS)

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

    Returns
    --------
        Tplot variable containing the gyrophase distribution

    Notes
    ------
        Based on IDL code by Drew Turner (10 Oct 2017): mms_feeps_gpd.pro
    """

    if isinstance(probe, int):
        probe = str(probe)

    feeps_data = pyspedas.projects.mms.feeps(trange=trange, data_rate=data_rate, probe=probe, level=level)

    if len(feeps_data) == 0:
        logging.error('Problem loading FEEPS data for this time range.')
        return

    # Account for angular response (finite field of view) of instruments
    # elec can use +/-21.4 deg on each pitch angle as average response angle; ions can start with +/-10 deg, but both need to be further refined
    if datatype == 'electron': dAngResp = 21.4 # [deg] 
    if datatype == 'ion': dAngResp = 10.0 # [deg]

    bin_size = float(bin_size)
    n_bins = 360.0/bin_size
    gyro_bins = 360.*np.arange(n_bins+1)/n_bins
    gyro_centers = 360.*np.arange(n_bins)/n_bins+(gyro_bins[1]-gyro_bins[0])/2.

    # get the gyrophase angles
    # calculate the gyro phase angles from the magnetic field data
    gyro_vars = mms_feeps_getgyrophase(trange=trange, probe=probe, data_rate=data_rate, level=level, datatype=datatype)
    gyro_data = get('mms' + str(probe) + '_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_gyrophase')

    if gyro_data is None or gyro_vars is None:
        logging.error('Problem calculating gyrophase angles.')
        return

    eyes = mms_feeps_active_eyes(trange, probe, data_rate, datatype, level)

    data_map = {}

    if data_rate == 'srvy':
        # From Allison Jaynes @ LASP: The 6,7,8 sensors (out of 12) are ions,
        # so in the pitch angle array, the 5,6,7 columns (counting from zero) will be the ion pitch angles.
        # for electrons:
        if datatype == 'electron': 
            data_map['top-electron'] = eyes['top']-1
            data_map['bottom-electron'] = eyes['bottom']-1
        elif datatype == 'ion':
            data_map['top-ion'] = eyes['top']-1
            data_map['bottom-ion'] = eyes['bottom']-1
    elif data_rate == 'brst':
        # note: the following are indices of the top/bottom sensors in pa_data
        # they should be consistent with pa_dlimits.labels
        data_map['top-electron'] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        data_map['bottom-electron'] = [9, 10, 11, 12, 13, 14, 15, 16, 17]
        # and ions:
        data_map['top-ion'] = [0, 1, 2]
        data_map['bottom-ion'] = [3, 4, 5]

    sensor_types = ['top', 'bottom']

    # First, initialize arrays for flux (dflux) and pitch angles (dpa) compiled from all sensors:
    if datatype == 'electron':
        dflux = np.zeros((len(gyro_data.times), len(data_map['top-electron']) + len(data_map['bottom-electron'])))
    elif datatype == 'ion':
        dflux = np.zeros((len(gyro_data.times), len(data_map['top-ion']) + len(data_map['bottom-ion'])))

    dpa = np.zeros(dflux.shape)

    for sensor_type in sensor_types:
        pa_map = data_map[sensor_type + '-' + datatype]
        particle_idxs = np.array(eyes[sensor_type])-1

        for isen in range(len(particle_idxs)): # loop through sensors
            # get the data
            var_name = 'mms' + str(probe) + '_epd_feeps_' + data_rate + '_' + level + '_' + datatype + '_' + sensor_type + '_' + data_units + '_sensorid_' + str(particle_idxs[isen]+1) + '_clean_sun_removed'
            data = get(var_name)
            if data is None:
                logging.error('Data not found: ' + var_name)
                continue
            data.y[data.y == 0.0] = np.nan # remove any 0s before averaging
            # Energy indices to use:
            indx = np.argwhere((data.v <= energy[1]) & (data.v >= energy[0]))
            if len(indx) == 0:
                logging.error('Energy range selected is not covered by the detector for FEEPS ' + datatype + ' data')
                continue
            dflux[:, pa_map[isen]] = nanmean(data.y[:, indx], axis=1).flatten()
            dpa[:, pa_map[isen]] = gyro_data.y[:,  pa_map[isen]].flatten()

    # we need to replace the 0.0s left in after populating dpa with NaNs; these 
    # 0.0s are left in there because these points aren't covered by sensors loaded
    # for this datatype/data_rate
    dpa[dpa == 0.0] = np.nan

    gyro_flux = np.zeros((len(gyro_data.times), int(n_bins)))
    delta_gyro = (gyro_bins[1]-gyro_bins[0])/2.0

    # Now loop through PA bins and time, find the telescopes where there is data in those bins and average it up!
    for it in range(len(dpa[:, 0])):
        for ipa in range(int(n_bins)):
            ind = np.argwhere((dpa[it, :] + dAngResp >= gyro_centers[ipa]-delta_gyro) & (dpa[it, :] - dAngResp < gyro_centers[ipa]+delta_gyro)).flatten()
            if ind.size != 0:
                if len(ind) > 1:
                    gyro_flux[it, ipa] = nanmean(dflux[it, ind])
                else:
                    gyro_flux[it, ipa] = dflux[it, ind[0]]
            #if len(ind) > 0:
            #   gyro_flux[it, ipa] = np.nanmean(dflux[it, ind], axis=0).flatten()

    # fill any missed bins with NAN
    gyro_flux[gyro_flux == 0.0] = np.nan 

    en_range_string = str(int(energy[0])) + '-' + str(int(energy[1])) + 'keV'

    new_name = 'mms' + str(probe) + '_epd_feeps_' + data_rate + '_' + level + '_' + datatype + '_' + data_units + '_' + en_range_string + '_gpd'

    saved = store(new_name, data={'x': gyro_data.times, 'y': gyro_flux, 'v': gyro_centers})

    if saved:
        options(new_name, 'spec', True)
        options(new_name, 'zlog', False)
        return new_name
