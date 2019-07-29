
import pytplot

def mms_feeps_split_integral_ch(units_type, species, probe, suffix='', data_rate='srvy', level='l2', sensor_eyes=None):
    if sensor_eyes is None:
        print('Error: sensor_eyes not defined')
        return

    top_sensors = sensor_eyes['top']
    bot_sensors = sensor_eyes['bottom']

    for sensor in top_sensors:
        top_name = 'mms'+str(probe)+'_epd_feeps_'+data_rate+'_'+level+'_'+species+'_top_'+units_type+'_sensorid_'+str(sensor)

        time, data, energies = pytplot.get_data(top_name+suffix)

        top_name_out = top_name+'_clean'+suffix
        pytplot.store_data(top_name_out, data={'x': time, 'y': data[:, :-1], 'v': energies[:-1]})

        pytplot.store_data(top_name+'_500keV_int'+suffix, data={'x': time, 'y': data[:, -1]})

        pytplot.del_data(top_name)

    if level == 'sitl': # SITL only has top sensors
        return

    for sensor in bot_sensors:
        bot_name = 'mms'+str(probe)+'_epd_feeps_'+data_rate+'_'+level+'_'+species+'_bottom_'+units_type+'_sensorid_'+str(sensor)

        time, data, energies = pytplot.get_data(bot_name+suffix)

        bot_name_out = bot_name+'_clean'+suffix
        pytplot.store_data(bot_name_out, data={'x': time, 'y': data[:, :-1], 'v': energies[:-1]})

        pytplot.store_data(bot_name+'_500keV_int'+suffix, data={'x': time, 'y': data[:, -1]})

        pytplot.del_data(bot_name)
