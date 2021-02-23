
import logging
import pytplot

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def mms_feeps_split_integral_ch(units_type, species, probe, suffix='', data_rate='srvy', level='l2', sensor_eyes=None):
    """
    This function splits the last integral channel from the FEEPS spectra, 
    creating 2 new tplot variables:

       [original variable]_clean - spectra with the integral channel removed
       [original variable]_500keV_int - the integral channel that was removed
    
    Parameters:
        units_type: str
            instrument datatype, e.g., 'intensity'

        species: str
            'electron' or 'ion'

        probe: str
            probe #, e.g., '4' for MMS4

        suffix: str
            suffix of the loaded data

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst'

        level: str
            data level

        sensor_eyes: dict
            Hash table containing the active sensor eyes

    Returns:
        List of tplot variables created.
    """

    if sensor_eyes is None:
        logging.error('Error: sensor_eyes not defined')
        return

    out_vars = []

    top_sensors = sensor_eyes['top']
    bot_sensors = sensor_eyes['bottom']

    for sensor in top_sensors:
        top_name = 'mms'+str(probe)+'_epd_feeps_'+data_rate+'_'+level+'_'+species+'_top_'+units_type+'_sensorid_'+str(sensor)

        time, data, energies = pytplot.get_data(top_name+suffix)

        top_name_out = top_name+'_clean'+suffix
        try:
            pytplot.store_data(top_name_out, data={'x': time, 'y': data[:, :-1], 'v': energies[:-1]})
            pytplot.store_data(top_name+'_500keV_int'+suffix, data={'x': time, 'y': data[:, -1]})
            out_vars.append(top_name_out)
            out_vars.append(top_name+'_500keV_int'+suffix)
        except Warning:
            continue

        pytplot.del_data(top_name+suffix)

    if level == 'sitl': # SITL only has top sensors
        return

    for sensor in bot_sensors:
        bot_name = 'mms'+str(probe)+'_epd_feeps_'+data_rate+'_'+level+'_'+species+'_bottom_'+units_type+'_sensorid_'+str(sensor)

        time, data, energies = pytplot.get_data(bot_name+suffix)

        bot_name_out = bot_name+'_clean'+suffix
        try:
            pytplot.store_data(bot_name_out, data={'x': time, 'y': data[:, :-1], 'v': energies[:-1]})
            pytplot.store_data(bot_name+'_500keV_int'+suffix, data={'x': time, 'y': data[:, -1]})
            out_vars.append(bot_name_out)
            out_vars.append(bot_name+'_500keV_int'+suffix)
        except Warning:
            continue

        pytplot.del_data(bot_name+suffix)

    return out_vars