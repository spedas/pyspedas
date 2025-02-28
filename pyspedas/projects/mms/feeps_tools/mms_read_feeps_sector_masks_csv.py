import csv
import os
import numpy as np
import logging
from pytplot import time_double, time_string


def mms_read_feeps_sector_masks_csv(trange):
    """
    This function returns the FEEPS sectors to mask due to sunlight contamination
    
    Parameters
    -----------
        trange : list of str
            time range of interest [start time, end time] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            
    Returns
    -----------
        Hash table containing the sectors to mask for each spacecraft and sensor ID

    """
    masks = {}

    dates = [1447200000.0000000, # 11/11/2015
             1468022400.0000000, # 7/9/2016
             1477612800.0000000, # 10/28/2016
             1496188800.0000000, # 5/31/2017
             1506988800.0000000, # 10/3/2017
             1538697600.0000000, # 10/5/2018
             1642032000.0000000, # 1/13/2022
             1651795200.0000000, # 5/6/2022
             1660521600.0000000, # 8/15/2022
             1706832000.0000000, # 02/02/2024
             1721779200.0000000, # 07/24/2024
             1739664000.0000000] # 02/16/2025

    # find the file closest to the start time
    nearest_date = dates[(np.abs(np.array(dates)-time_double(trange[0]))).argmin()]

    for mms_sc in [1, 2, 3, 4]:
        csv_filename = os.sep.join([os.path.dirname(os.path.abspath(__file__)), 'sun', 'MMS'+str(mms_sc)+'_FEEPS_ContaminatedSectors_'+time_string(nearest_date, fmt='%Y%m%d')+'.csv'])

        csv_file = open(csv_filename, 'r',encoding='utf-8-sig')
        csv_reader = csv.reader(csv_file)
        csv_data = []

        for line in csv_reader:
            try:
                csv_data.append([float(l) for l in line])
            except ValueError:
                logging.error("Trouble reading line in contamination file "+csv_filename)
                logging.error(line)
                csv_file.close()
                return
            
        csv_file.close()

        csv_data = np.array(csv_data)

        for i in range(0, 12):
            mask_vals = []
            for val_idx in range(0, len(csv_data[:, i])):
                if csv_data[val_idx, i] == 1: mask_vals.append(val_idx)
            masks['mms'+str(mms_sc)+'imaskt'+str(i+1)] = mask_vals

        for i in range(0, 12):
            mask_vals = []
            for val_idx in range(0, len(csv_data[:, i+12])):
                if csv_data[val_idx, i+12] == 1: mask_vals.append(val_idx)
            masks['mms'+str(mms_sc)+'imaskb'+str(i+1)] = mask_vals

    return masks
