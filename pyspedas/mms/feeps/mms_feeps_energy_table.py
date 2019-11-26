import numpy as np

def mms_feeps_energy_table(probe, eye, sensor_id):
    """
    This function returns the energy table based on
    each spacecraft and eye; based on the table from:

       FlatFieldResults_V3.xlsx
       
    from Drew Turner, 1/19/2017
    
    Parameters:
        probe: str
            probe #, e.g., '4' for MMS4

        eye: str
            sensor eye #

        sensor_id: int
            sensor ID

    Returns:
        Energy table 

    Notes:
        BAD EYES are replaced by NaNs

        - different original energy tables are used depending on if the sensor head is 6-8 (ions) or not (electrons)

        Electron Eyes: 1, 2, 3, 4, 5, 9, 10, 11, 12
        Ion Eyes: 6, 7, 8
    """

    table = {}
    table['mms1-top'] = [14.0, 7.0, 16.0, 14.0, 14.0, 0.0, 0.0, 0.0, 14.0, 14.0, 17.0, 15.0]
    table['mms1-bot'] = [np.nan, 14.0, 14.0, 13.0, 14.0, 0.0, 0.0, 0.0, 14.0, 14.0, -25.0, 14.0]

    table['mms2-top'] = [-1.0, 6.0, -2.0, -1.0, np.nan, 0.0, np.nan, 0.0, 4.0, -1.0, -1.0, 0.0]
    table['mms2-bot'] = [-2.0, -1.0, -2.0, 0.0, -2.0, 15.0, np.nan, 15.0, -1.0, -2.0, -1.0, -3.0]

    table['mms3-top'] = [-3.0, np.nan, 2.0, -1.0, -5.0, 0.0, 0.0, 0.0, -3.0, -1.0, -3.0, np.nan]
    table['mms3-bot'] = [-7.0, np.nan, -5.0, -6.0, np.nan, 0.0, 0.0, 12.0, 0.0, -2.0, -3.0, -3.0]

    table['mms4-top'] = [np.nan, np.nan, -2.0, -5.0, -5.0, 0.0, np.nan, 0.0, -1.0, -3.0, -6.0, -6.0]
    table['mms4-bot'] = [-8.0, np.nan, -2.0, np.nan, np.nan, -8.0, 0.0, 0.0, -2.0, np.nan, np.nan, -4.0]

    if sensor_id >= 6 and sensor_id <= 8:
        mms_energies = [57.900000, 76.800000, 95.400000, 114.10000, 133.00000, 153.70000, 177.60000, 
            205.10000, 236.70000, 273.20000, 315.40000, 363.80000, 419.70000, 484.20000,  558.60000,  609.90000]
    else:
        mms_energies = [33.200000, 51.900000, 70.600000, 89.400000, 107.10000, 125.20000, 146.50000, 171.30000, 
            200.20000, 234.00000, 273.40000, 319.40000, 373.20000, 436.00000, 509.20000, 575.80000]

    return [energy+ table['mms'+probe+'-'+eye][sensor_id-1] for energy in mms_energies]