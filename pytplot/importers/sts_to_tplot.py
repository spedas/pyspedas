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
import time

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

    # Create a dictionary and list in which we'll store STS variable data and variable names, respectively
    start_t = time.time()
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
    sts_file.sort()
    for s_file in sts_file:
        column_names, vec_names = read_column_names(s_file)
        headers = [item for sublist in column_names for item in sublist]
        with open(s_file, 'r') as f:
            lines = f.readlines()
        # In STS files, the beginning of the data starts after the last time 'END_OBJECT' is found
        end_objects = [l for l, line in enumerate(lines) if 'END_OBJECT' in line]
        end_headers = end_objects[-1]
        data = lines[end_headers+1:]
        data = [d.strip().split() for d in data]  # Remove extra spaces, then split on whitespaces
        # Create the STS dictionary
        for h, head in enumerate(headers):
            data_column = [d[h] for d in data]
            if head not in sts_dict:
                sts_dict[head] = data_column
            else:
                sts_dict[head].extend(data_column)

    # We need to create datetime objects from the sts_dict's year, doy, hour, min, sec, and msec data
    year = sts_dict['TIME_YEAR']
    doy = sts_dict['TIME_DOY']
    hour = sts_dict['TIME_HOUR']
    min = sts_dict['TIME_MIN']
    sec = sts_dict['TIME_SEC']
    msec = sts_dict['TIME_MSEC']

    dtimes = [datetime.datetime(int(yr),1,1,int(hr),int(mn),int(s),int(ms)*1000, tzinfo=datetime.timezone.utc) + datetime.timedelta(int(dy)-1)
              for yr, dy, hr, mn, s, ms in zip(year, doy, hour, min, sec, msec)]

    sts_dict['time_unix'] = dtimes
    # These keys are no longer necessary, nix them
    remove_time_keys = ['TIME_YEAR', 'TIME_DOY', 'TIME_HOUR', 'TIME_MIN', 'TIME_SEC', 'TIME_MSEC']
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
                    obs_specific, data={'x': sts_dict['time_unix'], 'y': [float(val) for val in sts_dict[var_name]]})
            except ValueError:
                continue

        if to_merge is True:
            cur_data_quant = pytplot.data_quants[var_name]
            plot_options = copy.deepcopy(pytplot.data_quants[var_name].attrs)
            pytplot.data_quants[var_name] = xr.concat([prev_data_quant, cur_data_quant], dim='time').sortby('time')
            pytplot.data_quants[var_name].attrs = plot_options

    # Now merge vectors
    for cn,vn in zip(column_names, vec_names):
        if vn == 'TIME':
            continue
        if vn is not None:
            names_to_join = []
            for c in cn:
                names_to_join.append(prefix+c+suffix)
            pytplot.join_vec(names_to_join, vn, merge=True)
            stored_variables.append(vn)
            pytplot.del_data(names_to_join)
        else:
            stored_variables.append(prefix+cn[0]+suffix)

    if notplot:
        return sts_dict

    return stored_variables


def read_column_names(sts_file):
    column_names = []
    vec_names = []
    record_object = False
    in_scalar_and_vector_object = False
    in_vector_object = False
    in_scalar_object = False

    with open(sts_file, 'r') as f:
        for line in f:
            line = line.split()
            if line == ["OBJECT","=","RECORD"]:
                record_object = True
            if record_object:
                if line == ["OBJECT", "=", "VECTOR"]:
                    in_vector_object = True
                    vec_column_names = []
                if line == ["OBJECT", "=", "SCALAR"]:
                    if in_vector_object:
                        in_scalar_and_vector_object = True
                    else:
                        in_scalar_object = True
                if line == ["END_OBJECT"]:
                    if in_scalar_and_vector_object:
                        in_scalar_and_vector_object = False
                    elif in_vector_object:
                        in_vector_object = False
                        column_names.append(vec_column_names)
                    elif in_scalar_object:
                        in_scalar_object = False
                    else:
                        # This is where we exit
                        return column_names, vec_names
                if line[0] == "NAME":
                    if in_vector_object and not in_scalar_and_vector_object:
                        vec_name = line[-1]
                        vec_names.append(vec_name)
                    if in_scalar_and_vector_object:
                        column_name = vec_name+"_"+line[-1]
                        vec_column_names.append(column_name)
                    if in_scalar_object:
                        column_name = line[-1]
                        column_names.append([column_name])
                        vec_names.append(None)


