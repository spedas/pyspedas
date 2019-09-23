# -*- coding: utf-8 -*-
"""
File:
    themis_load.py

Description:
    Data loading functions for the THEMIS mission.

Example:
    pyspedas.themis_load(['2015-12-31'], ['tha'], '*', ['l2'])

Parameters:
    dates: str/list of str ['yyyy-mm-dd']
        List of dates to be downloaded (eg. ['2015-12-31']).
    probes: str/list of str
        Probes for missions with multiple probes (eg. ['tha', 'thb']),
        wildcard ('*') for all probes.
    instruments: str/list of str
        List of instruments (eg. ['fft']), wildcard ('*') for all instruments.
    level: str
        Either 'l2' or 'l1'.
    downloadonly: bool (True/False)
        If True then CDF files are downloaded only,
        if False then they are also loaded into pytplot using cdf_to_tplot.
    varformat : str
        The file variable formats to load into tplot.
        Wildcard character "*" is accepted.
        By default, all variables are loaded in.
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
    List of possible values for "probes" variable:
    ['tha', 'tha', 'thc', 'thd', 'the']

    List of possible values for L2 themis "instruments" variable:
    ['efi', 'esa', 'fbk', 'fft', 'fgm', 'fit', 'gmom', 'mom', 'scm', 'sst']

    List of possible values for L1 themis "instruments" variable:
    ['bau', 'eff', 'efp', 'efw', 'esa', 'fbk', 'fff_16', 'fff_32', 'fff_64',
    'ffp_16', 'ffp_32', 'ffp_64', 'ffw_16', 'ffw_32', 'ffw_64', 'fgm', 'fit',
    'hsk', 'mom', 'scf', 'scm', 'scmode', 'scp', 'scw', 'spin', 'sst', 'state',
    'trg', 'vaf', 'vap', 'vaw']
"""

import os
import pyspedas
from .themis_helpers import get_instruments, get_probes


def themis_filename(dates, probes, instruments, level):
    """Create a list of tuples for downloading: remote_file, local_file"""
    prefs = pyspedas.get_spedas_prefs()
    if 'themis_remote' in prefs:
        remote_path = prefs['themis_remote']
    else:
        raise NameError('remote_path is not found in spd_prefs_txt.py')
    if 'data_dir' in prefs:
        data_dir = prefs['data_dir'] + 'themis'
        if ('data_dir_unix' in prefs) and (os.name != 'nt'):
            data_dir = prefs['data_dir_unix'] + 'themis'
    else:
        raise NameError('data_dir is not found in spd_prefs_txt.py')

    if level != 'l1':
        level = 'l2'
    probes = get_probes(probes)
    instruments = get_instruments(instruments, level)
    dates = pyspedas.get_dates(dates)

    if level == 'l1':
        version = '?'
    else:
        version = '1'

    file_list = []
    for sdate in dates:
        year = sdate[0:4]
        month = sdate[5:7]
        day = sdate[8:10]
        for probe in probes:
            for instrument in instruments:
                # file_dir = 'tha/l2/fgm/2015/'
                file_dir = probe + '/' + level + '/' + instrument + '/' + year
                file_dir_local = os.path.join(probe, level, instrument, year)
                # filename = 'tha_l2_fgm_20150101_v01.cdf'
                filename = probe + '_' + level + '_' + instrument + '_'\
                    + year + month + day + '_v0' + version + '.cdf'

                remote_file = remote_path + '/' + file_dir + '/' + filename
                local_file = os.path.join(data_dir, file_dir_local, filename)

                file_list.append((remote_file, local_file))

    return file_list


def themis_load(dates, probes, instruments, level, downloadonly=False,
                varformat=None, get_support_data=False, prefix='', suffix=''):
    """Loads themis data into pytplot variables"""

    file_list = themis_filename(dates, probes, instruments, level)
    # print(file_list)
    count = 0
    dcount = 0

    for remotef, localf in file_list:
        count += 1
        resp, err, localfile = pyspedas.download_files(remotef, localf)
        if resp:
            print(str(count) + '. File was downloaded. Location: ' + localfile)
            dcount += 1
            if not downloadonly:
                try:
                    cdfvars = pyspedas.cdf_to_tplot(localfile, varformat,
                                                    get_support_data, prefix,
                                                    suffix, False, True)

                except TypeError as e:
                    msg = "cdf_to_tplot could not load " + localfile
                    + "\nError:\n" + str(e)
                    print(msg)

        else:
            print(str(count) + '. There was a problem. Could not download \
                  file: ' + remotef)
            print(err)

    if len(dates) == 2:
        pyspedas.time_clip(cdfvars, dates[0], dates[1], cdfvars)

    print('Downloaded ' + str(dcount) + ' files.')
    print('tplot variables:')
    print(pyspedas.tplot_names())
