# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

import os
import datetime
import numpy as np
import xarray as xr
import pytplot
import copy

def sts_to_tplot(sts_file=None, read_only=False, prefix='', suffix='', merge=True, notplot=False):
    """
    Read in a given filename in situ file into a dictionary object
    Optional keywords maybe used to downselect instruments returned
     and the time windows.

    Input:
        filename: str/list of str
            The file names and full paths of STS files to be read and parsed.
        read_only: boolean
            If True, just reads data into dict and returns the dict.
            If False, loads data into dict and loads data in the dict into tplot variables.
        prefix: str
            The tplot variable names will be given this prefix.  By default,
            no prefix is added.
        suffix: str
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.
    Output:
        Either a dictionary (data structure) containing up to all of the columns included
        in a STS data file, or tplot variable names.
    """

    # List of headers present in MAG STS file
    headers = ['year', 'doy', 'hour', 'min', 'sec', 'msec', 'dday', 'outboard_b_j2000_x',
               'outboard_b_j2000_y', 'outboard_b_j2000_z', 'outboard_b_j2000_range', 'sc_posn_x', 'sc_posn_y',
               'sc_posn_z', 'outboard_bd_payload_x', 'outboard_bd_payload_y', 'outboard_bd_payload_z',
               'outboard_bd_payload_range']

    # Create a dictionary and list in which we'll store STS variable data and variable names, respectively
    sts_dict = {}
    stored_variables = []

    # Code assumes a list of STS files
    if isinstance(sts_file, str):
        sts_file = [sts_file]
    elif isinstance(sts_file, list):
        sts_file = sts_file
    else:
        print("Invalid filenames input.")
        return stored_variables

    for s_file in sts_file:
        with open(s_file, 'r') as f:
            lines = f.readlines()

        # In STS files, the beginning of the data starts after the last time 'END_OBJECT' is found
        end_objects = [l for l, line in enumerate(lines) if 'END_OBJECT' in line]
        end_headers = end_objects[-1]
        data = lines[end_headers+1:]
        data = [d.strip().split() for d in data]  # Remove extra spaces, then split on whitespaces

        # Create the STS dictionary
        for h, head in enumerate(headers):
            data_column = [d[h] for d in data[:10]]
            if head not in sts_dict:
                sts_dict[head] = data_column
            else:
                sts_dict[head].extend(data_column)

    # We need to create datetime objects from the sts_dict's year, doy, hour, min, sec, and msec data
    year = sts_dict['year']
    doy = sts_dict['doy']
    hour = sts_dict['hour']
    min = sts_dict['min']
    sec = sts_dict['sec']
    msec = sts_dict['msec']

    # First get year, month, and day
    dates = [datetime.datetime.strptime('{}+{}'.format(yr, dy), '%Y+%j') for yr, dy in zip(year, doy)]
    # Then add in the sts_dict's hour, min, sec, and msec data
    dtimes = [d.replace(hour=int(hr), minute=int(mn), second=int(s), microsecond=int(ms), tzinfo=datetime.timezone.utc)
              for d, hr, mn, s, ms in zip(dates, hour, min, sec, msec)]
    sts_dict['time_unix'] = dtimes

    # These keys are no longer necessary, nix them
    remove_time_keys = ['year', 'doy', 'hour', 'min', 'sec', 'msec']
    for key in remove_time_keys:
        try:
            sts_dict.pop(key)
        except KeyError:
            print('Key {} was not found'.format(key))

    # Don't create tplot vars if that's not what's desired
    if read_only:
        return sts_dict

    for var_name in sts_dict.keys():
        to_merge = False
        if var_name in pytplot.data_quants.keys() and merge:
            prev_data_quant = pytplot.data_quants[var_name]
            to_merge = True
        # create variable name
        obs_specific = prefix + var_name + suffix
        # if all values are NaN, continue
        if all(v is None for v in sts_dict[var_name]):
            continue
        # store data in tplot variable
        if var_name != 'time_unix':
            try:
                pytplot.store_data(
                    obs_specific, data={'x': sts_dict['time_unix'], 'y': [np.float(val) for val in sts_dict[var_name]]})
            except ValueError:
                continue
        if obs_specific not in stored_variables:
            stored_variables.append(obs_specific)

        if to_merge is True:
            cur_data_quant = pytplot.data_quants[var_name]
            plot_options = copy.deepcopy(pytplot.data_quants[var_name].attrs['plot_options'])
            pytplot.data_quants[var_name] = xr.concat([prev_data_quant, cur_data_quant], dim='time')
            pytplot.data_quants[var_name].attrs['plot_options'] = plot_options

    if notplot:
        return sts_dict

    return stored_variables
