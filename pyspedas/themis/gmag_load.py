# -*- coding: utf-8 -*-
"""
File:
    gmag_load.py

Desrciption:
    Data loading functions for the THEMIS GMAG stations.

Example:
    pyspedas.gmag_load(['2015-12-31'], ['bmls', 'ccnv', 'drby'])

Parameters:
    dates: str/list of str ['yyyy-mm-dd']
        List of dates to be downloaded (eg. ['2015-12-31']).
    stations: str/list of str
        GMAG station names (eg. 'bmls').
    group: str
        GMAG group of stations (eg. 'epo').
        If specified, then stations is ignored.
    downloadonly: bool
        If True then CDF files are downloaded only, if False
        then they are also loaded into pytplot using pytplot.cdf_to_tplot.
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
    For gmag station names and groups, see:
        http://themis.ssl.berkeley.edu/gmag/gmag_list.php
"""


import requests
import os
import pyspedas

gmag_dict = {}


def query_gmags():
    """ returns a dictionary of gmag stations and all their metadata
    """

    url = 'http://themis.ssl.berkeley.edu/gmag/gmag_json.php'
    global gmag_dict

    params = dict(
        station='',
        group=''
    )
    resp = requests.get(url=url, params=params)
    data = resp.json()
    gmag_dict = data

    return data


def get_group(station_name):
    """ returns a list with the groups that station belongs to
    """

    global gmag_dict
    group_list = []
    if gmag_dict == {}:
        gmag_dict = query_gmags()

    for station in gmag_dict:
        if station['ccode'].lower() == station_name:
            for key, value in station.items():
                if value == 'Y':
                    if station['ccode'].lower() not in group_list:
                        group_list.append(key)

    return group_list


def gmag_list(group='all'):
    """ returns a list of stations
        prints a list of "stations: start date - end date"
    """

    global gmag_dict
    station_list = []
    if gmag_dict == {}:
        gmag_dict = query_gmags()

    for station in gmag_dict:
        station_name = station['ccode'].lower()
        station_group = get_group(station_name)
        if group in ['all', '*', ''] or group in station_group:
            station_list.append(station_name)
            print(station_name + ": from " + station['day_first'] + " to "
                  + station['day_last'])

    return station_list


def gmag_groups():
    """ returns a dictionary of station groups with a list of stations
        prints a list of "group:'stations'"
    """

    global gmag_dict
    group_dict = {}
    if gmag_dict == {}:
        gmag_dict = query_gmags()

    for station in gmag_dict:
        for key, value in station.items():
            if value == 'Y':
                if key in group_dict:
                    if station['ccode'].lower() not in group_dict[key]:
                        group_dict[key].append(station['ccode'].lower())
                else:
                    group_dict[key] = []
                    group_dict[key].append(station['ccode'].lower())

    # print them
    print()
    for g, s in group_dict.items():
        print(g + ":" + ",'".join(s) + "'")

    return group_dict


def check_gmag(station_name):
    """ returns 1 if station_name is in the gmag list, 0 otherwise"
    """

    global gmag_dict
    if gmag_dict == {}:
        gmag_dict = query_gmags()

    for station in gmag_dict:
        if station['ccode'].lower() == station_name.lower():
            return 1

    return 0


def check_greenland(station_name):
    """ returns 1 if station_name is in the greenland gmag list, 0 otherwise"
    """

    global gmag_dict
    if gmag_dict == {}:
        gmag_dict = query_gmags()

    for station in gmag_dict:
        if station['ccode'].lower() == station_name.lower():
            if ((station['country'] is not None
                 and station['country'].lower() == 'greenland')
                or (station['greenland'] is not None
                    and station['greenland'].lower() == 'y')):
                return 1

    return 0


def gmag_filename(dates, stations):
    """Create a list of tuples for downloading: remote_file, local_file"""
    prefs = pyspedas.get_spedas_prefs()
    if 'themis_remote' in prefs:
        remote_path = prefs['themis_remote']
    else:
        raise NameError('remote_path is not found in spd_prefs.txt')
    if 'data_dir' in prefs:
        data_dir = prefs['data_dir']

    else:
        raise NameError('data_dir is not found in spd_prefs.txt')

    dates = pyspedas.get_dates(dates)

    file_list = []

    probe = 'thg'
    level = 'l2'
    instrument = 'mag'
    version = '1'
    if stations[0] == 'idx':
        level = 'l1'

    for sdate in dates:
        year = sdate[0:4]
        month = sdate[5:7]
        day = sdate[8:10]
        for station in stations:
            # file_dir = 'tha/l2/fgm/2015/'
            if station == 'idx':
                level = 'l1'
                file_dir = probe + '/' + level + '/' + instrument + '/' \
                    + station + '/' + year
                filename = probe + '_' + level + '_' + station + '_' + year \
                    + month + day + '_v0' + version + '.cdf'
            elif check_greenland(station):
                # thg/greenland_gmag/l2
                file_dir = probe + '/greenland_gmag/' + level + '/' \
                    + station + '/' + year
                filename = probe + '_' + level + '_' + instrument + '_' \
                    + station + '_' + year + month + day + '_v0' \
                    + version + '.cdf'
            else:
                # thg/l2/mag/
                file_dir = probe + '/' + level + '/' + instrument + '/' \
                    + station + '/' + year
                filename = probe + '_' + level + '_' + instrument + '_' \
                    + station + '_' + year + month + day + '_v0' \
                    + version + '.cdf'

            file_dir_local = os.path.join(probe, level, instrument,
                                          station, year)
            # thg_l2_mag_amd_20170109_v01.cdf
            remote_file = remote_path + '/' + file_dir + '/' + filename
            local_file = os.path.join(data_dir, file_dir_local, filename)

            file_list.append((remote_file, local_file))

    return file_list


def gmag_load(dates, stations, group=None, downloadonly=False, varformat=None,
              get_support_data=False, prefix='', suffix=''):
    """Loads themis data into pytplot variables"""

    if group is not None:
        stations = gmag_list(group)

    file_list = gmag_filename(dates, stations)

    count = 0
    dcount = 0
    for remotef, localf in file_list:
        count += 1
        resp, err, locafile = pyspedas.download_files(remotef, localf)
        if resp:
            print(str(count) + '. File was downloaded. Location: ' + locafile)
            dcount += 1
            if not downloadonly:
                try:
                    testcdf = pyspedas.cdf_to_tplot(locafile, varformat,
                                                    get_support_data, prefix,
                                                    suffix, False, True)
                    print(testcdf)
                except TypeError as e:
                    msg = "cdf_to_tplot could not load " + locafile
                    + "\nError:\n" + str(e)
                    print(msg)

        else:
            print(str(count) + '. There was a problem. Could not download \
                  file: ' + remotef)
            print(err)

    print('Downloaded ' + str(dcount) + ' files.')
    print('tplot variables:')
    print(pyspedas.tplot_names())
