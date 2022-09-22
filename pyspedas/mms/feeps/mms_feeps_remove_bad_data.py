import logging
import numpy as np
from pyspedas import time_string, time_double, tnames
import pytplot


def mms_feeps_remove_bad_data(probe='1', data_rate='srvy', datatype='electron', level='l2', suffix='', trange=None):
    """
    This function removes bad eyes, bad lowest energy channels based on data from Drew Turner
    
    Parameters:
        probe: str
            probe #, e.g., '4' for MMS4

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst'

        datatype: str
            'electron' or 'ion'

        level: str
            data level

        suffix: str
            suffix of the loaded data

        trange: list of str or list of float
            Time range
    Returns:
        None
    """
    if trange is None:
        logging.error('Time range required for mms_feeps_remove_bad_data.')
        return

    data_rate_level = data_rate + '_' + level

    # electrons first, remove bad eyes
    #;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; 1. BAD EYES ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    #  First, here is a list of the EYES that are bad, we need to make sure these 
    #  data are not usable (i.e., make all of the counts/rate/flux data from these eyes NAN). 
    #  These are for all modes, burst and survey:
    bad_data_table = {}
    bad_data_table['2017-10-01'] = {}
    bad_data_table['2017-10-01']['mms1'] = {'top': [1], 'bottom': [1, 11]}
    bad_data_table['2017-10-01']['mms2'] = {'top': [5, 7, 12], 'bottom': [7]}
    bad_data_table['2017-10-01']['mms3'] = {'top': [2, 12], 'bottom': [2, 5, 11]}
    bad_data_table['2017-10-01']['mms4'] = {'top': [1, 2, 7], 'bottom': [2, 4, 5, 10, 11]}

    bad_data_table['2018-10-01'] = {}
    bad_data_table['2018-10-01']['mms1'] = {'top': [1], 'bottom': [1, 11]}
    bad_data_table['2018-10-01']['mms2'] = {'top': [7, 12], 'bottom': [2, 12]}
    bad_data_table['2018-10-01']['mms3'] = {'top': [1, 2], 'bottom': [5, 11]}
    bad_data_table['2018-10-01']['mms4'] = {'top': [1, 7], 'bottom': [4, 11]}

    dates = np.asarray(time_double(list(bad_data_table.keys())))
    closest_table_tm = (np.abs(dates - time_double(trange[0]))).argmin()

    closest_table = time_string(dates[closest_table_tm], '%Y-%m-%d')
    bad_data = bad_data_table[closest_table]['mms'+probe]

    bad_vars = []

    # top electrons
    for bad_var in bad_data['top']:
        if bad_var in [6, 7, 8]: continue # ion eyes
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_top_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_top_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_top_counts_sensorid_'+str(bad_var)+suffix))

    # bottom electrons
    for bad_var in bad_data['bottom']:
        if bad_var in [6, 7, 8]: continue # ion eyes
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_bottom_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_bottom_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_bottom_counts_sensorid_'+str(bad_var)+suffix))

    # top ions
    for bad_var in bad_data['top']:
        if bad_var not in [6, 7, 8]: continue # ion eyes
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_top_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_top_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_top_counts_sensorid_'+str(bad_var)+suffix))

    # bottom ions
    for bad_var in bad_data['bottom']:
        if bad_var not in [6, 7, 8]: continue # ion eyes
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_bottom_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_bottom_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_bottom_counts_sensorid_'+str(bad_var)+suffix))

    for bad_var in bad_vars:
        if bad_var == []: continue
        bad_var_data = pytplot.get_data(bad_var[0])

        if bad_var_data is not None:
            times, data, energies = bad_var_data
            data[:] = np.nan
            pytplot.store_data(bad_var[0], data={'x': times, 'y': data, 'v': energies})

    # ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; 2. BAD LOWEST E-CHANNELS ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    # ; Next, these eyes have bad first channels (i.e., lowest energy channel, E-channel 0 in IDL indexing).  
    # ; Again, these data (just the counts/rate/flux from the lowest energy channel ONLY!!!) 
    # ; should be hardwired to be NAN for all modes (burst and both types of survey).  
    # ; The eyes not listed here or above are ok though... so once we do this, we can actually start 
    # ; showing the data down to the lowest levels (~33 keV), meaning we'll have to adjust the hard-coded 
    # ; ylim settings in SPEDAS and the SITL software:

    # ; from Drew Turner, 5Oct18:
    # ;Bad Channels (0 and 1):
    # ;Update: All channels 0 (Ch0) on MMS-2, -3, and -4 electron eyes (1, 2, 3, 4, 5, 9, 10, 11, 12) should be NaN
    # ;Additionally, the second channels (Ch1) on the following should also be made NaN:
    # ;MMS-1: Top: Ch0 on Eyes 6, 7
    # ;Bot: Ch0 on Eyes 6, 7, 8
    # ;MMS-2: Top:
    # ;Bot: Ch0 on Eyes 6, 8
    # ;MMS-3: Top: Ch0 on Eye 8
    # ;Bot: Ch0 on Eyes 6, 7
    # ;MMS-4: Top: Ch1 on Eye 1; Ch0 on Eye 8
    # ;Bot: Ch0 on Eyes 6, 7, 8; Ch1 on Eye 9

    bad_vars = []
    bad_vars_both_chans = []
    bad_vars_3_chans = []

    # -- the following are the pre-May 2019 masks
    # bad_ch0 = {}
    # bad_ch0['mms1'] = {'top': [2, 5, 6, 7], 'bottom': [2, 3, 4, 5, 6, 7, 8, 9, 11, 12]}
    # bad_ch0['mms2'] = {'top': [1, 2, 3, 4, 5, 9, 10, 11, 12], 'bottom': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]}
    # bad_ch0['mms3'] = {'top': [1, 2, 3, 4, 5, 8, 9, 10, 11, 12], 'bottom': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12]}
    # bad_ch0['mms4'] = {'top': [1, 2, 3, 4, 5, 8, 9, 10, 11, 12], 'bottom': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}

    # bad_ch1 = {}
    # bad_ch1['mms1'] = {'top': [], 'bottom': [11]}
    # bad_ch1['mms2'] = {'top': [8], 'bottom': [12]}
    # bad_ch1['mms3'] = {'top': [1], 'bottom': []}
    # bad_ch1['mms4'] = {'top': [1], 'bottom': [6, 9]}

    # -- the following are the post-May 2019 masks
    bad_ch0 = {}
    bad_ch0['mms1'] = {'top': [2, 5, 6], 'bottom': [2, 3, 4, 5, 6, 8, 9, 11, 12]}
    bad_ch0['mms2'] = {'top': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12], 'bottom': [1, 2, 3, 4, 5, 7, 9, 10, 11, 12]}
    bad_ch0['mms3'] = {'top': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'bottom': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12]}
    bad_ch0['mms4'] = {'top': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12], 'bottom': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}

    bad_ch1 = {}
    bad_ch1['mms1'] = {'top': [6], 'bottom': [6, 11]}
    bad_ch1['mms2'] = {'top': [8], 'bottom': [7, 12]}
    bad_ch1['mms3'] = {'top': [1, 6, 7], 'bottom': [6, 7]}
    bad_ch1['mms4'] = {'top': [1, 6], 'bottom': [6, 7, 8, 9]}

    bad_ch2 = {}
    bad_ch2['mms1'] = {'top': [], 'bottom': []}
    bad_ch2['mms2'] = {'top': [], 'bottom': []}
    bad_ch2['mms3'] = {'top': [], 'bottom': []}
    bad_ch2['mms4'] = {'top': [], 'bottom': [6, 7]}

    bad_ch0 = bad_ch0['mms'+str(probe)]
    bad_ch1 = bad_ch1['mms'+str(probe)]
    bad_ch2 = bad_ch2['mms'+str(probe)]

    #### bottom channel

    # top electrons
    for bad_var in bad_ch0['top']:
        if bad_var in [6, 7, 8]: continue # ion eyes
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_top_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_top_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_top_counts_sensorid_'+str(bad_var)+suffix))

    # bottom electrons
    for bad_var in bad_ch0['bottom']:
        if bad_var in [6, 7, 8]: continue # ion eyes
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_bottom_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_bottom_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_bottom_counts_sensorid_'+str(bad_var)+suffix))

    # top ions
    for bad_var in bad_ch0['top']:
        if bad_var not in [6, 7, 8]: continue # ion eyes
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_top_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_top_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_top_counts_sensorid_'+str(bad_var)+suffix))

    # bottom ions
    for bad_var in bad_ch0['bottom']:
        if bad_var not in [6, 7, 8]: continue # ion eyes
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_bottom_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_bottom_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_bottom_counts_sensorid_'+str(bad_var)+suffix))


    #### bottom 2 channels

    # top electrons
    for bad_var in bad_ch1['top']:
        if bad_var in [6, 7, 8]: continue # ion eyes
        bad_vars_both_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_top_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars_both_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_top_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars_both_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_top_counts_sensorid_'+str(bad_var)+suffix))

    # bottom electrons
    for bad_var in bad_ch1['bottom']:
        if bad_var in [6, 7, 8]: continue # ion eyes
        bad_vars_both_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_bottom_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars_both_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_bottom_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars_both_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_bottom_counts_sensorid_'+str(bad_var)+suffix))

    # top ions
    for bad_var in bad_ch1['top']:
        if bad_var not in [6, 7, 8]: continue # ion eyes
        bad_vars_both_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_top_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars_both_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_top_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars_both_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_top_counts_sensorid_'+str(bad_var)+suffix))

    # bottom ions
    for bad_var in bad_ch1['bottom']:
        if bad_var not in [6, 7, 8]: continue # ion eyes
        bad_vars_both_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_bottom_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars_both_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_bottom_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars_both_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_bottom_counts_sensorid_'+str(bad_var)+suffix))


    #### bottom 3 channels

    # top electrons
    for bad_var in bad_ch2['top']:
        if bad_var in [6, 7, 8]: continue # ion eyes
        bad_vars_3_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_top_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars_3_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_top_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars_3_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_top_counts_sensorid_'+str(bad_var)+suffix))

    # bottom electrons
    for bad_var in bad_ch2['bottom']:
        if bad_var in [6, 7, 8]: continue # ion eyes
        bad_vars_3_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_bottom_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars_3_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_bottom_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars_3_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_electron_bottom_counts_sensorid_'+str(bad_var)+suffix))

    # top ions
    for bad_var in bad_ch2['top']:
        if bad_var not in [6, 7, 8]: continue # ion eyes
        bad_vars_3_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_top_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars_3_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_top_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars_3_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_top_counts_sensorid_'+str(bad_var)+suffix))

    # bottom ions
    for bad_var in bad_ch2['bottom']:
        if bad_var not in [6, 7, 8]: continue # ion eyes
        bad_vars_3_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_bottom_count_rate_sensorid_'+str(bad_var)+suffix))
        bad_vars_3_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_bottom_intensity_sensorid_'+str(bad_var)+suffix))
        bad_vars_3_chans.append(tnames('mms'+str(probe)+'_epd_feeps_'+data_rate_level+'_ion_bottom_counts_sensorid_'+str(bad_var)+suffix))

    # set the first energy channel to NaN
    for bad_var in bad_vars:
        if bad_var == []: continue
        bad_var_data = pytplot.get_data(bad_var[0])
        if bad_var_data is not None:
            times, data, energies = bad_var_data

            # check if the energy table contains all nans
            if np.isnan(np.sum(energies)): continue

            data[:, 0] = np.nan
            pytplot.store_data(bad_var[0], data={'x': times, 'y': data, 'v': energies})

    # set the first and second energy channels to NaN
    for bad_var in bad_vars_both_chans:
        if bad_var == []: continue
        bad_var_data = pytplot.get_data(bad_var[0])
        if bad_var_data is not None:
            times, data, energies = bad_var_data

            # check if the energy table contains all names
            if np.isnan(np.sum(energies)): continue

            data[:, 0] = np.nan
            data[:, 1] = np.nan
            pytplot.store_data(bad_var[0], data={'x': times, 'y': data, 'v': energies})

    # set the bottom 3 energy channels to NaN
    for bad_var in bad_vars_3_chans:
        if bad_var == []: continue
        bad_var_data = pytplot.get_data(bad_var[0])
        if bad_var_data is not None:
            times, data, energies = bad_var_data

            # check if the energy table contains all names
            if np.isnan(np.sum(energies)): continue

            data[:, 0] = np.nan
            data[:, 1] = np.nan
            data[:, 2] = np.nan
            pytplot.store_data(bad_var[0], data={'x': times, 'y': data, 'v': energies})
