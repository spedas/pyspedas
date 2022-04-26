
import logging
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

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def mms_feeps_omni(eyes, probe='1', datatype='electron', data_units='intensity', data_rate='srvy', level='l2', suffix=''):
    """
    This function will calculate the omni-directional FEEPS spectrograms, and is automatically called from mms_load_feeps
    
    Parameters:
        eyes: dict
            Hash table containing the active sensor eyes

        probe: str
            probe #, e.g., '4' for MMS4

        datatype: str
            'electron' or 'ion'

        data_units: str
            'intensity'

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst'

        level: str
            data level

        suffix: str
            suffix of the loaded data

    Returns:
        List of tplot variables created.
    """

    out_vars = []
    units_label = ''
    if data_units == 'intensity':
        units_label = '1/(cm^2-sr-s-keV)'
    elif data_units == 'counts':
        units_label = '[counts/s]'

    prefix = 'mms'+probe+'_epd_feeps_'
    if datatype == 'electron':
        energies = np.array([33.2, 51.90, 70.6, 89.4, 107.1, 125.2, 146.5, 171.3,
                    200.2, 234.0, 273.4, 319.4, 373.2, 436.0, 509.2])
    else:
        energies = np.array([57.9, 76.8, 95.4, 114.1, 133.0, 153.7, 177.6,
                    205.1, 236.7, 273.2, 315.4, 363.8, 419.7, 484.2,  558.6])

    # set unique energy bins per spacecraft; from DLT on 31 Jan 2017
    eEcorr = [14.0, -1.0, -3.0, -3.0]
    iEcorr = [0.0, 0.0, 0.0, 0.0]
    eGfact = [1.0, 1.0, 1.0, 1.0]
    iGfact = [0.84, 1.0, 1.0, 1.0]

    if probe == '1' and datatype == 'electron':
        energies = energies + eEcorr[0]
    if probe == '2' and datatype == 'electron':
        energies = energies + eEcorr[1]
    if probe == '3' and datatype == 'electron':
        energies = energies + eEcorr[2]
    if probe == '4' and datatype == 'electron':
        energies = energies + eEcorr[3]

    if probe == '1' and datatype == 'ion':
        energies = energies + iEcorr[0]
    if probe == '2' and datatype == 'ion':
        energies = energies + iEcorr[1]
    if probe == '3' and datatype == 'ion':
        energies = energies + iEcorr[2]
    if probe == '4' and datatype == 'ion':
        energies = energies + iEcorr[3]

    # percent error around energy bin center to accept data for averaging; 
    # anything outside of energies[i] +/- en_chk*energies[i] will be changed 
    # to NAN and not averaged   
    en_chk = 0.10

    top_sensors = eyes['top']
    bot_sensors = eyes['bottom']

    tmpdata = get_data(prefix+data_rate+'_'+level+'_'+datatype+'_top_'+data_units+'_sensorid_'+str(top_sensors[0])+'_clean_sun_removed'+suffix)

    if tmpdata is not None:
        if level != 'sitl':
            dalleyes = np.empty((len(tmpdata[0]), len(tmpdata[2]), len(top_sensors)+len(bot_sensors)))
            dalleyes[:] = np.nan

            for idx, sensor in enumerate(top_sensors):
                var_name = prefix+data_rate+'_'+level+'_'+datatype+'_top_'+data_units+'_sensorid_'+str(sensor)+'_clean_sun_removed'+suffix
                data = get_data(var_name)
                dalleyes[:, :, idx] = data[1]
                try:
                    iE = np.where(np.abs(energies-data[2]) > en_chk*energies)
                    if iE[0].size != 0:
                        dalleyes[:, iE[0], idx] = np.nan
                except Warning:
                    logging.warning('NaN in energy table encountered; sensor T' + str(sensor))
            for idx, sensor in enumerate(bot_sensors):
                var_name = prefix+data_rate+'_'+level+'_'+datatype+'_bottom_'+data_units+'_sensorid_'+str(sensor)+'_clean_sun_removed'+suffix
                data = get_data(var_name)
                dalleyes[:, :, idx+len(top_sensors)] = data[1]
                try:
                    iE = np.where(np.abs(energies-data[2]) > en_chk*energies)
                    if iE[0].size != 0:
                        dalleyes[:, iE[0], idx+len(top_sensors)] = np.nan
                except Warning:
                    logging.warning('NaN in energy table encountered; sensor B' + str(sensor))
        else: # sitl data
            dalleyes = np.empty((len(tmpdata[0]), len(tmpdata[2]), len(top_sensors)))
            dalleyes[:] = np.nan

            for idx, sensor in enumerate(top_sensors):
                var_name = prefix+data_rate+'_'+level+'_'+datatype+'_top_'+data_units+'_sensorid_'+str(sensor)+'_clean_sun_removed'+suffix
                data = get_data(var_name)
                dalleyes[:, :, idx] = data[1]
                iE = np.where(np.abs(energies-data[2]) > en_chk*energies)
                if iE[0].size != 0:
                    dalleyes[:, iE[0], idx] = np.nan

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            flux_omni = nanmean(dalleyes, axis=2)

        if probe == '1' and datatype == 'electron':
            flux_omni = flux_omni*eGfact[0]
        if probe == '2' and datatype == 'electron':
            flux_omni = flux_omni*eGfact[1]
        if probe == '3' and datatype == 'electron':
            flux_omni = flux_omni*eGfact[2]
        if probe == '4' and datatype == 'electron':
            flux_omni = flux_omni*eGfact[3]

        if probe == '1' and datatype == 'ion':
            flux_omni = flux_omni*iGfact[0]
        if probe == '2' and datatype == 'ion':
            flux_omni = flux_omni*iGfact[1]
        if probe == '3' and datatype == 'ion':
            flux_omni = flux_omni*iGfact[2]
        if probe == '4' and datatype == 'ion':
            flux_omni = flux_omni*iGfact[3]

        store_data('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_'+data_units+'_omni'+suffix, data={'x': tmpdata[0], 'y': flux_omni, 'v': energies})
        options('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_'+data_units+'_omni'+suffix, 'spec', True)
        options('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_'+data_units+'_omni'+suffix, 'ylog', True)
        options('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_'+data_units+'_omni'+suffix, 'zlog', True)
        options('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_'+data_units+'_omni'+suffix, 'Colormap', 'spedas')
        options('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_'+data_units+'_omni'+suffix, 'ztitle', units_label)
        options('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_'+data_units+'_omni'+suffix, 'ytitle', 'MMS' + str(probe) + ' ' + datatype)
        options('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_'+data_units+'_omni'+suffix, 'ysubtitle', '[keV]')
        out_vars.append('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_'+data_units+'_omni'+suffix)

    return out_vars





