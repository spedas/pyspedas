import numpy as np
from pytplot import time_double


def mms_feeps_active_eyes(trange, probe, data_rate, species, level):
    """
    This function returns the FEEPS active eyes, based on date/probe/species/rate
    
    Parameters:
        trange: list of str
            time range

        probe: str
            probe #, e.g., '4' for MMS4

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst'

        species: str
            'electron' or 'ion'

        level: str
            data level

    Returns:
        Hash table containing 2 keys:
            output['top'] -> maps to the active top eyes
            output['bottom'] -> maps to the active bottom eyes

    Notes:
         1) Burst mode should include all sensors (TOP and BOTTOM):
             electrons: [1, 2, 3, 4, 5, 9, 10, 11, 12]
             ions: [6, 7, 8]
         
         2) SITL should return (TOP only):
             electrons: set_intersection([5, 11, 12], active_eyes)
             ions: None
             
         3) From Drew Turner, 9/7/2017, srvy mode:
         
           - before 16 August 2017:
              electrons: [3, 4, 5, 11, 12]
              iond: [6, 7, 8]
         
           - after 16 August 2017:
               MMS1
                 Top Eyes: 3, 5, 6, 7, 8, 9, 10, 12
                 Bot Eyes: 2, 4, 5, 6, 7, 8, 9, 10

               MMS2
                 Top Eyes: 1, 2, 3, 5, 6, 8, 10, 11
                 Bot Eyes: 1, 4, 5, 6, 7, 8, 9, 11

               MMS3
                 Top Eyes: 3, 5, 6, 7, 8, 9, 10, 12
                 Bot Eyes: 1, 2, 3, 6, 7, 8, 9, 10

               MMS4
                 Top Eyes: 3, 4, 5, 6, 8, 9, 10, 11
                 Bot Eyes: 3, 5, 6, 7, 8, 9, 10, 12

    """
    if data_rate.lower() == 'brst' and species.lower() == 'electron': return {'top': [1, 2, 3, 4, 5, 9, 10, 11, 12], 'bottom': [1, 2, 3, 4, 5, 9, 10, 11, 12]}
    if data_rate.lower() == 'brst' and species.lower() == 'ion': return {'top': [6, 7, 8], 'bottom': [6, 7, 8]}

    # old eyes, srvy mode, prior to 16 August 2017
    if species.lower() == 'electron':
        sensors = {'top': [3, 4, 5, 11, 12], 'bottom': [3, 4, 5, 11, 12]}
    else:
        sensors = {'top': [6, 7, 8], 'bottom': [6, 7, 8]}

    if isinstance(trange[0], str): 
        start_time = time_double(trange[0])
    elif isinstance(trange[0], np.datetime64):
        start_time = np.int64(trange[0]) / 1e9
    else:
        start_time = trange[0]

    # srvy mode, after 16 August 2017
    if start_time >= time_double('2017-08-16') and data_rate.lower() == 'srvy':
        active_table = {'1-electron': {'top': [3, 5, 9, 10, 12], 'bottom': [2, 4, 5, 9, 10]}, 
        '1-ion': {'top': [6, 7, 8], 'bottom': [6, 7, 8]},
        '2-electron': {'top': [1, 2, 3, 5, 10, 11], 'bottom': [1, 4, 5, 9, 11]},
        '2-ion': {'top': [6, 8], 'bottom': [6, 7, 8]},
        '3-electron': {'top': [3, 5, 9, 10, 12], 'bottom': [1, 2, 3, 9, 10]},
        '3-ion': {'top': [6, 7, 8], 'bottom': [6, 7, 8]},
        '4-electron': {'top': [3, 4, 5, 9, 10, 11], 'bottom': [3, 5, 9, 10, 12]},
        '4-ion': {'top': [6, 8], 'bottom': [6, 7, 8]}}
        sensors = active_table[probe.lower()+'-'+species.lower()]
        if level.lower() == 'sitl':
            return {'top': list(set(sensors['top']) & set([5, 11, 12])), 'bottom': []}

    if level.lower() == 'sitl':
        return {'top': [5, 11, 12], 'bottom': []}

    return sensors
