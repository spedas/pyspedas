# -*- coding: utf-8 -*-
"""
File:
    omni_load.py

Description:
    Data loading functions for OMNI.

Example:
    pyspedas.omni_load('2015-12-31', '5min', False)

Parameters:
    dates: str/list of str ['yyyy-mm-dd']
        List of dates to be downloaded (eg. ['2015-12-31']).
    level: str
        Either '1min' or '5min'.
    downloadonly: bool (True/False)
        If True then CDF files are downloaded only,
        if False then they are also loaded into pytplot using cdf_to_tplot.
    varformat : str
        The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.
    get_support_data: bool
        Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".
    prefix: str
        The tplot variable names will be given this prefix.
        By default, no prefix is added.
    suffix: str
        The tplot variable names will be given this suffix.
        By default, no suffix is added.

Notes:
    https://cdaweb.gsfc.nasa.gov/istp_public/data/omni/hro_1min/2017/
    omni_hro_1min_20171201_v01.cdf
"""

import os
import pytplot
import pyspedas


def omni_filename(dates, level):
    """Create a list of tuples for downloading: remote_file, local_file"""
    prefs = pyspedas.get_spedas_prefs()
    if 'omni_remote' in prefs:
        remote_path = prefs['omni_remote']
    else:
        raise NameError('remote_path is not found in spd_prefs.txt')
    if 'data_dir' in prefs:
        data_dir = prefs['data_dir'] + 'omni'

    else:
        raise NameError('data_dir is not found in spd_prefs.txt')

    if level != '1min':
        level = '5min'

    dates = pyspedas.get_dates(dates)
    version = '?'

    file_list = []
    for sdate in dates:
        year = sdate[0:4]
        month = sdate[5:7]

        file_dir = r'hro_' + level + '/' + year
        file_dir_local = os.path.join('hro_' + level, year)
        filename = r'omni_hro_' + level + '_' + year + month + '01' + '_v0' \
                                + version + '.cdf'

        remote_file = remote_path + '/' + file_dir + '/' + filename
        local_file = os.path.join(data_dir, file_dir_local, filename)

        if len([item for item in file_list if item[0] == remote_file]) == 0:
            file_list.append((remote_file, local_file))

    return file_list


def omni_load(dates, level, downloadonly=False, varformat=None,
              get_support_data=False, prefix='', suffix=''):
    """Loads OMNI data into pytplot variables"""

    file_list = omni_filename(dates, level)

    # 1. Download files
    count = 0
    downloaded_files = []
    for remotef, localf in file_list:
        count += 1
        resp, err, localfile = pyspedas.download_files(remotef, localf)
        if resp:
            print(str(count) + '. File was downloaded. Location: ' + localfile)
            downloaded_files.append(localfile)
        else:
            print(str(count) + '. Error: Could not download file: ' + remotef)
            print(err)
    print('Downloaded ' + str(len(downloaded_files)) + ' files.')

    # 2. Load files into tplot
    downloaded_vars = []
    if not downloadonly:
        try:
            downloaded_vars = pytplot.cdf_to_tplot(downloaded_files, varformat,
                                                   get_support_data, prefix,
                                                   suffix, False, True)
        except TypeError as e:
            msg = "cdf_to_tplot could not load all data.\nError:\n" + str(e)
            print(msg)
    print('Loaded ' + str(len(downloaded_vars)) + ' variables.')

    # 3. Time clip
    if len(downloaded_vars) > 0:
        pyspedas.time_clip(downloaded_vars, dates[0], dates[1], '')
